import os
import copy
from .tools_unit_constant import unit_ang2au, unit_au2ang
from .parser_grrm_param         import parser_grrm_param

def parser_grrm_tslist(fname):
    
    fdat = open(fname, 'r')
    out_list=[]
    
    ## get number of EQs
    ieq_cout=-1

    tag_first_struct=0
    line = True
    while line:

        line = fdat.readline()
        if "# Geometry of TS" in line:
            ## get EQ 
            t_d=line.split()
            ieq_cout=int(t_d[4].split(",")[0])
            ieq_sym=t_d[7]

            ## put the last dat into json:
            if tag_first_struct != 0:
                out_list.append(t_json)
            else:
                tag_first_struct=1
                
            ## put the last dat into json:
            t_json={}


            ## Load xyz geometry in [Bohr]
            t_nam=[]
            t_xyz=[]
            while line:
                line = fdat.readline()
                if "Energy" in line:
                    break
                else:
                    t_d=line.split()
                    t_nam.append(t_d[0])
                    t_w=[]
                    t_w.append(float(t_d[1])*unit_ang2au())
                    t_w.append(float(t_d[2])*unit_ang2au())
                    t_w.append(float(t_d[3])*unit_ang2au())
                    t_xyz.append(t_w)

            ## save into the lib
            t_json["symmetry"]=ieq_sym
            t_json["atomname"]=copy.deepcopy(t_nam)
            t_json["xyz"]=copy.deepcopy(t_xyz)
            t_json["category"]="TS"
            t_json["comment"]="TS%d" % (ieq_cout)
            t_json["num"]=ieq_cout
            t_json["energy"]=[0.0]
            t_json["connection"]=[-1,-1]
            t_json["frequency_cm"]=[]
            t_json["hess_eigenvalue_au"]=[]
            t_json["gradient"]=[]
            t_json["s2_value"]=0.0
            t_json["dipole"]=[]
            t_json["pathdata"]=[]

        ## GET ENERGY
        if "Energy" in line:
            line = line.replace("Energy","").replace("=","").replace("(","").replace(":","").replace(")","")
            t_d=line.split()
            
            if len(t_d) == 1:
                t_json["energy"]=[float(t_d[0])]
            elif len(t_d) == 2:
                t_json["energy"]=[float(t_d[0]), float(t_d[1])]
            elif len(t_d) == 3:
                t_json["energy"]=[float(t_d[0]), float(t_d[1]), float(t_d[2])]
            else:
                print("SPPR SYSTEM: in parser_grrm_eqlist.py. Energy not found !!")


            t_eigenvalue=[]
            while 1:
                line = fdat.readline()
                if "CONNECTION" in line:
                    break
                elif "Spin" in line:
                    t_json["s2_value"]=float(line.split()[2])
                elif "ZPVE" in line or "Normal mode eigenvalues" in line:
                    pass
                else:
                    t_d=line.split()
                    for ielem in range(0, len(t_d)):
                        t_eigenvalue.append(float(t_d[ielem]))

            t_json["hess_eigenvalue_au"]=copy.deepcopy(t_eigenvalue)


        ## GET ENERGY
        if "CONNECTION" in line:
            t_d=line.split(":")[1]
            t_con0 = t_d.split("-")[0]
            t_con1 = t_d.split("-")[1]

            if "DC" in t_con0 or "?" in t_con0:
                t_json["connection"][0]=-1
            else:
                t_json["connection"][0]=int(t_con0)

            if "DC" in t_con1 or "?" in t_con1:
                t_json["connection"][1]=-1
            else:
                t_json["connection"][1]=int(t_con1)

            t_json["comment"]="%s CON(%d,%d)" % (t_json["comment"], t_json["connection"][0], t_json["connection"][1])
            

    fdat.close()    

    ## put the last data
    if ieq_cout >= 0: 
        out_list.append(t_json)

        if len(out_list)>0:
            return out_list


    ## --------------------
    ## load param file
    ## --------------------
    fn_param_rrm="none"
    fn_tsptlist_log_1="none"
    if "_TS_list.log" in fname.split("/")[-1]:
        fn_param_rrm="%s_PARAM.rrm" % (fname[:-(len("_TS_list.log"))])
        fn_tsptlist_log_1="%s_TS_list.log_1" % (fname[:-(len("_TS_list.log"))]) 
        
    elif "_PT_list.log" in fname.split("/")[-1]:
        fn_param_rrm="%s_PARAM.rrm" % (fname[:-(len("_PT_list.log"))])
        fn_tsptlist_log_1="%s_PT_list.log_1" % (fname[:-(len("_PT_list.log"))])


    ## --------------------
    ## load PT_list.log_1
    ## --------------------
    if len(out_list)==0 and os.path.exists(fn_tsptlist_log_1):
        out_list=parser_grrm_tslist(fn_tsptlist_log_1)
        
        if len(out_list)>0:
            return out_list


    ## -------------------------
    ## load infile PT_list.log
    ## -------------------------
    fn_infile_log="none"
    param_infile="none"
    param_jobtype="none"
    if len(out_list)==0 and os.path.exists(fn_param_rrm):

        ## get the infile information
        param_dat=parser_grrm_param(fn_param_rrm)
        param_jobtype=param_dat["jobtype"]
        param_infile=param_dat["infile"]
        if param_jobtype=="repath" and param_infile!="none":
            dn_infile=fname[:-(len(fname.split("/")[-1])+1)]

            if "_TS_list.log" in fname.split("/")[-1]:
                fn_infile_log="%s/%s_TS_list.log" % (dn_infile, param_infile)
            elif "_PT_list.log" in fname.split("/")[-1]:
                fn_infile_log="%s/%s_PT_list.log" % (dn_infile, param_infile)

            if os.path.exists(fn_infile_log):
                out_list=parser_grrm_tslist(fn_infile_log)
    
    return out_list


