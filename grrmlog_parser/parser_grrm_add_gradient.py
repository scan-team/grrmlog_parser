import copy
import numpy as np

def parser_grrm_add_gradient\
    (fname_top, json_eqlist, json_tslist, json_ptlist, json_datlist):

    ndatlist=len(json_datlist)

    ## ---------------------
    ##  No dat information
    ## ---------------------
    if ndatlist==0:
        return copy.deepcopy(json_eqlist), copy.deepcopy(json_tslist), copy.deepcopy(json_ptlist)

    ## ---------------------------
    ##  Find geometries from dat 
    ## --------------------------
    ls_tag_used=np.zeros(ndatlist, dtype=int)

    t_comment=""
    
    ntslist=len(json_tslist)
    for its in range(0, ntslist):
        json_tslist[its], ls_tag_used\
            =_assign_dat_json(json_tslist[its], \
                             json_datlist, \
                             ls_tag_used,\
                              tag_del=False,\
                              t_comment="TS%d" % its)

    neqlist=len(json_eqlist)
    for ieq in range(0, neqlist):
        json_eqlist[ieq], ls_tag_used\
            =_assign_dat_json(json_eqlist[ieq], \
                             json_datlist, \
                             ls_tag_used,\
                              tag_del=False,\
                              t_comment="EQ%d" % ieq)
        
    nptlist=len(json_ptlist)
    npathnode=0
    for ipt in range(0, nptlist):
        json_ptlist[ipt], ls_tag_used\
            =_assign_dat_json(json_ptlist[ipt],\
                             json_datlist, \
                             ls_tag_used,\
                              tag_del=False,\
                              t_comment="PT%d" % ipt)
        
        if "pathdata" in json_ptlist[ipt]:
            npathnode=npathnode + len(json_ptlist[ipt]["pathdata"])
            for inode in range(0,  len(json_ptlist[ipt]["pathdata"])):
                json_ptlist[ipt]["pathdata"][inode], ls_tag_used\
                    =_assign_dat_json(json_ptlist[ipt]["pathdata"][inode],\
                                      json_datlist,\
                                      ls_tag_used,\
                                      tag_del=True,\
                                      t_comment="NODE%d" % inode)
            
    
    return copy.deepcopy(json_eqlist), copy.deepcopy(json_tslist), copy.deepcopy(json_ptlist)



## ---------------------------
##   Assign dat obj
## --------------------------
def _assign_dat_json(t_json, json_datlist, \
                     ls_tag_used, tag_del=False,\
                     t_comment="none"):

    for idat in range(0, len(json_datlist)): 
        if ls_tag_used[idat]==0:  ## 0: not used, 1: already used
            tag_load=False
            if t_json["energy"][0]==json_datlist[idat]["energy"][0]:
                if t_json["s2_value"]==json_datlist[idat]["s2_value"]:
                    if t_json["xyz"]==json_datlist[idat]["xyz"]:
                        tag_load=True
                        
            if tag_load:

                ## delete from dat
                if tag_del:
                    ls_tag_used[idat]=1 ## 0: not used, 1: already used
                t_json["gradient"]=json_datlist[idat]["gradient"]
                t_json["dipole"]=json_datlist[idat]["dipole"]

                break
        
        else:
            pass

    return t_json, ls_tag_used



