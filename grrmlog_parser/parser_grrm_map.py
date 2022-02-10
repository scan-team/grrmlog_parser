import os
import copy
from tqdm.auto import trange
from .models import GRRMMap, EQ, Edge
from .parser_grrm_eqlist        import parser_grrm_eqlist
from .parser_grrm_tslist        import parser_grrm_tslist
from .parser_grrm_com           import parser_grrm_com
from .parser_grrm_modify_energy import parser_grrm_modify_energy
from .parser_grrm_param         import parser_grrm_param
from .parser_grrm_main_log      import parser_grrm_main_log
from .parser_grrm_dat           import parser_grrm_dat
from .parser_grrm_pt_path       import parser_grrm_pt_path
from .parser_grrm_add_gradient  import parser_grrm_add_gradient

# grrmdatsortkey:"energy"or"energy_zpc", xyzunit:"au"or"ang"
def parser_grrm_map(fn_abs_top):

    ##file check
    print('Builing filenames')
    fn_eqlist = fn_abs_top + "_EQ_list.log"
    fn_tslist = fn_abs_top + "_TS_list.log"
    fn_dclist = fn_abs_top + "_DC_list.log"
    fn_ptlist = fn_abs_top + "_PT_list.log"
    fn_param = fn_abs_top + "_PARAM.rrm"
    fn_com = fn_abs_top + ".com"
    fn_top =  fn_abs_top.split("/")[-1]
    dn_abs_map = fn_abs_top[:-(len(fn_top)+1)]

    ## get file list
    print('Retrieving files list')
    work_fname_list = os.listdir(dn_abs_map)

    ## check data
    print('Checking data presence')
    tag_1eq_2dc_4ts_8pt=0
    if "%s_EQ_list.log" % (fn_top) in work_fname_list: tag_1eq_2dc_4ts_8pt=tag_1eq_2dc_4ts_8pt + 1
    if "%s_DC_list.log" % (fn_top) in work_fname_list: tag_1eq_2dc_4ts_8pt=tag_1eq_2dc_4ts_8pt + 2
    if "%s_TS_list.log" % (fn_top) in work_fname_list: tag_1eq_2dc_4ts_8pt=tag_1eq_2dc_4ts_8pt + 4
    if "%s_PT_list.log" % (fn_top) in work_fname_list: tag_1eq_2dc_4ts_8pt=tag_1eq_2dc_4ts_8pt + 8

    ## Error message:
    if tag_1eq_2dc_4ts_8pt < 4:
        print("GRRM-MAP: Warning in parser_grrm_map_log.py")
        print("GRRM-MAP: This program require at least files below.")
        print("GRRM-MAP: xxxxx_TS_list.log or xxxxx_PT_list.log")
        print("GRRM-MAP: tag_1eq_2dc_4ts_8pt = %d" % tag_1eq_2dc_4ts_8pt)
        print("GRRM-MAP: fname_top %s" % (fn_abs_top))
        raise IndentationError("grrm")


    ## Get job type
    print('Extracting job type')
    t_jobtype="none"
    if os.path.exists(fn_param):
        param_dat=parser_grrm_param(fn_param)
        t_jobtype=param_dat["jobtype"]
    else:
        param_dat={}
        param_dat["jobtype"]="none"
        param_dat["pathtype"]="none"


    ## prepare the log data
    out_json={}

    ## Load EQ list
    print('Extracting EQ data')
    if os.path.exists(fn_eqlist):
        out_json["EQ"]=parser_grrm_eqlist(fn_eqlist)
    else:
        out_json["EQ"]=[]

    ## Load TS list
    print('Extracting TS data')
    if os.path.exists(fn_tslist):
        out_json["TS"]=parser_grrm_tslist(fn_tslist)
    else:
        out_json["TS"]=[]

    ## Load PT list
    print('Extracting PT data')
    if os.path.exists(fn_ptlist):
        out_json["PT"]=parser_grrm_tslist(fn_ptlist)
    else:
        out_json["PT"]=[]

    ## Load DAT file including gradient
    print('Extracting PT gradient data')
    if os.path.exists(fn_ptlist):
        out_json["DAT"]\
            =parser_grrm_dat\
            (fn_abs_top)
    else:
        out_json["DAT"]=[]


    ## PT path registrated
    print('Processing PT paths')
    if t_jobtype=="sc-afir"\
       or t_jobtype=="repath":
        if len(out_json["PT"])>=0:
            out_json["PT"]\
                =parser_grrm_pt_path\
                (fn_abs_top, out_json["PT"])

    ## SC-AFIR universal energy change
    ## only when universal force is not zero
    print('Correcting AFIR-induced energy change')
    if (t_jobtype=="sc-afir" or t_jobtype=="repath") and param_dat["universal_gamma"]!=0.0 and param_dat["readbareenergy"]==True:
        out_json["EQ"], out_json["TS"], out_json["PT"] \
            = parser_grrm_modify_energy(fn_abs_top, out_json["EQ"], out_json["TS"], out_json["PT"])
    elif param_dat["universal_gamma"]!=0.0:
        print()
        print("parser_grrm_map.py: Error")
        print("universal_gamma is only for sc-afir job.")
        print()
        quit()

    ## analize data
    print('Computing min/max energies')
    t_low_ene = 0.0
    t_high_ene = 0.0
    for ilist in trange(0, len(out_json["EQ"]), unit='EQ'):
        t_d = out_json["EQ"][ilist]["energy"][0]
        if t_low_ene > t_d:
            t_low_ene = t_d

        if t_high_ene < t_d or t_high_ene==0.0:
            t_high_ene = t_d

    for ilist in trange(0, len(out_json["TS"]), unit='TS'):
        t_d = out_json["TS"][ilist]["energy"][0]
        if t_low_ene > t_d:
            t_low_ene = t_d

        if t_high_ene < t_d or t_high_ene==0.0:
            t_high_ene = t_d


    ## ---------------------
    ## get data from log
    ## ---------------------
    print('Retrieving data from log file')
    t_json_main_log\
        =parser_grrm_main_log\
        ("%s.log" % (fn_abs_top))


    ## ---------------------
    ## get data from com
    ## ---------------------
    print('Retrieving data from input file')
    if len(out_json["EQ"])==0:
        data_com=parser_grrm_com(fn_com)
        natoms=data_com["natoms"]
    else:
        natoms=len(out_json["EQ"][0]["atomname"])


    ## ---------------------------------------
    ##   assign all data for each geometries
    ## ---------------------------------------
    print('Assigning gradient data to geometries')
    if len(out_json["DAT"])>=0:
        out_json["EQ"], out_json["TS"], out_json["PT"] \
            = parser_grrm_add_gradient\
            (fn_abs_top, out_json["EQ"], \
             out_json["TS"], \
             out_json["PT"], \
             out_json["DAT"])


    ## --------------------------
    ##  add all data for object
    ## --------------------------
    ## prepare the log data
    print('Converting raw data:')
    map = GRRMMap()

    print('Converting raw EQ data')
    if os.path.exists(fn_eqlist)\
       and len(out_json["EQ"])>=0:
        map.eq_list=_convert_list_to_object(out_json["EQ"],"eq")

    print('Converting raw TS data')
    if os.path.exists(fn_tslist)\
       and len(out_json["TS"])>=0:
        map.ts_list=_convert_list_to_object(out_json["TS"],"ts")

    print('Converting raw PT data')
    if os.path.exists(fn_ptlist)\
       and len(out_json["PT"])>=0:
        map.pt_list=_convert_list_to_object(out_json["PT"],"pt")

        ## Put the path data
        print('Organizing pathdata')
        for ipt in trange(0,len(map.pt_list)):
            if len(out_json["PT"][ipt]["pathdata"])!=0:
                map.pt_list[ipt].pathdata\
                    =_convert_list_to_object(out_json["PT"][ipt]["pathdata"],\
                                             "node")


    print('Converting raw gradient data')
    if len(out_json["DAT"])>=0:
        map.geom_list=_convert_list_to_object(out_json["DAT"],"dat")

    ## ---------------------------
    ##   summary
    ## ---------------------------
    print('Converting map related global information')
    map.param={}
    map.fname_top_abs=fn_abs_top
    map.fname_top_rel=fn_abs_top.split("/")[-1]
    map.jobtype=t_jobtype
    map.natoms=natoms
    map.lowest_energy=t_low_ene
    map.highest_energy=t_high_ene
    map.neq=len(out_json["EQ"])
    map.nts=len(out_json["TS"])
    map.npt=len(out_json["PT"])
    map.jobtime=param_dat["jobtime"]
    map.universal_gamma=param_dat["universal_gamma"]
    map.infile=param_dat["infile"]
    map.scpathpara=param_dat["scpathpara"]
    map.pathtype=param_dat["pathtype"]
    map.nobondrearrange=param_dat["nobondrearrange"]
    map.siml_temperature_kelvin=param_dat["siml_temperature_kelvin"]
    map.siml_pressure_atm=param_dat["siml_pressure_atm"]
    map.energyshiftvalue_au=param_dat["energyshiftvalue_au"]
    map.level=param_dat["level"]
    map.spinmulti=param_dat["spinmulti"]
    map.totalcharge=param_dat["totalcharge"]

    map.atom_name=copy.deepcopy(param_dat["atomname"])
    map.initxyz=copy.deepcopy(param_dat["initxyz"])
    map.initpart=copy.deepcopy(param_dat["part"])

    ## log data
    map.jobstatus=t_json_main_log["jobstatus"]
    map.jobmessage=t_json_main_log["jobmessage"]
    map.ngradient=t_json_main_log["ngradient"]
    map.nhessian=t_json_main_log["nhessian"]
    map.elapsedtime_sec=t_json_main_log["elapsedtime_sec"]

    return map




