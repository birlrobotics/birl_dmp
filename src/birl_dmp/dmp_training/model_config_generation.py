import numpy as np
import copy

score_hist_stack = []


def _debug_score_level(s):
    print 'socre level %s: %s'%(len(score_hist_stack), s)

def update_now_score(_now_score):
    record_of_last_level = score_hist_stack[-1]
    record_of_last_level['now_score'] = _now_score
    _debug_score_level('update %s'%(_now_score,))

def init_new_score_level():
    global score_hist_stack
    score_hist_stack.append({
        "best": None, 
        "now_score": None, 
        "bad_score_count": 0, 
    })
    _debug_score_level('new score level')

def update_last_score_level():
    global score_hist_stack

    _debug_score_level('gonna update')

    record_of_this_level = score_hist_stack[-1]
    if record_of_this_level['now_score'] is None:
        _debug_score_level('no now_score for this level, abort update')
        pass
    else:
        if record_of_this_level['best'] is None\
            or record_of_this_level['now_score'] < record_of_this_level['best']:
            _debug_score_level('now_score(%s) < best(%s), will update best'%(record_of_this_level['now_score'], record_of_this_level['best']))
            record_of_this_level['best'] = record_of_this_level['now_score'] 
        else:
            _debug_score_level('now_score(%s) >= best(%s), bad_score_count %s->%s'%(record_of_this_level['now_score'], record_of_this_level['best'], record_of_this_level['bad_score_count'], record_of_this_level['bad_score_count']+1))
            record_of_this_level['bad_score_count'] += 1 

def does_bad_score_count_hit(bad_score_count_max):
    record_of_this_level = score_hist_stack[-1]
    return record_of_this_level['bad_score_count'] >= bad_score_count_max

def clear_last_score_level():
    global score_hist_stack

    _debug_score_level('gonna clear_last_score_level')

    # pass the best to upper level,
    # the upper level will need the best of this level to make a decision

    if len(score_hist_stack) > 1:
        _debug_score_level('will assign best of this level(%s) to now_score of upper level'%(score_hist_stack[-1]['best'],))
        score_hist_stack[-2]['now_score'] = score_hist_stack[-1]['best']

    del score_hist_stack[-1]

def get_model_config_generator(model_type, _model_config):
    global score_hist_stack

    model_config = copy.deepcopy(_model_config)

    score_hist_stack = []
    if model_type == 'pydmps':
        import hmmlearn.hmm 
        if type(model_config['n_bfs']) is not list:
            model_config['n_bfs'] = [model_config['n_bfs']]

        if 'max_ay' in model_config:
            model_config['ay'] = range(1, model_config['max_ay']+1)
        else:
            if type(model_config['ay']) is not list:
                model_config['ay'] = [model_config['ay']]

        print model_config

        init_new_score_level()
        for n_bfs in model_config['n_bfs']:
            update_last_score_level()
            if does_bad_score_count_hit(1):
                clear_last_score_level()
                break

            init_new_score_level()
            for ay in model_config['ay']:
                update_last_score_level()
                if does_bad_score_count_hit(3):
                    clear_last_score_level()
                    break

                now_model_config = {
                    "n_bfs": n_bfs,
                    "ay": ay,
                }
                
                yield now_model_config 
