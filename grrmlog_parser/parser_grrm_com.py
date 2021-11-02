import numpy as np
from .tools_unit_constant import unit_ang2au

## -----------------------
## read xxxx.com
## -----------------------
def parser_grrm_com(fname):

    t_json={}
    t_json["link"]=[]
    t_json["level"]=""
    t_json["atomname"]=["H"]
    t_json["xyz"]=[[0.0,0.0,0.0]]
    t_json["natoms"]=1

    ## Open file 
    fdat = open(fname, 'r')
    line = True
    while line:
        line = fdat.readline()
        if "#" in line:
            t_json["level"]=line.strip()
            break
        else:
            t_json["link"].append(line.strip())
    
    ## get xyz
    line = fdat.readline()
    line = fdat.readline()
    t_d=line.split()
    t_nam=[]
    t_xyz=[]
    while line:
        line = fdat.readline()
        if "options" in line.lower():
            break
        else:
            t_d=line.split()
            t_nam.append(t_d[0])
            work1=[]
            work1.append(float(t_d[1])*unit_ang2au())
            work1.append(float(t_d[2])*unit_ang2au())
            work1.append(float(t_d[3])*unit_ang2au())
            t_xyz.append(work1)
            
    natoms=len(t_nam)
        
    ## set information
    t_json["atomname"]=t_nam
    t_json["xyz"]=t_xyz
    t_json["natoms"]=natoms
    
    return t_json


