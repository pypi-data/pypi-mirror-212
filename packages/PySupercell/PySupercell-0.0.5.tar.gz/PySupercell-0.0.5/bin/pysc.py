#!/usr/bin/env python


#==============================================================#
#                                                              #
#  File:       pysc.py                                         #
#  Usage:      define a class for crystal structures           #      
#  Author:     Shunhong Zhang <szhang2@ustc.edu.cn>            #
#  Date:       Jun 03, 2023                                    #
#                                                              #
#==============================================================#


import os
import numpy as np
import warnings
import itertools
import copy 
from pysupercell import __version__
from pysupercell.pysupercell import *
from pysupercell.arguments import str2bool, add_control_arguments, add_io_arguments, add_structure_arguments
 
try:
    from termcolor import cprint
    color_print=True
except:
    color_print=False


def get_args(desc_str):
    import argparse
    parser = argparse.ArgumentParser(prog='pysupercell', description = desc_str)
    add_control_arguments(parser)
    add_io_arguments(parser)
    add_structure_arguments(parser)
    parser.add_argument('--upf',    type=str, default=".pbe-mt_fhi.UPF",help="type of pseudopotentail")
    parser.add_argument('--strain',type=eval,default=0,help='magnitude of strain')
    parser.add_argument('--strain_dirs',type=eval,default=None,help='directions for strain, along crystal axes')
    parser.add_argument('--angle',type=float,default=0,help='angle to rotate the crystal axes')
    parser.add_argument('--symmprec',type=float,default=1E-4,help='accuracy to find crystal symmetry in Angstrom')
    parser.add_argument('--case',type=str,default='case',help='case name for wien2k input')
    parser.add_argument('--kgrid',type=float,default=0.02,help='density of kgrid, in unit of 2pi/Angs')
    parser.add_argument('--idir_shift',type=int,default=2,help='latt vector index, for shifting')
    parser.add_argument('--shift',type=float,default=1,help='atom shift distance along certain direction')
    args = parser.parse_args()
    return parser, args


def cmp_struct(poscar1,poscar2):
    print ('\ncomparing two structures\n{0}'.format('-'*60))
    print ('Structure 1 from file {}'.format(poscar1))
    print ('Structure 2 from file {}'.format(poscar2))

    assert os.path.isfile(poscar1) and os.path.isfile(poscar2),'cannot find {0} or {1}'.format(poscar1,poscar2)
    struct_1=cryst_struct.load_poscar(poscar1)
    struct_2=cryst_struct.load_poscar(poscar2)
    assert struct_1._natom==struct_2._natom,'numbers of atoms in the two structures are different'
    nat = struct_1._natom
    diff=np.zeros(nat)
    print (('{:4s} '*3+'{:>8s} '*4).format('idx','st1','st2','dist (Ang)','dx','dy','dz'))
    Rvecs = gen_Rvecs()
    for iat in range(nat):
        images = np.dot(struct_2._pos[iat]+Rvecs,struct_2._cell)
        norms = np.linalg.norm(struct_1._pos_cart[iat]-images,axis=1)
        diff[iat]=np.min(norms)
        idx = np.where(norms==np.min(norms))[0][0]
        print (' {:<4d} {:4s} {:4s} '.format(iat+1,struct_1._symbols[iat],struct_2._symbols[iat]),end=' ')
        print (('{:8.4f} '*4).format(diff[iat],*tuple(struct_1._pos_cart[iat] - images[idx])))
    print ('{0}'.format('-'*60))
    print ('{0:14s}'.format('Total dist : ')+'   {:8.4f}'.format(np.sum(diff)))
    print ('{0:14s}'.format('Max   dist : ')+'   {:8.4f}\n'.format(np.max(diff)))
    return diff


task_list=[
'crystal_info',
'redefine',
'slab',
'tube',
'strain',
'bond',
'rotate_z',
'kmesh',
'reset_vacuum',
'bending',
'screw_dislocation',
'wien',
'write_pw',
'None',
]



desc_str='''
input exmaple:
    {0}
    {0} --task=redefine --sc1=1,-1,0 --sc2=1,1,0 sc3=0,0,1
    {0} --task=slab --hkl=121
    {0} --task=tube --chiral_num=2,4
    {0} --task=bond --atom_index=0,1
    {0} --task=wien
    {0} --task=crystal_info
    {0} --task=cmp --poscar1=POSCAR --poscar2=CONTCAR
    {0} --task=strain --dirs=0,1 --strain=0.01
    {0} --task=kmesh
    {0} --task=bending --nn=8 --idir_per=1 --idir_bend=2
    {0} --task=shift --idir_shift=2 --shift=10
    {0} --task=screw_dislocation --burgers_vector=[0,0,1] --screw_idir=2 --display_structure=True
'''.format(__file__.split('/')[-1])



