import os
import copy
import datetime
from .tools_unit_constant import unit_ang2au

## -----------------------
## read xxxx_PARAM.rrm
## -----------------------
def parser_grrm_param(fname):
    t_json={}

    t_json["jobtime"]="none"
    t_json["kinetype"]="none"
    t_json["universal_gamma"]=0.0
    t_json["readbareenergy"]=False
    t_json["infile"]="none"
    t_json["scpathpara"]="none"
    t_json["jobtype"]="none"
    t_json["pathtype"]="none"
    t_json["nobondrearrange"]=0  ## 0: OFF, 1: ON
    t_json["siml_temperature_kelvin"]=[]
    t_json["siml_pressure_atm"]=1.0
    t_json["energyshiftvalue_au"]=0.0
    t_json["level"]="none"
    t_json["part"]=[]

    
    ## get file time
    oldest_last_modified=-1
    tmp_fn_time=fname
    if os.path.exists(tmp_fn_time):
        stat = os.stat(tmp_fn_time)
        last_modified = stat.st_mtime
        if oldest_last_modified==-1 or oldest_last_modified>last_modified:
            oldest_last_modified=last_modified

    tmp_fn_time="%s_DC_list.log" % (fname[:-(len("_PARAM.rrm"))])
    if os.path.exists(tmp_fn_time):
        stat = os.stat(tmp_fn_time)
        last_modified = stat.st_mtime
        if oldest_last_modified==-1 or oldest_last_modified>last_modified:
            oldest_last_modified=last_modified

    tmp_fn_time="%s_TS_list.log" % (fname[:-(len("_PARAM.rrm"))])
    if os.path.exists(tmp_fn_time):
        stat = os.stat(tmp_fn_time)
        last_modified = stat.st_mtime
        if oldest_last_modified==-1 or oldest_last_modified>last_modified:
            oldest_last_modified=last_modified

    tmp_fn_time="%s.log" % (fname[:-(len("_PARAM.rrm"))])
    if os.path.exists(tmp_fn_time):
        stat = os.stat(tmp_fn_time)
        last_modified = stat.st_mtime
        if oldest_last_modified==-1 or oldest_last_modified>last_modified:
            oldest_last_modified=last_modified

    dt = datetime.datetime.fromtimestamp(oldest_last_modified)
    t_json["jobtime"]=dt.strftime("%Y/%m/%d-%H:%M:%S")


    ## Open file
    fdat = open(fname, 'r')

    ## get Job type
    line = fdat.readline() ## INPUT DATA SET OF THE GRRM VER. 13.x
    if   "INPUT DATA SET OF THE GRRM VER" in line:
        t_json["grrmversion"]=line.split()[7]
    line = fdat.readline() ## -------------------------------------------------------------------------

    ##-------------------
    ## get Link Program
    ##-------------------
    line = fdat.readline()
    if   "----------------------------------------------------" in line:
        pass
    elif "Energy Calculation =" in line:
        if     "GAMESS" in line: t_json["linkprog"]="gamess"
        elif "GAUSSIAN" in line: t_json["linkprog"]="gaussian"
        elif "ORCA"   in line: t_json["linkprog"]="orca"
        elif "SIESTA"   in line: t_json["linkprog"]="siesta"
        else:
            print ("SPPR: parser_grrm_param.py")
            print ("SPPR: Please add if _grrm_pxdb_param:")
            print (line)
            quit()

        ## read out one line
        line = fdat.readline()


    ##-------------------
    ## InFile
    ##-------------------
    line = fdat.readline()
    if   "----------------------------------------------------" in line:
        pass
    elif   "InFile =" in line:
        t_json["infile"]=line.split()[-1]
        line = fdat.readline()

    ##-------------------
    ## get Job type
    ##-------------------
    line = fdat.readline()
    if   "----------------------------------------------------" in line:
        print("PXDB: parser_grrm_pxdb_param.py: There is no job type!")
        quit()
    elif "Job type =" in line :
        if   "Job type = 3"  in line: t_json["jobtype"]="saddle"
        elif "Job type = 4"  in line: t_json["jobtype"]="irc"
        elif "Job type = 5"  in line: t_json["jobtype"]="2pshs"
        elif "Job type = 6"  in line: t_json["jobtype"]="scw"
        elif "Job type = 7"  in line: t_json["jobtype"]="addf"
        elif "Job type = 8"  in line: t_json["jobtype"]="restruct"
        elif "Job type = 9"  in line: t_json["jobtype"]="reenergy"
        elif "Job type = 12" in line: t_json["jobtype"]="mc-afir"
        elif "Job type = 13" in line: t_json["jobtype"]="lup"
        elif "Job type = 14" in line: t_json["jobtype"]="repath"
        elif "Job type = 16" in line: t_json["jobtype"]="sc-afir"
        elif "Job type = 17" in line: t_json["jobtype"]="ds-afir"
        elif "Job type = 1"  in line: t_json["jobtype"]="freq"
        elif "Job type = 2"  in line: t_json["jobtype"]="min"
        else:
            t_json["jobtype"]="none"
            print ("Please add if _grrm_pxdb_param:")
            print (line)
            quit()

        ## increase one line
        line = fdat.readline()


    ##-------------------
    ## MO File
    ##-------------------
    line = fdat.readline()
    if   "----------------------------------------------------" in line:
        pass
    else:

        t_func_basis=line.lower().split()[0]
        t_d=line.lower()
        t_json["level"]="%s" % (t_func_basis)

        ## for skip one line
        line = fdat.readline() ## -------------------------------------------------------------------------



    line = fdat.readline() ## 0 3 19 19 0
    t_d=line.split()
    if line.strip()!="":
        t_json["totalcharge"]=int(t_d[0])
        t_json["spinmulti"]=int(t_d[1])
        t_json["natoms"]=int(t_d[2])
    else:
        t_json["totalcharge"]=0
        t_json["spinmulti"]=1
        t_json["natoms"]=0

    line = fdat.readline() ## -------------------------------------------------------------------------

    t_atomname=[]
    t_intxyz=[]
    t_part=[]
    for iatom in range(0, t_json["natoms"]):
        line = fdat.readline()
        t_d=line.split()
        t_atomname.append(t_d[0])
        t_w=[]
        t_w.append(float(t_d[1])*unit_ang2au())
        t_w.append(float(t_d[2])*unit_ang2au())
        t_w.append(float(t_d[3])*unit_ang2au())
        t_intxyz.append(t_w)
        if len(t_d)>=5:
            t_part.append(int(t_d[4]))
        else:
            t_part.append(0)

    t_json["initxyz"]=t_intxyz
    t_json["atomname"]=t_atomname
    t_json["part"]=t_part

    line = True
    line_count=0
    while line:
        line = fdat.readline()
        if "-------------------------------------------------------------------------":
            line_count=line_count+1                
            
        if line_count == 4:
            break

    ## Read Options Line
    while line:
        line = fdat.readline()

        if "KeepLUPPaths" in line:
            t_json["pathtype"]="luppath"

        ## Parallel
        if "SC = PathPara" in line:
            t_d=line.split("-")[1]
            ipara=int(t_d.split("/")[0])
            npara=int(t_d.split("/")[1])
            t_json["scpathpara"]="%d/%d" % (ipara,npara)

        elif "OPT =" in line and "LOOSE" in line:
            t_json["optloose"]="loose"

        elif "SIML_tempearture =" in line:
            t_d=line.split("=")[1].split()
            t_d2=[]
            for itmp in range(0,len(t_d)):
                t_d2.append(float(t_d[itmp]))
            t_json["siml_temperature_kelvin"]=copy.deepcopy(t_d2)

        elif "Pressure =" in line:
            t_d=line.split()[2]
            t_json["siml_pressure_atm"]=float(t_d)

        elif "NoBondRearrange" in line:
            t_json["nobondrearrange"]=1  ## 0: OFF, 1: ON

        elif "ShiftE =" in line and "hartree" in line:
            t_json["energyshiftvalue_au"]=float(line.split()[2])

        ## Second input:
        elif "ADD INTERACTION" in line:
            fn_addint="%s_ADDINT.rrm" %  (fname[:-(len("_PARAM.rrm"))])
            
            if os.path.exists(fn_addint):

                ## fn_addinteraction file
                faddint = open(fn_addint, 'r')
                line_addint=True
                while line_addint:
                    line_addint = faddint.readline()
                    if "universal" in line_addint.lower():
                        t_json["universal_gamma"]\
                            =float(line_addint.split("=")[1].split()[0])

                faddint.close()

            else:
                pass

        elif "AddUniversalFORCE =" in line:
            t_json["universal_gamma"]\
                =float(line.split("=")[1].split()[0])

        elif "ReadBareEnergy" in line:
            t_json["readbareenergy"]=True

        elif "TrafficVolCheck" in line and t_json["kinetype"]:
            t_json["kinetype"]="traf-vol-chk"

        elif "RetroSynth" in line:
            t_json["kinetype"]="retrosynth"

        ## not set option
        else:
            pass


    fdat.close()

    ## --------------------
    ## control temperature
    ## --------------------
    if len(t_json["siml_temperature_kelvin"])==0:
        t_json["siml_temperature_kelvin"].append(300.0)

    return t_json


