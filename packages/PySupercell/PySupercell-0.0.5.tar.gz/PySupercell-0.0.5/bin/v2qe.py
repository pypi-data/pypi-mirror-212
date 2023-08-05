#!/usr/bin/env python

#===========================================================================#
#                                                                           #
#  File:       v2qe.py                                                      #
#  Dependence: pysupercell.py                                               #
#  Usage:      convert the POSCAR file to part of input file for PWscf(QE)  #      
#  Author:     Shunhong Zhang <szhang2@ustc.edu.cn>                         #
#  Date:       Jun 03, 2023                                                 #
#                                                                           #
#===========================================================================#

import sys
import numpy as np
from pysupercell.QE_ibrav_lib import *
from pysupercell import __version__
from pysupercell.pysupercell import cryst_struct
try: from termcolor import cprint,colored
except: pass
import os
import shutil

pyver=sys.version_info[0]

Note='''
This file can be used to generate input file for PWscf (Quantum ESPRESSO) by using VASP-POSCAR as input.
The definition of primitive cell basis vectors follows the Quantum ESPRESSO code, please refer to:
http://www.quantum-espresso.org/wp-content/uploads/Doc/INPUT_PW.html#idm6425376
'''
Usage='''
Usage: Please prepare the POSCAR file in the conventional cell form, use direct (fractional) coordinates to indicate atomic positions.
Then run this script by type the command: python v2qe.py
'''

Alert='''
Caution on the space group and ibrav when dealing with the following systems:
1.  Low dimensional materials: 
    The periodicity in the vacuum direction(s) are inrealistic
    so the 'spacegroup' may be wrong.
2.  Magnetic materials: 
    The spin polarization may adds extra properties to the atoms, 
    so the magnetic unit cell may differs from the chemical primitive cell.
3.  Body/Face/Base-centered structures: 
    The choice of the base plane is alternative, 
    please check the generated structure carefully using xcrysden.
'''

conv_cell_prompt='''
this is a structure with face/body/base-centered symmetry
The POSCAR you provide is a primitive cell
use phonopy to generate BPOSCAR which is a conventional cell
and then try again
good luck!
'''

def standardize_poscar(ibrav,spg,poscar='POSCAR'):
    struct = cryst_struct.load_poscar(poscar)
    sc=np.eye(3)
    if abs(ibrav)==9 and spg.split()[0]=="A": 
        sc=sc[[1,2,0]]
    elif ibrav in [2,3,11,13]:
        latt_param = struct.latt_param()
        if latt_param['alpha']!=90 or latt_param['beta']!=90 or latt_param['gamma']!=90:
            if os.path.isfile('BPOSCAR'): 
                struct = cryst_struct.load_poscar('BPOSCAR')
                print ('use BPOSCAR generated from phonopy')
            else:
                exit (conv_cell_prompt)
        if ibrav == 13:
            print ('note: the unit cell is reoriented so that')
            print ('C (spanned by a and b) is the base plane, and gamma is the non-right angle')
            sc=np.array(([[1,0,0],[0,0,1],[0,-1,0]]),float)   # switch b and c

    struct_std = struct.build_supercell(sc)
    struct_std._system=system='standardized poscar'
    struct_std.write_poscar_head(filename='POSCAR_standardized')
    struct_std.write_poscar_atoms(filename='POSCAR_standardized',mode='a')
    return struct_std


def gen_pw_nml(args,struct):
    ibrav = struct._get_ibrav()[0]
    pw_nml={}
    control_nml={
    'calculations':args.calculation,
    'restart_mode':'from_scratch',
    'outdir': args.outdir,
    'pseudo_dir': args.pseudo_dir,
    'prefix':args.prefix,
    'tprnfor':False}
    system_nml={
    'ibrav':ibrav}
    #'celldm':struct._find_celldm(ibrav)
    #}
    pw_nml.setdefault('CONTROL',control_nml)
    pw_nml.setdefault('SYSTEM',system_nml)
    return pw_nml



#============================================================#
# input file for quantum ESPRESSO (only for SCF calculation) #
#============================================================#


def write_pwi_nml(pwi_nml,fil='rx.in'):
    import f90nml
    with open(fil,'w') as fw:
       f90nml.write(pwi_nml,fw) 


def write_pwi(setup_dic,ibrav,struct_std,struct,filename="rx.in"):
    # important change: use cell of conventional cell, natom of primitive cell
    struct_std._natom = struct._natom
    
    try:
        import phonopy.structure.atoms as atoms
        atomic_mass=[atoms.atom_data[atoms.symbol_map[sym]][-1] for sym in struct._species]
    except:
        print ('Fail to load atomic mass from phonopy, atomic mass will be displayed as -1')
        atomic_mass = -np.ones(struct._natom)
 
    if filename:
       filename=open(filename,"w")
    print ("&CONTROL", file=filename)
    print ("calculation = ","'vc-relax'", file=filename)
    print ("restart_mode = ","'from_scratch'", file=filename)
    print ("outdir = './tmp/'", file=filename)
    print ("pseudo_dir = ",setup_dic['pseudo_dir'], file=filename)
    print ("prefix = '{0}'".format(setup_dic['prefix']), file=filename)
    print ('tprnfor=.true.',file=filename)
    print ('tstress=.true.',file=filename)
    print ('etot_conv_thr=1.d-12',file=filename)
    print ('forc_conv_thr=1.d-8',file=filename)
    print ("/", file=filename)
    print ("&SYSTEM", file=filename)
    struct_std.write_pw_cell(filename=filename)
    print ("ecutwfc = ",setup_dic['ecutwfc'], file=filename)
    print ("ecutrho = ",setup_dic['ecutrho'], file=filename)
    print ("occupations = 'smearing'", file=filename)
    print ("smearing ='gaussian'", file=filename)
    print ("degauss = 0.001", file=filename)
    print ("/", file=filename)
    print ("&ELECTRONS", file=filename)
    print ("conv_thr=1.d-8", file=filename)
    print ("/", file=filename)
    print ('&IONS',file=filename)
    print ('/',file=filename)
    print ('&CELL',file=filename)
    print ("cell_dofree='2Dxy'",file=filename)
    print ('press_conv_thr=1.d-1',file=filename)
    print ('/',file=filename)
    if ibrav==0:
       print ('CELL_PARAMETERS angstrom', file=filename)
       print ('\n'.join([' '.join(['{0:15.10f}'.format(struct._cell[i,j]) for j in range(3)]) for i in range(3)]), file=filename)