def main(task_list,desc_str):
    parser, args = get_args(desc_str)

    if args.source=='VASP':
        struct = cryst_struct.load_poscar(args.poscar)
    elif args.source=='QE':
        struct = cryst_struct.load_pwscf_in(args.filpw)
    elif args.source=='cif':
        struct = cryst_struct.load_cif(args.filcif)

    if args.task==None: 
        pass

    elif args.task=='crystal_info': 
        struct.verbose_crystal_info()

    elif args.task=='redefine':
        filpos = 'POSCAR_redefine'
        redef_struct = struct.redefine_lattice(args.sc1,args.sc2,args.sc3,args.cell_orientation)
        redef_struct.write_poscar_head(filename=filpos)
        redef_struct.write_poscar_atoms(filename=filpos,mode='a')

    elif args.task=='reset_vacuum':
        redef_struct=copy.copy(struct)
        redef_struct._cell[2,2]=args.vacuum
        central_z = np.average(redef_struct._pos_cart[:,2])
        redef_struct._pos_cart[:,2] -= central_z + redef_struct._cell[2,2]/2
        redef_struct._pos=np.dot(redef_struct._pos_cart,np.linalg.inv(redef_struct._cell))
        redef_struct.shift_atoms_to_home()
        flpos='POSCAR_reset_vacuum'
        redef_struct.write_poscar_head(filename=flpos)
        redef_struct.write_poscar_atoms(filename=flpos,mode='a')
        
    elif args.task=='rotate_z':
        a=struct.latt_param()['a']
        b=struct.latt_param()['b']
        gamma=struct.latt_param()['gamma']
        cell_1=[a*cos((args.angle)/180*np.pi),a*np.sin((args.angle)/180*np.pi),0]
        cell_2=[b*cos((gamma+args.angle)/180*np.pi),b*np.sin((gamma+args.angle)/180*np.pi),0]
        struct._cell=np.array([cell_1,cell_2,struct._cell[2]])
        struct._system='POSCAR_rotate_z'
        struct.write_poscar_head(filename=flpos)
        struct.write_poscar_atoms(filename=flpos,mode='add')

    elif args.task=='slab':
        hkl=args.hkl
        if len(hkl)>3:
            exit('we do not allow negative index!')
        h,k,l=list(map(int,hkl))
        struct_slab = struct.build_slab(h,k,l,args.thickness,args.vacuum,args.atom_shift)
        struct_slab._system='slab'
        struct_slab.write_poscar_head(filename=flpos)
        struct_slab.write_poscar_atoms(filename=flpos,mode='a')

    elif args.task=='tube':
        n,m=args.chiral_num
        struct_tube = struct.build_tube(n,m,negative_R=args.negative_R)
        fltube = "POSCAR_tube_{0}_{1}".format(n,m)
        struct_tube._system=system='{0}_{1}_nanotube'.format(n,m)
        struct_tube.write_poscar_head(filename=flpos)
        struct_tube.write_poscar_atoms(filename=flpos,mode='a')

    elif args.task=='bending':
        struct_bend = struct.build_bending_supercell(args.nn,args.amp,args.idir_per,args.idir_bend,args.central_z)
        struct_bend._system = 'bending struct'
        struct_bend.write_poscar_head(filename=flpos)
        struct_bend.write_poscar_atoms(filename=flpos,mode='a')

    elif args.task=='strain':
        for idir in args.strain_dirs:
            struct._cell[idir] *= 1+args.strain
        struct._pos_cart=np.dot(struct._pos,struct._cell)
        filpos='POSCAR_{0:5.3f}'.format(args.strain)
        struct.write_poscar_head(filename=filpos)
        struct.write_poscar_atoms(filename=filpos)

    elif args.task=='shift':        
        struct.shift_pos(args.idir_shift,args.shift,to_home=False)
        filpos='POSCAR_shifted'
        struct.write_poscar_head(filename=filpos)
        struct.write_poscar_atoms(filename=filpos)

    elif args.task=='bond':
        i,j=args.atom_index
        cc=np.append(0,np.cumsum(struct._counts))
        ic=i-cc[np.where(i-cc>=0)[0][-1]]+1
        jc=j-cc[np.where(j-cc>=0)[0][-1]]+1
        print ('\n{0}\natomic positions in the home cell\n{0}'.format('-'*80))
        print ('symbol  atom '+('{:>10s} '*6).format('x','y','z','x_cart','y_cart','z_cart'))
        for ii,jj in zip((i,j),(ic,jc)):
            print ('{:>6s} {:5d} '.format(struct._symbols[ii],jj),end='')
            print (' '.join(['{:10.5f}'.format(item) for item in np.append(struct._pos[ii],struct._pos_cart[ii])]))
        print ( '-'*80)
        output='min distance between {}{} and {}{} is: {:8.5f} Angstrom'
        print (output.format(struct._symbols[i],ic,struct._symbols[j],jc,struct.bond_length(i,j)))

    elif args.task=='screw_dislocation':
        burgers_vector = np.dot(args.burgers_vector,struct._cell)
        struct_screw = struct.make_screw_dislocation(burgers_vector,args.screw_center,args.screw_normal,args.screw_idir)
        struct_screw._system = 'screw dislocation structure'
        struct_screw.write_poscar_head(filename='POSCAR_screw')
        struct_screw.write_poscar_atoms(filename='POSCAR_screw',mode='a')
        if args.display_structure: map_data(struct_screw._cell,struct_screw._pos)

    elif args.task=='Select_Dynamics' or args.task=='SD':
        struct.write_poscar_head(filename='POSCAR_sd')
        struct.write_poscar_atoms(selective_dynamics=True,fix_dirs=args.dirs,filename='POSCAR_sd')

    elif args.task=='wien':         
        struct.write_wien2k_struct(args.case,symmprec=args.symmprec)

    elif args.task=='write_pw':
        struct.write_pw_cell()
        struct.write_pw_atoms()

    elif args.task=='cmp':        
        cmp_struct(args.poscar1,args.poscar2)

    elif args.task=='kmesh':
        struct.writekp(args.kgrid)

    else:
        print ('\n{}\navailable tasks:'.format('-'*30))
        print ('\n'.join([task for task in task_list])+'\n{0}'.format('-'*30))


if __name__=='__main__':
    try:
        from pyfiglet import Figlet
        f = Figlet()
        pysc_text = f.renderText('PySupercell')
        print (pysc_text)
    except:
        print ('\nRunning the script: {0}\n'.format(__file__.lstrip('./')))

    print ('{:>53s}'.format('version {}\n'.format(__version__)))
    if color_print: cprint (desc_str,'green')
    else: print (desc_str)


    main(task_list,desc_str)
