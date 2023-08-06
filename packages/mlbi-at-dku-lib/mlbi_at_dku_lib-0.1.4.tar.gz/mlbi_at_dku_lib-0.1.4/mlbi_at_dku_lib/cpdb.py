import copy, os, time, warnings
import numpy as np
import pandas as pd
import scanpy as sc
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
from subprocess import Popen, PIPE
import shlex

def run_command(cmd, verbose = True):
    cnt = 0
    with Popen(shlex.split(cmd), stdout=PIPE, bufsize=1, \
               universal_newlines=True ) as p:
        for line in p.stdout:
            if (line[:14] == 'Tool returned:'):                    
                cnt += 1
            elif cnt > 0:
                pass
            else: 
                if verbose:
                    print(line, end='')
                    
        exit_code = p.poll()
    return exit_code


def cpdb_run( df_cell_by_gene, cell_types, out_dir,
              gene_id_type = 'gene_name', db = None, 
              n_iter = None, pval_th = None, mean_th = None):
    
    start = time.time()
    print('Running CellPhoneDB .. ')    
    X = df_cell_by_gene.astype(int) 
    ## X = (X.div(X.sum(axis = 1), axis=0)*1e6).astype(int)
    
    if out_dir[-1] == '/':
        out_dir = out_dir[:-1]
    
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
        
    file_meta = '%s/meta_tmp.tsv' % out_dir
    file_cpm = '%s/exp_mat_tmp.tsv' % out_dir
    
    X.transpose().to_csv(file_cpm, sep = '\t')
    df_celltype = pd.DataFrame({'cell_type': cell_types}, 
                               index = X.index.values)    
    df_celltype.to_csv(file_meta, sep = '\t')
    
    cmd = 'cellphonedb method statistical_analysis '
    cmd = cmd + '%s %s ' % (file_meta, file_cpm)
    cmd = cmd + '--counts-data=%s ' % gene_id_type
    if pval_th is not None: cmd = cmd + '--pvalue=%f ' % pval_th
    if mean_th is not None: cmd = cmd + '--threshold=%f ' % mean_th
    if n_iter is not None: cmd = cmd + '--iterations=%i ' % n_iter
    if db is not None: '--database %s ' % db
    cmd = cmd + '--output-path %s ' % out_dir

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        run_command(cmd) 
    
    elapsed = time.time() - start
    print('Running CellPhoneDB .. done. %i' % elapsed )    
    
    if os.path.exists(file_cpm):
        os.remove(file_cpm)
    if os.path.exists(file_meta):
        os.remove(file_meta)
    
    return cmd
    
    
def split_cellphonedb_out(df):
    cols = df.columns.values
    items = cols[:10]
    pairs = cols[10:]
    df_items = df[items]
    df_pairs = df[pairs]    
    return df_items, df_pairs    
    
def cpdb_get_res( out_dir ):
    
    ## Load p_values
    df_pval = pd.read_csv('%s/pvalues.txt' % out_dir, sep = '\t', 
                          index_col = 0)    
    df_pval_items, df_pval_pairs = split_cellphonedb_out(df_pval)
    
    ## Load means
    df_mean = pd.read_csv('%s/means.txt' % out_dir, sep = '\t', 
                          index_col = 0)    
    df_mean_items, df_mean_pairs = split_cellphonedb_out(df_mean)
    
    ## Check integrity
    idxp = list(df_pval_items.index.values)
    idxm = list(df_mean_items.index.values)
    idxc = set(idxp).intersection(idxm)
    cnt = 0
    for p, m in zip(idxp, idxm):
        if p != m:
            cnt += 1
    if cnt > 0:
        print( len(idxc), len(df_pval_items.index.values), 
               len(df_mean_items.index.values), cnt )
    
    return df_mean_items, df_mean_pairs, df_pval_items, df_pval_pairs   


def to_vector(df, rows, cname):    
    cols = df.columns.values
    idxs, gps, cps, vals = [], [], [], []
    ga, gb, ca, cb = [], [], [], []
    
    for c in list(cols):
        vt = list(df[c])
        ct = [c]*len(vt)
        gt = list(rows)
        it = []
        for r in gt:
            idx = '%s--%s' % (r,c)
            it.append(idx)            
        idxs = idxs + it
        gps = gps + gt
        cps = cps + ct
        vals = vals + vt
        ga = ga + [g.split('_')[0] for g in gt]
        gb = gb + [g.split('_')[1] for g in gt]
        ca = ca + [g.split('|')[0] for g in ct]
        cb = cb + [g.split('|')[1] for g in ct]
        
    dfo = pd.DataFrame({'gene_pair': gps, 'cell_pair': cps, 
                        'gene_A': ga, 'gene_B': gb,
                        'cell_A': ca, 'cell_B': cb,
                         cname: vals}, index = idxs)    
    return dfo

def cpdb_get_vec( df_info, df_mean_pairs, df_pval_pairs, 
                  pval_max = 0.05, mean_min = 0.01 ):    
    dfp = to_vector(df_pval_pairs, 
                    df_info['interacting_pair'], 'pval')
    dfm = to_vector(df_mean_pairs, 
                    df_info['interacting_pair'], 'mean')
    b = (dfp['pval'] <= pval_max) & (dfm['mean'] >= mean_min) 
    b = b & (~dfp['pval'].isnull()) & (~dfm['mean'].isnull())
    dfp = dfp.loc[b,:].copy(deep=True)
    dfm = dfm.loc[b,:].copy(deep=True)   
    dfp['mean'] = dfm['mean']    
    return dfp    


