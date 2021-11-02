from .tools_unit_constant import unit_au2ang

class tools_cntl_xyz_traj:
    
    def __init__(self,fname):
        if ".xyz" in fname:
            self.fname = fname
        else:
            self.fname = fname+".xyz"
        
    def mkxyz_initialize(self):
        fdata=open(self.fname, 'w')
        fdata.close()

    def mkxyz_put_oneGeom(self,atom_name,xyz_mat,comment):
        natoms=len(atom_name)
        fdata=open(self.fname, "a")
        fdata.write("%d\n" % (natoms))
        fdata.write("%s\n" % (comment))
        for iatom in range(0,natoms):
            fdata.write("%2s  %20.14f%20.14f%20.14f\n" % (atom_name[iatom],xyz_mat[iatom][0]*unit_au2ang(),xyz_mat[iatom][1]*unit_au2ang(),xyz_mat[iatom][2]*unit_au2ang()))

        fdata.close()


