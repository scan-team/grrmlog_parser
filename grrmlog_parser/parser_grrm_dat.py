import os
import copy
import glob
from tqdm.auto import trange
from .tools_unit_constant import unit_ang2au, unit_au2ang
from .parser_grrm_param         import parser_grrm_param

def parser_grrm_dat(fname):

    tmp_fn_list=glob.glob("%s_P*.dat" % (fname))
    tmp_fn_list.sort()

    ## ---------------
    ##  get list dat
    ## ---------------
    out_list=[]
    count_id=0
    for ifn in trange(0, len(tmp_fn_list), unit='file'):
        t_num=tmp_fn_list[ifn][len(fname)+2:-4]
        if t_num.isnumeric():
            tmp_dat,count_id\
                =_load_dat_file(tmp_fn_list[ifn], count_id)

            for idat in range(0,len(tmp_dat)):
                out_list.append(copy.deepcopy(tmp_dat[idat]))

            del tmp_dat

    if len(out_list) > 0:
        return out_list


    ## -------------------------
    ## Find infile jobs
    ## -------------------------
    fn_param_rrm="%s_PARAM.rrm" % (fname)
    param_infile="none"
    param_jobtype="none"
    if os.path.exists(fn_param_rrm):
        ## get the infile information
        param_dat=parser_grrm_param(fn_param_rrm)
        param_jobtype=param_dat["jobtype"]
        param_infile=param_dat["infile"]
        if param_jobtype=="repath" and param_infile!="none":

            dn_infile=fname[:-(len(fname.split("/")[-1])+1)]

            fn_abs_infile_top="%s/%s" % (dn_infile, param_infile)

            ## Load pt path from the previous job
            out_list=parser_grrm_dat(fn_abs_infile_top)


    return out_list


def _load_dat_file(fn_abs_dat, count_id):

    ls_dat=[]

    fdat = open(fn_abs_dat, 'r')
    ieq_cout=-1
    tag_first_eq=0
    line = True
    while line:

        line = fdat.readline()

        #RESULTS
        #CURRENT COORDINATE
        #H         -1.696741879408         -0.381991249860         -0.776848274818
        #B          0.778532341016         -0.368262935046         -0.940077243633
        #C         -0.644739894670         -0.303723056303         -0.550973655507
        #P          0.316401529176          0.133374525555          0.871271043561
        #ENERGY = -404.733252292855    0.000000000000    0.000000000000
        #       =    0.000000000000    0.000000000000    0.000000000000
        #S**2   =    0.756508849780
        #GRADIENT
        #   0.003235547110
        #   0.000410425111
        #  -0.001175093180
        #   0.015696975400
        #  -0.006641569140
        #  -0.026453248300
        #  -0.026122430400
        #  -0.006014107450
        #  -0.013792948200
        #   0.007189907880
        #   0.012245251500
        #   0.041421289600
        #DIPOLE =   -0.422221604000    0.027694074600    0.118443339000

        if "CURRENT COORDINATE" in line:
            ## put the last dat into json:
            t_json={}
            t_xyz=[]
            while line:
                line = fdat.readline()

                if "ENERGY" in line:
                    break
                else:
                    t_d=line.split()
                    t_w=[]
                    t_w.append(float(t_d[1])*unit_ang2au())
                    t_w.append(float(t_d[2])*unit_ang2au())
                    t_w.append(float(t_d[3])*unit_ang2au())
                    t_xyz.append(t_w)

            ## Load Energy
            t_ene=[]
            t_ene.append(float(line.split()[2]))
            t_ene.append(float(line.split()[3]))
            t_ene.append(float(line.split()[4]))
            line = fdat.readline()
            t_ene.append(float(line.split()[1]))
            t_ene.append(float(line.split()[2]))

            ## Load S^2 value
            line = fdat.readline() #S**2   =    0.756508849780
            t_s2v=float(line.split()[2])

            ## Load Gradient
            natoms=len(t_xyz)
            line = fdat.readline() #GRADIENT
            t_grad=[]
            for iatom in  range(0, natoms):
                work=[]
                for idim in range(0,3):
                    line = fdat.readline()
                    work.append(float(line))
                t_grad.append(work)

            ## Load DIPOLE
            line = fdat.readline() #DIPOLE =   -0.422221604000    0.027694074600    0.118443339000
            t_dipol=[]
            t_dipol.append(float(line.split()[2]))
            t_dipol.append(float(line.split()[3]))
            t_dipol.append(float(line.split()[4]))

            ## save into the lib
            t_json["category"]="DAT"
            t_json["symmetry"]=""
            t_json["num"]=count_id
            t_json["xyz"]=copy.deepcopy(t_xyz)
            t_json["energy"]=copy.deepcopy(t_ene)
            t_json["gradient"]=copy.deepcopy(t_grad)
            t_json["s2_value"]=t_s2v
            t_json["dipole"]=copy.deepcopy(t_dipol)
            t_json["atomname"]=[]
            t_json["hess_eigenvalue_au"]=[]
            ieq_cout=ieq_cout+1
            t_json["comment"]="NODE%d" % (ieq_cout)

            ## add to list and count up
            count_id=count_id+1
            ls_dat.append(t_json)
    fdat.close()

    return ls_dat, count_id

