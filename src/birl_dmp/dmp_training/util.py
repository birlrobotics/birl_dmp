
def get_dmp_model(mat, model_type, model_config):
    if model_type == 'pydmps':
        import pydmps.dmp_discrete
        import numpy as np
        n_dmps = mat.shape[1]
        model_config['ay'] = np.ones(n_dmps)*model_config['ay']
        dmp = pydmps.dmp_discrete.DMPs_discrete(n_dmps=n_dmps, **model_config)
        dmp.imitate_path(y_des=mat.T)
        return dmp

def generalize_via_dmp(start, end, model):
    import pydmps
    import ipdb
    if issubclass(type(model), pydmps.dmp_discrete.DMPs_discrete):
        model.y0 = start
        model.goal = end 
        y_track, dy_track, ddy_track = model.rollout()
        return y_track
        
