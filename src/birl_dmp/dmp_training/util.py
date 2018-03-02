import numpy
import ipdb

def get_dmp_model(mat, model_type):
    if model_type == 'pydmps':
        import pydmps.dmp_discrete
        n_dmps = mat.shape[1]
        dmp = pydmps.dmp_discrete.DMPs_discrete(n_dmps=n_dmps, n_bfs=100, ay=numpy.ones(n_dmps)*5)
        dmp.imitate_path(y_des=mat.T)
        return dmp

def generalize_via_dmp(start, end, model):
    import pydmps
    import ipdb
    if type(model)==dict and \
        'dmp_instance' in model and \
        issubclass(type(model['dmp_instance']), pydmps.dmp_discrete.DMPs_discrete):
        dmp_instance = model['dmp_instance']
    
        gen_ay = model['gen_ay']
        new_dmp = pydmps.dmp_discrete.DMPs_discrete(n_dmps=dmp_instance.n_dmps, n_bfs=100, ay=numpy.ones(dmp_instance.n_dmps)*gen_ay, w=dmp_instance.w)

        new_dmp.y0 = numpy.array(start)
        new_dmp.goal = numpy.array(end)
        y_track, dy_track, ddy_track = new_dmp.rollout(tau=1)
        return y_track
        
