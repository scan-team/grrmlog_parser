import copy

def parser_grrm_modify_energy(fname_top, json_eqlist, json_tslist, json_ptlist):

    ntslist=len(json_tslist)
    for its in range(0, ntslist):
        if len(json_tslist[its]["energy"])==1:
            pass
        else:
            if json_tslist[its]["energy"][1]!=0.0:
                t_ene_univ = json_tslist[its]["energy"][0]
                json_tslist[its]["energy"][0] = json_tslist[its]["energy"][1]
                json_tslist[its]["energy"][1] = t_ene_univ
                
    neqlist=len(json_eqlist)
    for ieq in range(0, neqlist):
        if len(json_eqlist[ieq]["energy"]) == 1:
            pass
        
        else:
            if json_eqlist[ieq]["energy"][1] != 0.0:
                t_ene_univ = json_eqlist[ieq]["energy"][0]
                json_eqlist[ieq]["energy"][0] = json_eqlist[ieq]["energy"][1]
                json_eqlist[ieq]["energy"][1] = t_ene_univ

    nptlist=len(json_ptlist)
    for ipt in range(0, nptlist):
        if len(json_ptlist[ipt]["energy"]) == 1:
            pass
        
        else:
            if json_ptlist[ipt]["energy"][1] != 0.0:
                t_ene_univ = json_ptlist[ipt]["energy"][0]
                json_ptlist[ipt]["energy"][0] = json_ptlist[ipt]["energy"][1]
                json_ptlist[ipt]["energy"][1] = t_ene_univ

        for inode in range(0, len(json_ptlist[ipt]["pathdata"])):
            if len(json_ptlist[ipt]["pathdata"][inode]["energy"]) == 1:
                pass
            else:
                if json_ptlist[ipt]["pathdata"][inode]["energy"][1] != 0.0:
                    t_ene_univ= json_ptlist[ipt]["pathdata"][inode]["energy"][0]
                    json_ptlist[ipt]["pathdata"][inode]["energy"][0]=json_ptlist[ipt]["pathdata"][inode]["energy"][1]
                    json_ptlist[ipt]["pathdata"][inode]["energy"][1]=t_ene_univ
                    
                    
    return copy.deepcopy(json_eqlist), copy.deepcopy(json_tslist), copy.deepcopy(json_ptlist)

