import time, os, sys
import numpy as np
import pandas as pd
from scipy import stats

SKLEARN = True
try:
    from sklearn.decomposition import PCA
except ImportError:
    SKLEARN = False
    print('DEiso ERROR: scikit-learn not installed.')

    
def DEiso_pca( dfs, n_comp = 2 ):

    rownames = ['PC%i' % (i+1) for i in range(int(n_comp))]
    pca_obj = PCA(n_components=int(n_comp))
    X_pca = pca_obj.fit_transform(dfs.transpose()).transpose()  
    df_pca = pd.DataFrame(X_pca, index = rownames, columns = dfs.columns.values)
    return df_pca


def DEiso_anal_per_gene( dfs_in, groups, gr, norm = False, log = False,
                         n_pca_comp = 0, cn_th = 1e-10, ro = 0.1, nth = 0.8 ):
    
    dfs = dfs_in.copy(deep = True)
    if norm:
        dfs = dfs.div(dfs.sum(axis = 0), axis = 1)*100
        if log:
            dfs = np.log2(dfs + 1)
            
    if n_pca_comp > 0:
        dfs = DEiso_pca( dfs, n_comp = min(n_pca_comp, dfs.shape[0]) )
    
    samples = np.array(list(dfs.columns.values))
    glst = list(groups)
    glst = list(set(glst))
    glst.sort()
    if gr in glst:
        glst.remove(gr)

    cov = {}
    mns = {}
    
    b = np.array(groups) == gr
    ssel = list(samples[b])
    
    bt = ((dfs[ssel] > 0).sum(axis = 0) > 0)
    if bt.sum() < dfs[ssel].shape[1]*nth:
        return None

    Cr = dfs[ssel].transpose().cov()
    mr = dfs[ssel].mean(axis = 1)
    
    res = {}
    for i, g in enumerate(glst):
        b = np.array(groups) == g
        ssel = list(samples[b])
        
        bt = ((dfs[ssel] > 0).sum(axis = 0) > 0)
        if bt.sum() >= dfs[ssel].shape[1]*nth:
        
            Ct = dfs[ssel].transpose().cov()
            mt = dfs[ssel].mean(axis = 1)
            m = mt - mr    

            C = Cr + Ct
            C = C + (np.diag(C).mean()*ro)*np.eye(C.shape[0])
            if np.linalg.det(C) < cn_th:
                c1 = 0
            else:
                C = np.linalg.inv(C)
                c1 = m.transpose().dot(C.dot(m))
                c1 = np.sqrt(c1)

                p1 = stats.t.sf(c1, df = dfs.shape[1])*2
                res[g] = (c1, p1)

    if len(glst) == 1:
        if g in list(res.keys()):
            return res
        else:
            return None
    else:
        return res    
    

def DEiso_anal( df, gene_names, groups, ref_group, norm = True, log = False, 
                n_pca_comp = 0, rho = 0.1, nth = 0.8, verbose = True ):
    
    if not SKLEARN:
        print('DEiso ERROR: scikit-learn not installed.', flush=True)
        return None
    
    gr = ref_group
    glst = list(set(gene_names))
    glst.sort()
    idxs = {}
    for g in glst:
        idxs[g] = []

    ilst = list(df.index.values)
    nlst = list(gene_names)
    for g, t in zip(nlst, ilst):
        idxs[g].append(t)

    start = time.time()

    df_res = None
    cnt = 0
    for k, g in enumerate(glst):
        idx = idxs[g]
        if len(idx) >= 2:
            dfs = df.loc[idx,:]
            
            bt = ((dfs > 0).sum(axis = 0) > 1)
            if bt.sum() >= dfs.shape[1]: 
                
                # v = None
                v = DEiso_anal_per_gene( dfs, groups, gr, norm = norm, log = log,
                                        n_pca_comp = n_pca_comp, ro = rho, nth = nth )
                if v is not None:
                    if isinstance(v, dict):
                        keys = v.keys()
                        if cnt == 0:
                            df_res = {}
                            for key in keys:
                                df_res[key] = pd.DataFrame(columns = ['stat', 'pval'])

                        for key in keys:
                            if key in list(df_res.keys()):
                                df_res[key].loc[g, :] = list(v[key])
                            else:
                                df_res[key] = pd.DataFrame(columns = ['stat', 'pval'])

                    else:
                        if cnt == 0:
                            df_res = pd.DataFrame(columns = ['stat', 'pval'])
                        df_res.loc[g, :] = list(v)

                    cnt += 1

        if verbose: 
            if k%100 == 0: 
                print('DEiso Progress: %i/%i(%i)   ' % (k, len(glst), cnt), end = '\r', flush=True)

    elapsed = time.time() - start
    if verbose: print('DEiso done (%i) .. %i               ' % (elapsed, cnt), flush=True)

    if df_res is not None:
        if isinstance(df_res, dict):
            for key in df_res.keys():
                df_res[key]['pval_adj'] = df_res[key]['pval']*cnt
                b = df_res[key]['pval_adj'] > 1
                df_res[key].loc[b, 'pval_adj'] = 1
                df_res[key] = df_res[key].sort_values(['stat'], ascending = False)
        else:
            df_res['pval_adj'] = df_res['pval']*cnt
            b = df_res['pval_adj'] > 1
            df_res.loc[b, 'pval_adj'] = 1
            df_res = df_res.sort_values(['stat'], ascending = False)
       
    return df_res


def save_to_excel(df_res_all, file_out):

    cnt = 0
    for key in df_res_all.keys():

        if cnt == 0: 
            with pd.ExcelWriter(file_out, mode='w') as writer:
                df_res_all[key].to_excel(writer, sheet_name = key)
        else: 
            with pd.ExcelWriter(file_out, mode='a', if_sheet_exists = 'replace') as writer:
                df_res_all[key].to_excel(writer, sheet_name = key)
        cnt += 1

    return