## ---------------------------
##   convert list to object
##   EQ TS PT and DAT files
## ---------------------------
def _convert_list_to_object(t_json,inp_category):

    ## initial setting
    out_obj_list=[]

    ## main loop
    for ilist in range(0,len(t_json)):
        category=t_json[ilist]["category"]
        t_id=t_json[ilist]["num"]

        if 1==0:
            print("%s %d/%d" % (category, t_id, len(t_json)))

        if "EQ"==category:
            obj = EQ(t_id)
        elif "TS"==category:
            obj = Edge(t_id)
        elif "DAT"==category:
            obj = EQ(t_id)
        elif "NODE"==category:
            obj = EQ(t_id)
        else:
            print("GRRM: Error strange category")
            quit()

        if "EQ"==category \
           or "TS"==category\
           or "NODE"==category\
           or  "DAT"==category:

            ## -----------------------
            ##   common(EQ,TS): data
            ## -----------------------
            obj.xyz=t_json[ilist]["xyz"]
            obj.symmetry=t_json[ilist]["symmetry"]
            obj.comment=t_json[ilist]["comment"]
            obj.category = inp_category
            obj.hess_eigenvalue_au = t_json[ilist]["hess_eigenvalue_au"]
            obj.energy = t_json[ilist]["energy"]
            obj.gradient=t_json[ilist]["gradient"]
            obj.dipole = t_json[ilist]["dipole"]
            obj.s2_value = t_json[ilist]["s2_value"]


        if "EQ"==category:
            for itemp in range(0,3):
                ## Traffic volume
                if t_json[ilist]["trafficvolume_%d" % (itemp)]!=None:
                    obj.trafficvolume[itemp] =t_json[ilist]["trafficvolume_%d" % (itemp)]

                ## Population
                if t_json[ilist]["pop_yield_%d" % (itemp)]!=None:
                    obj.population[itemp]    =t_json[ilist]["pop_yield_%d" % (itemp)]

                ## Reaction Yield
                if t_json[ilist]["sim_yield_%d" % (itemp)]!=None:
                    obj.reactionyield[itemp] =t_json[ilist]["sim_yield_%d" % (itemp)]

        elif "TS"==category:
            obj.connection=t_json[ilist]["connection"]


        out_obj_list.append(copy.deepcopy(obj))

    return out_obj_list

