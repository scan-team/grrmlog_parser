import os

def tools_get_abs_fn_top(fn_abs_rel):

    dn_pwd=os.getcwd()

    if "/" not in fn_abs_rel:
        fn_top=fn_abs_rel
        dn_abs=dn_pwd
        fn_abs_abs="%s/%s" % (dn_abs, fn_top)
    elif "./" in fn_abs_rel[:2]:
        fn_top=fn_abs_rel.split("/")[-1]
        dn_abs=fn_abs_rel[:-(len(fn_top)+1)]\
            .replace("./","%s/" % (dn_pwd))
        fn_abs_abs="%s/%s" % (dn_abs, fn_top)
    else:
        fn_top=fn_abs_rel.split("/")[-1]
        dn_abs=fn_abs_rel[:-(len(fn_top)+1)]
        fn_abs_abs=fn_abs_rel
        
    return fn_abs_abs

