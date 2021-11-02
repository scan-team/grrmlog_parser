import os
def tools_judge_grrm_log(fn_abs_top):

    tag_judge_grrm_log=True

    fn_abs_log=fn_abs_top+".log"
    if os.path.exists(fn_abs_log):
        pass
    else:
        print("GRRM: Not exist! %s" % (fn_abs_log))
    
    return tag_judge_grrm_log

