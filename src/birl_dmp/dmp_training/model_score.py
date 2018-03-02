import numpy 
import ipdb
import util
import dtw

def score(model, orig_mat, list_of_random_startend):

    list_of_gen_mat = []
    for idx, tup in enumerate(list_of_random_startend):
        now_start = tup[0]
        now_end = tup[1]
        list_of_gen_mat.append(
            util.generalize_via_dmp(now_start, now_end, model)
        ) 

    list_of_dtwdistance = []
    for idx, gen_mat in enumerate(list_of_gen_mat):
        dist, cost, acc, path = dtw.dtw(orig_mat, gen_mat, dist=lambda x, y: numpy.linalg.norm(x - y, ord=2))
        list_of_dtwdistance.append(dist)

    debug_var = zip(list_of_gen_mat, list_of_dtwdistance)

    return sum(list_of_dtwdistance), debug_var
   
