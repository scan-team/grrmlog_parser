import os
import copy
from .tools_unit_constant import unit_ang2au, unit_au2ang
from .parser_grrm_param         import parser_grrm_param

def parser_grrm_eqlist(fname):
    fdat = open(fname, 'r')
    
    out_list=[]

    ## get number of EQs
    ieq_cout=-1
    tag_first_eq=0
    line = True
    while line:

        line = fdat.readline()
        if "# Geometry of EQ" in line:

            ## get EQ 
            t_d=line.split()
            ieq_cout=int(t_d[4].split(",")[0])
            ieq_sym=t_d[7]

            ## put the last dat into json:
            if tag_first_eq != 0:
                out_list.append(t_json)
            else:
                tag_first_eq=1
                
            ## put the last dat into json:
            t_json={}

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
            t_json["comment"]="EQ%d" % (ieq_cout)
            t_json["category"]="EQ"
            t_json["to_be_applied"]=None
            t_json["to_be_applied_0"]=None
            t_json["to_be_applied_1"]=None
            t_json["to_be_applied_2"]=None
            t_json["trafficvolume"]=None
            t_json["trafficvolume_0"]=None
            t_json["trafficvolume_1"]=None
            t_json["trafficvolume_2"]=None
            t_json["sim_yield"]=None
            t_json["sim_yield_0"]=None
            t_json["sim_yield_1"]=None
            t_json["sim_yield_2"]=None
            t_json["pop_yield"]=None
            t_json["pop_yield_0"]=None
            t_json["pop_yield_1"]=None
            t_json["pop_yield_2"]=None
            t_json["num"]=ieq_cout
            t_json["energy"]=[0.0]
            t_json["hess_eigenvalue_au"]=[]
            t_json["gradient"]=[]
            t_json["s2_value"]=0.0
            t_json["dipole"]=[]
            
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
                print("SYSTEM: in parser_grrm_eqlist.py. Energy not found !!")

            t_eigenvalue=[]
            while 1:
                line = fdat.readline()
                if ""==line.strip():
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


    fdat.close()    

    ## put in the last EQ data
    if tag_first_eq==1:
        out_list.append(t_json)

        

    ## ------------------------------------
    ##   load EQ_list.log_0
    ## ------------------------------------
    fn_eqlist_log_1="%s_EQ_list.log_1" % (fname[:-(len("_EQ_list.log"))])
    
    if len(out_list)==0 and os.path.exists(fn_eqlist_log_1):
        out_list=parser_grrm_eqlist(fn_eqlist_log_1)

    
    ######################################
    ##   load param file for empty EQ_list
    ######################################
    fn_param_rrm="%s_PARAM.rrm" % (fname[:-12])
    fn_infile_log=None
    param_infile=None
    param_jobtype=None
    if len(out_list)==0 and os.path.exists(fn_param_rrm):
        ## get the infile information
        param_dat=parser_grrm_param(fn_param_rrm)
        param_jobtype=param_dat["jobtype"]
        param_infile=param_dat["infile"]

        ## Load infile job EQ_list
        if param_jobtype=="repath" and param_infile!=None:
            dn_infile=fname[:-(len(fname.split("/")[-1])+1)]
            fn_infile_log="%s/%s_EQ_list.log" % (dn_infile, param_infile)
            if os.path.exists(fn_infile_log):
                out_list=parser_grrm_eqlist(fn_infile_log)


    ######################################
    ## get To be applied
    ## from  xxxx_EQ_test.rrm  x=0~2
    ######################################
    fn_eqtst="%s_EQ_test.rrm" % (fname[:-12])
    to_be_applied_key="to_be_applied"
    if os.path.exists(fn_eqtst) and len(out_list)>0:
        out_list=_load_testlog_file(fn_eqtst, out_list, to_be_applied_key)

    ## from  xxxx_EQ_test.rrm_x  x=0~2
    for itemp in range(0,3):
        fn_eqtst="%s_EQ_test.rrm_%d" % (fname[:-12], itemp)
        to_be_applied_key="to_be_applied_%d" % (itemp)
        if os.path.exists(fn_eqtst) and len(out_list)>0:
            out_list=_load_testlog_file(fn_eqtst, out_list, to_be_applied_key)



    ######################################
    ## get traffic volume and sim yields
    ## from  xxxx_sim.log_x  x=0~2
    ######################################
    for itemp in range(0,3):
        fn_eqtst="%s_sim.log_%d" % (fname[:-12], itemp)
        yield_key="sim_yield_%d" % (itemp)
        trafvol_key="trafficvolume_%d" % (itemp)
        if os.path.exists(fn_eqtst) and len(out_list)>0:
            out_list=_load_simlog_file(fn_eqtst, out_list, yield_key, trafvol_key)


    ######################################
    ## get population
    ## from  xxxx_popl.rrm_x x=0~2
    ######################################
    for itemp in range(0,3):
        fn_eqtst="%s_EQ_popl.rrm_%d" % (fname[:-12], itemp)
        population_key="pop_yield_%d" % (itemp)
        if os.path.exists(fn_eqtst) and len(out_list)>0:
            out_list=_load_popllog_file(fn_eqtst, out_list, population_key)


    return out_list



