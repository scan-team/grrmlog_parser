import math
import os
import copy
import numpy as np
from .tools_unit_constant import unit_ang2au

## -----------------------
## read xxxx.log
## -----------------------
def parser_grrm_main_log(fname):

    developer_comment = 0  ## 0. OFF, 1. ON
    if ".log" in fname[-4:]:
        fname_top=fname[0:-4]
    else:
        fname_top=fname
        fname=fname+".log"
    
    t_json={}
    t_json["jobstatus"]="none"
    t_json["jobmessage"]="none"
    t_json["ngradient"]=-1
    t_json["nhessian"]=-1
    t_json["elapsedtime_sec"]=0.0

    
    ## -------------------------
    ## get TS irc first step   
    ## -------------------------
    out_ngradient=-1
    out_nhessian=-1
    out_elapsedtime_sec=0.0

    
    ## -------------
    ##   file open
    ## -------------
    fdat = open(fname, 'r')
    line = fdat.readline()
    while line:
        if "Normal termination of the GRRM Program" in line:
            if t_json["jobstatus"]!="notconverged":
                t_json["jobstatus"]="finished" ##
            line = fdat.readline()

        elif "Normal termination of Global Reaction Route Mapping Programs" in line:
            if t_json["jobstatus"]!="notconverged":
                t_json["jobstatus"]="finished" ##
            line = fdat.readline()
            
        elif "NUMBER OF FORCE CALCULATIONS        :" in line:
            out_ngradient=int(line.split()[5])
            line = fdat.readline()

        elif "NUMBER OF HESSIAN CALCULATIONS      :" in line:
            out_nhessian=int(line.split()[5])
            line = fdat.readline()

        elif "TOTAL ELAPSED TIME                  :" in line:
            out_elapsedtime_sec=float(line.split()[4])
            line = fdat.readline()

        else:
            line = fdat.readline()

    if t_json["jobstatus"]=="finished":
        t_json["ngradient"]=out_ngradient
        t_json["nhessian"]=out_nhessian
        t_json["elapsedtime_sec"]=out_elapsedtime_sec

    fdat.close()

    ## ---------------
    ##   get message
    ## ---------------
    fn_judge="%s_message_STOP.rrm" % (fname_top)
    if os.path.exists(fn_judge):
        t_json["jobmessage"]="stop"
        fn_judge="%s_message_CONTINUE.rrm" % (fname_top)
        if os.path.exists(fn_judge):
            t_json["jobmessage"]="continue"
            if t_json["jobstatus"]=="none":
                t_json["jobstatus"]="continue" ##

    fn_judge="%s_message_DETECT.rrm" % (fname_top)
    if os.path.exists(fn_judge):
        t_json["jobmessage"]="END"

    fn_judge="%s_message_ERROR.rrm" % (fname_top)
    if os.path.exists(fn_judge):
        t_json["jobmessage"]="error"
        if t_json["jobstatus"]=="none":
            t_json["jobstatus"]="error" ##

    fn_judge="%s_message_END.rrm" % (fname_top)
    if os.path.exists(fn_judge):
        t_json["jobmessage"]="end"
        t_json["jobstatus"]="finished" ##
    
    return t_json

