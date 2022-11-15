import os
import glob
import copy
from .tools_judge_grrm_log import tools_judge_grrm_log

## ----------------------------------
##   get all filename of GRRM type log
## ----------------------------------
def get_filename_list_abs_path\
    (dn_base, ndepth=10):
    """
    get file list in dn_base
    ndepth is how deep directories are searched 
    from the directory.
    """
    
    ## initialize
    ls_fn_abs=[]

    ## initialize
    if not os.path.isdir(dn_base):
        return ls_fn_abs

    keyword="_PARAM.rrm"
    inp_star=""
    for idepth in range(0, ndepth):
        ## set keyword
        tmp_keyword_idepth="%s/%s*%s" \
            % (dn_base, inp_star, keyword)

        ## get file list
        tmp_fn_list=glob.glob(tmp_keyword_idepth)
        for ifn in range(0, len(tmp_fn_list)):

            fn_abs_top\
                =tmp_fn_list[ifn][:-(len(keyword))]

            ## judge log
            tag_grrm_map_log\
                =tools_judge_grrm_log(fn_abs_top)

            ## To control uploading to SCAN : not upload
            if os.path.exists("%s.scan.donot.upload.txt" % (fn_abs_top)):
                pass
            
            ## add in list
            elif os.path.exists("%s_EQ_list.log" % (fn_abs_top))\
               and os.path.exists("%s_PT_list.log" % (fn_abs_top))\
               and os.path.exists("%s.log" % (fn_abs_top)):
                ls_fn_abs.append(copy.deepcopy(fn_abs_top))

        ## add star directory
        inp_star="*/%s" % (inp_star)

    return ls_fn_abs