######################################
##  get To be applied
######################################
def _load_testlog_file(fn_eqtst, out_list, to_be_applied_key):
    fdat = open(fn_eqtst, 'r')
    
    ## get number of EQs
    ieq_cout=0
    line = True
    while line:
        line = fdat.readline()
        if "Not to be applied" in line:
            out_list[ieq_cout][to_be_applied_key]=0
        elif "To be applied" in line:
            out_list[ieq_cout][to_be_applied_key]=1
        ieq_cout = ieq_cout +1
    fdat.close()
    return out_list



######################################
## get traffic volume and sim yields
######################################
def _load_simlog_file(fn_eqtst, out_list, yield_key, trafvol_key):
    fdat = open(fn_eqtst, 'r')
    line = True
    while line:
        ieq_cout=None
        line = fdat.readline()
        #Traffic volume for EQ -   138 : 0.00000e+00 (Yield = 0.00000)
        #Traffic volume for EQ -   139 : 0.00000e+00 (Yield = 0.00000)
        #Traffic volume for EQ -   140 : 0.00000e+00 (Yield = 0.00000)
        if "Traffic volume for EQ" in line and "BoltzPopl" not in line and "Yield" in line:
            data=line.replace(")","").split()
            ieq_cout=int(data[5])
            out_list[ieq_cout][yield_key]=float(data[10])
            out_list[ieq_cout][trafvol_key]=float(data[7])

        #Traffic volume for EQ -     0 : 8.17506e-01
        #Traffic volume for EQ -     1 : 5.97471e-01
        #Traffic volume for EQ -     2 : 3.12910e-01
        elif "Traffic volume for EQ" in line and "BoltzPopl" not in line and "Yield" not in line:
            data=line.split()
            ieq_cout=int(data[5])
            out_list[ieq_cout][trafvol_key]=float(data[7])
    fdat.close()    

    return out_list



######################################
## get population
######################################
def _load_popllog_file(fn_eqtst, out_list, population_key):
    fdat = open(fn_eqtst, 'r')
    ieq_cout=0
    line = True
    while line:
        line = fdat.readline()
        #Population of EQ -     0 : 7.51198e-01
        #Population of EQ -     1 : 1.23935e-01
        #Population of EQ -     2 : 1.24866e-01
        #Population of EQ -     3 : 7.11687e-112
        if "Population of EQ" in line:
            data=line.split()
            ieq_cout=int(data[4])
            data=line.split(":")
            out_list[ieq_cout][population_key]=float(data[1])
    fdat.close()
    
    return out_list


