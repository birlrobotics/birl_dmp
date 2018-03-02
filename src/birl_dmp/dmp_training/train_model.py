import model_config_generation
import model_score
import ipdb
import os
import util
import numpy 
DEBUG_MODE = True

def filter_static_points(mat):
    last = mat[0]
    new_mat = [last]
    for idx in range(mat.shape[0]):
        if numpy.linalg.norm(mat[idx]-last) < 0.01:
            pass
        else:
            new_mat.append(mat[idx])
            last = mat[idx]

    return numpy.array(new_mat)

def run(mat, model_type, model_config):
    mat = filter_static_points(mat)

    start = mat[0].copy() 
    end = mat[-1].copy() 
    noise_std = model_config['std_of_normal_noise_in_generalization_test']
    list_of_random_startend = []
    for i in range(10):
        now_end = end.copy()
        now_end[2] += i*0.01
        list_of_random_startend.append((
            start,
            #start+numpy.random.normal(0, noise_std, mat.shape[1]),
            now_end
        ))


    model_list = []
    model_generator = model_config_generation.get_model_config_generator(model_type, model_config)
    for now_model_config in model_generator:
        print
        print '-'*20
        print ' working on config:', now_model_config

        try:
            model_instance = util.get_dmp_model(mat, model_type, now_model_config)
            score, debug_var = model_score.score(model_instance, mat, list_of_random_startend)

        except Exception as e:
            print "Failed to train model_instance, will ignore it: %s"%e
            raise e
            
        if score == None:
            print "scorer says to skip this model, will do"
            continue

        model_list.append({
            "model_instance": model_instance,
            "now_model_config": now_model_config,
            "score": score,
            'debug_var': debug_var,
        })
        print 'score:', score 
        print '='*20
        print 

        model_config_generation.update_now_score(score)

    sorted_model_list = sorted(model_list, key=lambda x:x['score'])

    if len(sorted_model_list) == 0:
        print "ERORR: empty sorted_model_list."
        return None

    if DEBUG_MODE:
        for d in sorted_model_list:
            debug_var = d['debug_var']
            score = d['score']
            import matplotlib.pyplot as plt
            from mpl_toolkits.mplot3d import Axes3D
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.plot(mat[:, 0], mat[:, 1], mat[:, 2], color='black', label='orig')
            from matplotlib.pyplot import cm
            import numpy as np
            color=iter(cm.rainbow(np.linspace(0, 1, len(debug_var))))
            for tup in debug_var:
                gen_mat = tup[0]
                dist = tup[1]
                ax.plot(gen_mat[:, 0], gen_mat[:, 1], gen_mat[:, 2], color=next(color), label=dist)
            ax.set_title(score)
            ax.legend()
            ax.set_xlim3d(0, 2)
            ax.set_ylim3d(-2, 2)
            ax.set_zlim3d(-2, 2)
            fig.show()
        raw_input()

    return sorted_model_list

if __name__ == '__main__':
    import numpy
    dir_of_this_script = os.path.dirname(os.path.realpath(__file__))
    mat = numpy.load(os.path.join(dir_of_this_script, '..', 'data_for_test', 'test_mat.npy'))
    model_type = 'pydmps'
    model_config = {
        'n_bfs': [100],
        'ay': [5, 10, 15, 20, 25, 30],
        'std_of_normal_noise_in_generalization_test': 0.1,
    }
    sorted_model_list = run(mat, model_type, model_config)
    print sorted_model_list[0]

