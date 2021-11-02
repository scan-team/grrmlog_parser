"""
class for the grrm-map log load.
"""

class GRRMMap:

    def __init__(self):

        """
        eq_list: EQ_list.log
        ts_list: TS_list.log
        pt_list: PT_list.log
        dc_list: DC_list.log
        goem_list: just keep all the xyz geometry on the map with gradient

        xyz geometries : in [bohr = a.u]
        initxyz : molecular geometry xyz in input [xxx.com]
        natoms : number of atoms natoms=len(initxyz)=len(atom_name)
        atom_name : vec=["H","H","C","C","C"....] natoms elements
        spinmulti : spin multiplicity
        totalcharge : charge of molecule
        fname_top_abs : absolute path of the file without .com
        fname_top_rel : relative path of the file without .com
        lowest_energy : lowest energy in EQ_list.log
        highest_energy : highest energy in PT_list.log or TS_list.log
        neq : the number of geometries in EQ_list.log
        nts : the number of geometries in TS_list.log
        npt : the number of geometries in PT_list.log
        jobtime : time stamp of PARAM.rrm file
        universal_gamma : universal force for GRRM search
        infile : infile is the GRRM included file
        scpathpara : SC paths can be separated using this option.
        jobtype : min, saddle, mc-afir, sc-afir, repath, restruct
        pathtype : PT or IRC
        nobondrearrange : only search the geometries have same bonding pattern
        siml_temperature_kelvin : temperature of the kinetic simulation
        siml_pressure_atm : pressure of the kinetic simulation
        energyshiftvalue_au : pressure of the kinetic simulation
        level : electronic structure calculation level
        """

        ## list of hash
        self.eq_list = []
        self.pt_list = []
        self.ts_list = []
        self.dc_list = []
        self.geom_list = []

        ## normal data
        self.atom_name = []
        self.initxyz = []
        self.initpart = []
        self.fname_top_abs="none"
        self.fname_top_rel="none"
        self.natoms=0
        self.lowest_energy=0.0
        self.highest_energy=0.0
        self.neq=0
        self.nts=0
        self.npt=0
        self.jobtime="none"
        self.universal_gamma=0.0
        self.infile="none"
        self.scpathpara="none"
        self.jobtype="none"
        self.pathtype="none"
        self.nobondrearrange=0  ## 0: OFF, 1: ON
        self.siml_temperature_kelvin=[]
        self.siml_pressure_atm=1.0
        self.energyshiftvalue_au=0.0
        self.level="none"
        self.spinmulti=1
        self.totalcharge=0
        self.jobstatus="none"
        self.jobmessage="none"
        self.ngradient=-1
        self.nhessian=-1
        self.elapsedtime_sec=0.0


class EQ:
    def __init__(self, id):

        """
        EQ : list of hash for EQ

        xyz : molecular geometry 3d-xyz
        xyz geometries : in [bohr = a.u]
        gradient : get from xxxx.dat file (normally empty)
        self.category : EQ TS PT DC
        self.energy:
            list
                energy in hartree = a.u.
                energy[0] is electronic energy
        self.gradient:
            list
                2 dimension : natom * 3
                gradient in hartree = a.u.
                Data is attributed by comparing all list files
                and xxxx.dat file. When s2_value is different
                gradient becomes empty, [].
        self.dipole:
            list
                dipole in hartree = debye
                Data is attributed by comparing all list files
                and xxxx.dat file. When s2_value is different
                gradient becomes empty, [].
        self.symmetry:
            computed by GRRM
        self.comment :
        self.hess_eigenvalue_au:
            list
                2 dimension : 3*natom * 3*natom
                Hessian eigen value
        self.trafficvolume:
            list
                1 dimension : 3 elements (number of temperatures)
                in self.siml_temperature_kelvin
                In Trafic Volume for TrafficVolCheck or RetroSynth
        self.population:
            list
                1 dimension : 3 elements (number of temperatures)
                in self.siml_temperature_kelvin
                Population for TrafficVolCheck
                value should be 0.0 ~ 1.0
        self.reactionyield:
            list
                1 dimension : 3 elements (number of temperature)
                contribution ratio (reaction yield) for RetroSynth
                value should be 0.0 ~ 1.0

        """

        self.id = id
        self.category = ""
        self.symmetry = ""
        self.comment = ""
        self.xyz = []
        self.energy = []
        self.gradient = []
        self.s2_value = 0.0
        self.dipole = []
        self.hess_eigenvalue_au = []
        self.trafficvolume = [None,None,None]
        self.population = [None,None,None]
        self.reactionyield = [None,None,None]


class Edge:
    def __init__(self, id):
        """
        Edge : list of hash for TS, PT

        xyz : molecular geometry 3d-xyz
        xyz geometries : in [bohr = a.u]
        gradient : get from xxxx.dat file (normally empty)
        self.category : EQ TS PT DC
        self.energy:
            list
                energy in hartree = a.u.
                energy[0] is electronic energy
        self.energy:
            list
                energy in hartree = a.u.
                energy[0] is electronic energy
        self.symmetry : computed by GRRM
        self.comment :
        self.hess_eigenvalue_au : Hessian eigen value
        self.connection: -1:error, the other is for EQ number EQxx
        self.pathdata:
        pathdata is for geometries between EQ-TS(PT)-EQ
        there should be several geometries along the path.
        the geometries are indicated by NODE0-NODEx
        each NODE has the information of EQ(python object)
        """
        self.id = id
        self.category = ""
        self.symmetry = ""
        self.comment = ""
        self.xyz = []
        self.gradient = []
        self.energy = []
        self.s2_value = 0.0
        self.dipole = []
        self.hess_eigenvalue_au = []
        self.pathdata = []
        self.connection = []

