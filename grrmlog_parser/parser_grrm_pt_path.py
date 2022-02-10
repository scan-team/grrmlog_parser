import os
import copy
import glob
from tqdm.auto import trange
from .tools_unit_constant import unit_ang2au, unit_au2ang
from .parser_grrm_param         import parser_grrm_param

def parser_grrm_pt_path(fn_abs_top, ls_pt_json):

    tag_read_pt_path=False

    ## Find PT log data
    for ipt in trange(0, len(ls_pt_json), unit='file'):

        fn_rel_top=fn_abs_top.split("/")[-1]

        ## Detailed output ON
        fn_pt_path="%s_PT%d.log" % (fn_abs_top, ipt)
        if os.path.exists(fn_pt_path):
            ls_pt_json[ipt]["pathdata"]\
                =_load_pt_path_file(fn_pt_path)
            tag_read_pt_path=True

        ## Detailed output OFF in SPDAT
        fn_pt_path="%s_SPDAT/%s_PT%d.log" \
            % (fn_abs_top, fn_rel_top, ipt)
        if os.path.exists(fn_pt_path):
            ls_pt_json[ipt]["pathdata"]\
                =_load_pt_path_file(fn_pt_path)
            tag_read_pt_path=True

    if len(ls_pt_json) == 0 or tag_read_pt_path==True:
        return ls_pt_json

    ## -------------------------
    ## Find infile jobs
    ## -------------------------
    fn_param_rrm="%s_PARAM.rrm" % (fn_abs_top)
    param_infile="none"
    param_jobtype="none"
    if os.path.exists(fn_param_rrm):
        ## get the infile information
        param_dat=parser_grrm_param(fn_param_rrm)
        param_jobtype=param_dat["jobtype"]
        param_infile=param_dat["infile"]
        if param_jobtype=="repath" and param_infile!="none":
            dn_infile=fn_abs_top[:-(len(fn_abs_top.split("/")[-1])+1)]

            fn_abs_infile_top="%s/%s" % (dn_infile, param_infile)

            ## Load pt path from the previous job
            ls_pt_json=parser_grrm_pt_path\
                (fn_abs_infile_top, ls_pt_json)

    return ls_pt_json




## --------------------------------------
##   Load PT path file to "pathdata"
## --------------------------------------
def _load_pt_path_file(fname):

    ## initialize
    ls_json=[]

    ## -------------------------
    ## open xxxxx_PTyy.log file
    ## -------------------------
    fdat = open(fname, 'r')
    line = "noneline"
    while line:
        if "# NODE" in line:
            ## NODE 1
            #H         -1.841436690919         -0.497625277033         -1.611523932496
            #B          0.038436920897         -0.199104928808          0.005675481915
            #C         -0.998858163248         -0.399889253745         -0.880521760797
            #P          1.555310029384          0.176016743923          1.089742080984
            #           Item                    Value                Threshold
            #           ENERGY       -404.676496870404                                 (   0.000000000000 :    0.000000000000)
            #           Spin(**2)       0.782801924831
            #           LAMDA          -0.019823842677
            #           TRUST RADII     0.066872571292
            #           STEP RADII      0.066872604923
            #  Maximum  Force           0.079664017830          0.000300000000
            #  RMS      Force           0.053751201519          0.000200000000
            #  Maximum  Displacement    0.013668210620          0.001500000000
            #  RMS      Displacement    0.007239262828          0.001000000000
            #NORMAL MODE EIGENVALUE : N_MODE = 5
            #  0.077826113   0.203289746   0.365227277   0.375676140   0.464381607

            ## get EQ
            t_d=line.split()
            inode_cout=int(t_d[2].replace(":",""))

            t_nam=[]
            t_xyz=[]
            while line:
                line = fdat.readline()
                if "Item"in line\
                   and "Value" in line\
                   and "Threshold" in line:
                    break
                else:
                    t_d=line.split()
                    t_nam.append(t_d[0])
                    t_w=[]
                    t_w.append(float(t_d[1])*unit_ang2au())
                    t_w.append(float(t_d[2])*unit_ang2au())
                    t_w.append(float(t_d[3])*unit_ang2au())
                    t_xyz.append(t_w)

            ## GET ENERGY
            line = fdat.readline() #           ENERGY       -404.676496870404
            t_energy=[]
            if "ENERGY" in line:
                line = line.replace("ENERGY","").replace("(","").replace(":","").replace(")","")
                t_d=line.split()
                if len(t_d) == 1:
                    t_energy=[float(t_d[0])]
                elif len(t_d) == 2:
                    t_energy=[float(t_d[0]), float(t_d[1])]
                elif len(t_d) == 3:
                    t_energy=[float(t_d[0]), float(t_d[1]), float(t_d[2])]
                else:
                    print("SPPR SYSTEM: in parser_grrm_eqlist.py. Energy not found !!")

            line = fdat.readline() #           Spin(**2)       0.782801924831
            t_s2value=float(line.split()[1])
            line = fdat.readline() #           LAMDA          -0.019823842677
            line = fdat.readline() #           TRUST RADII     0.066872571292
            line = fdat.readline() #           STEP RADII      0.066872604923
            line = fdat.readline() #  Maximum  Force           0.079664017830          0.000300000000
            line = fdat.readline() #  RMS      Force           0.053751201519          0.000200000000
            line = fdat.readline() #  Maximum  Displacement    0.013668210620          0.001500000000
            line = fdat.readline() #  RMS      Displacement    0.007239262828          0.001000000000
            line = fdat.readline() #NORMAL MODE EIGENVALUE : N_MODE = 5

            ##  hessian eigen values
            t_eigenvalue=[]
            while 1:
                line = fdat.readline()
                if ""==line.strip():
                    break
                elif "# NODE"==line.strip():
                    break
                else:
                    t_d=line.split()
                    for ielem in range(0, len(t_d)):
                        t_eigenvalue.append(float(t_d[ielem]))

            ## put the last dat into json:
            t_json={}
            t_json["atomname"]=copy.deepcopy(t_nam)
            t_json["xyz"]=copy.deepcopy(t_xyz)
            t_json["comment"]="NODE%d" % (inode_cout)
            t_json["category"]="NODE"
            t_json["symmetry"]=""
            t_json["num"]=inode_cout
            t_json["energy"]=copy.deepcopy(t_energy)
            t_json["s2_value"]=t_s2value
            t_json["hess_eigenvalue_au"]=copy.deepcopy(t_eigenvalue)
            t_json["gradient"]=[]
            t_json["dipole"]=[]

            ## add to list
            ls_json.append(copy.deepcopy(t_json))

        else:
            line = fdat.readline()
    fdat.close()

    return copy.deepcopy(ls_json)

