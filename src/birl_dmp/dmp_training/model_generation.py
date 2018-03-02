import pydmps.dmp_discrete
import ipdb
import numpy as np

def get_model(mat, model_type, model_config):
    if model_type == 'pydmps':
        n_dmps = mat.shape[1]
        model_config['ay'] = np.ones(n_dmps)*model_config['ay']
        dmp = pydmps.dmp_discrete.DMPs_discrete(n_dmps=n_dmps, **model_config)
        dmp.imitate_path(y_des=mat.T)
        return dmp
        
        