def cpdb_get_results( out_dir, pval_max = 0.05, mean_min = 0.01 ):
    df_mean_info, df_mean_pairs, df_pval_info, df_pval_pairs = \
          cpdb_get_res( out_dir )
    dfv = cpdb_get_vec( df_pval_info, df_mean_pairs, df_pval_pairs, 
                        pval_max = pval_max, mean_min = mean_min )
    '''
    idxs = list(dfv.index.values)
    rend = {}
    for idx in idxs:
        if dfv.loc[idx,'cell_A'] > dfv.loc[idx,'cell_B']:
            ca = dfv.loc[idx,'cell_A']
            cb = dfv.loc[idx,'cell_B']
            ga = dfv.loc[idx,'gene_A']
            gb = dfv.loc[idx,'gene_B']   
            dfv.loc[idx,'cell_A'] = cb
            dfv.loc[idx,'cell_B'] = ca
            dfv.loc[idx,'gene_A'] = gb
            dfv.loc[idx,'gene_B'] = ga
            idx_new = '%s_%s--%s|%s' % (gb, ga, cb, ca)
            dfv.loc[idx,'cell_pair'] = '%s|%s' % (cb, ca)
            dfv.loc[idx,'gene_pair'] = '%s|%s' % (gb, ga)
            rend[idx] = idx_new

    if len(rend.keys()) > 0:
        dfv.rename(index = rend, inplace = True)
    '''        
    return df_pval_info, df_pval_pairs, df_mean_pairs, dfv


def cpdb_plot( dfp, mkr_sz = 6, tick_sz = 6, 
                             legend_fs = 11, title_fs = 14,
                             dpi = 120, title = None, swap_ax = False ):
    if swap_ax == False:
        a = 'gene_pair'
        b = 'cell_pair'
    else:
        b = 'gene_pair'
        a = 'cell_pair'
    
    y = len(set(dfp[a]))
    x = len(set(dfp[b]))
    
    print('%i %ss, %i %ss found' % (y, a, x, b))
    
    pv = -np.log10(dfp['pval']+1e-10).round()
    np.min(pv), np.max(pv)
    
    mn = np.log2((1+dfp['mean']))
    np.min(mn), np.max(mn)    
    
    w = x/6
    sc.settings.set_figure_params(figsize=(w, w*(y/x)), 
                                  dpi=dpi, facecolor='white')
    fig, ax = plt.subplots()

    mul = mkr_sz
    scatter = ax.scatter(dfp[b], dfp[a], s = pv*mul, c = mn, 
                         linewidth = 0, cmap = 'Reds')

    legend1 = ax.legend(*scatter.legend_elements(),
                        loc='upper left', 
                        bbox_to_anchor=(1+1/x, 0.5), 
                        title=' log2(m) ', 
                        fontsize = legend_fs)
    legend1.get_title().set_fontsize(legend_fs)
    ax.add_artist(legend1)

    # produce a legend with a cross section of sizes from the scatter
    handles, labels = scatter.legend_elements(prop='sizes', alpha=0.6)
    # print(labels)
    labels = [1, 2, 3, 4, 5]
    legend2 = ax.legend(handles, labels, loc='lower left', 
                        bbox_to_anchor=(1+1/x, 0.5), 
                        title='-log10(p)', 
                        fontsize = legend_fs)
    legend2.get_title().set_fontsize(legend_fs)

    if title is not None: plt.title(title, fontsize = title_fs)
    plt.yticks(fontsize = tick_sz)
    plt.xticks(rotation = 90, ha='center', fontsize = tick_sz)
    plt.margins(x=0.6/x, y=0.6/y)
    plt.show()   
    return 

def cpdb_get_gp_n_cp(idx):
    
    items = idx.split('--')
    gpt = items[0]
    cpt = items[1]
    gns = gpt.split('_')
    ga = gns[0]
    gb = gns[1]
    cts = cpt.split('|')
    ca = cts[0]
    cb = cts[1]
    
    return gpt, cpt, ga, gb, ca, cb
    
    
def cpdb_add_interaction( file_i, file_c = None, 
                          file_p = None, file_g = None, 
                          out_dir = 'cpdb_out'):
        
    if file_i is None:
        print('ERROR: provide file containing interaction info.')
        return None
    if not os.path.exists(file_i):
        print('ERROR: %s not found' % file_i)
    
    if file_c is not None:
        if not os.path.exists(file_c):
            print('ERROR: %s not found' % file_c)
            return None
    
    if file_p is not None:
        if not os.path.exists(file_p):
            print('ERROR: %s not found' % file_p)
            return None

    if file_g is not None:
        if not os.path.exists(file_g):
            print('ERROR: %s not found' % file_g)
            return None
    
    cmd = 'cellphonedb database generate '
    cmd = cmd + '--user-interactions %s ' % file_i
    if file_c is not None: cmd = cmd + '--user-complex %s ' % file_c
    if file_p is not None: cmd = cmd + '--user-protein %s ' % file_p
    if file_g is not None: cmd = cmd + '--user-gene %s ' % file_g
    cmd = cmd + '--result-path %s ' % out_dir

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        run_command(cmd) 
        pass
    
    print('Updated DB files saved to %s' % out_dir )    
    return out_dir