def get_args():
    import argparse
    parser = argparse.ArgumentParser(prog='v2qe.py', description = Note)
    parser.add_argument('--poscar',type=str,default='POSCAR',help='name of the POSCAR file')
    parser.add_argument('--symmprec', type=float, default=5e-4, help='deviation tolerance for finding crystal symmetry, in angstrom')
    parser.add_argument('--ecutwfc', type=float, default=100, help='plane wave cutoff')
    parser.add_argument('--ecutrho', type=float, default=500, help='charge density cutoff')
    parser.add_argument('--calculation',type=str,default="'vc-relax'",help="calculation task of QE")
    parser.add_argument('--outdir',type=str,default="'./tmp'",help="directory for temporary files")
    parser.add_argument('--prefix', type=str, default="pw", help='prefix for the pw calculation')
    parser.add_argument('--pseudo_dir',type=str,default="'/home/zsh/pseudo/pbe'",help="directory for pseudopotential files")
    parser.add_argument('--upf',    type=str, default=".pbe-mt_fhi.UPF",help="type of pseudopotentail")
    parser.add_argument('--kmesh', type=str, default='auto', help='k point mesh using the Monkhorst Pack scheme')
    parser.add_argument('--kshift', type=str, default="0 0 0", help='k point mesh shift from the Gamma point')
    args=   parser.parse_args()
    return parser, args


def main():
    print ('\nrunning the script {0}\n'.format(__file__.lstrip('./')))
    try:
        from termcolor import cprint
        cprint(Note,'cyan')
        cprint(Usage,'blue')
        cprint(Alert,"red")
        cprint(def_ibrav,'green')
    except:
        print ('{0}\n{1}\n{2}\n{3}'.format(Note,Usage,Alert,def_ibrav))
    parser, args=get_args()

    print ('VASP sutructure from {}'.format(args.poscar))
    struct = cryst_struct.load_poscar(args.poscar)
    if args.kmesh=='auto': kgrid = ('{:3d} '*3).format(*tuple(struct.get_kmesh(0.02)))
    else: kgrid=args.kmesh

    pw_setup_dic={ "prefix" : args.prefix,
                   "ecutwfc": args.ecutwfc,
                   "ecutrho": args.ecutrho,
                "pseudo_dir": args.pseudo_dir,
                   "upf"    : args.upf,
                   "kmesh"  : kgrid,
                   "kshift" : args.kshift}

    kwargs = dict(symmprec=args.symmprec,report=True)
    spg, spg_no = struct.find_symmetry(**kwargs)
    ibrav,brav,center = struct.get_ibrav(symmprec=args.symmprec)

    redef_note="\nDo you want to define ibrav manually?(n/y, default: n)\n"
    try: redef=colored(redef_note,"red")
    except: redef=redef_note
    if pyver==2: ldef=raw_input(redef)
    else: ldef=input(redef)
    if ldef=="y": ibrav=input(colored("ibrav = ","red"))
    ibrav=int(ibrav)

    connect=get_connect(ibrav,spg,struct.latt_param())
    print ( "connect matrix\n")
    print ((('{:7.4f} '*3+'\n')*3+'\n').format(*tuple(connect.flatten())))

    standardize_poscar(ibrav,spg,poscar=args.poscar)
    struct_std = cryst_struct.load_poscar('POSCAR_standardized')
    if ldef=='y':struct_std=struct
    celldm=struct_std.find_celldm(ibrav=ibrav)
    print ("Lattice Parameters of standardized POSCAR:")
    struct_std.print_latt_param()
    
    struct_pm = struct_std.build_supercell(connect)
    struct_pm._system='primitive cell'
    struct_pm.write_poscar_head(filename="POSCAR_Primitive")
    struct_pm.write_poscar_atoms(filename="POSCAR_Primitive",mode='a')

    print ("\n{0}\nSample input for PWscf(Quantum ESPRESSO),Start\n{0}\n".format('-'*60))
    write_pwi(pw_setup_dic,ibrav,struct_std,struct_pm,filename=None)
    write_pwi(pw_setup_dic,ibrav,struct_std,struct_pm,filename="rx.in")
    print ("\n{0}\nSample input for PWscf(Quantum ESPRESSO),End\n{0}\n".format('-'*60))
    #struct._visualize_struct()

    for file in ['BPOSCAR','PPOSCAR','phonopy_symm.yaml','POSCAR_standardized','POSCAR_for_symm_analysis']:
        if os.path.isfile(file): os.remove(file)



desc_str = 'Convert POSCAR into QE pwscf input'

if __name__=='__main__':
    try:
        from pyfiglet import Figlet
        f = Figlet()
        pysc_text = f.renderText('PySupercell')
        print (pysc_text)
    except:
        pass

    print ('{:>53s}'.format('version {}\n'.format(__version__)))
    try: cprint (desc_str,'green')
    except: print (desc_str)

    main()
