#!/usr/bin/env python


#===========================================================================#
#                                                                           #
#  File:       setup.py                                                     #
#  Dependence: the whole tool-kit                                           #
#  Usage:      install the files as a lib and generate excutables           #      
#  Author:     Shunhong Zhang <szhang2@ustc.edu.cn>                         #
#  Date:       Nov 22, 2019                                                 #
#                                                                           #
#===========================================================================#


from __future__ import print_function
import os
import sys
import platform
from distutils.core import setup
#from setuptools import setup


def set_path(bin_dirs):
    current_path = os.environ['PATH'].split(os.pathsep)
    for bin_dir in bin_dirs:
        binpath="export PATH=\$PATH:{0}".format(bin_dir)
        print ('\nThe directory containing executive files is:\n{}'.format(bin_dir))
        print (binpath)
        if sys.platform=='linux':
            if bin_dir not in current_path:  
                print ('It has been added to ~/.bashrc')
                print ('Run "source ~/.bashrc" to activate it')
                add_binpath = 'echo "{0}"|cat >>~/.bashrc'.format(binpath)
                os.system(add_binpath)
            else:  
                print ('The utility directory already in the path\n')



def test_modules(module_list,desc,pkg='asd'):
    import importlib
    import glob
    import shutil
    print ( '\n{0}\nTEST: {1}\n{0}'.format('='*50,desc))
    print ( '{0:40s} {1:10s}\n{2}'.format('MODULE','STATUS','-'*50))
    #cwd=os.getcwd()
    #os.chdir(os.path.expanduser("~"))
    for mod in module_list:
        try:
            mod = mod.replace('/','.')
            importlib.import_module(mod)
            print('{0:40s} success'.format(mod))
        except:
            print('{0:40s} failed!'.format(mod))
    print('{0}\n'.format('='*50))
    for item in glob.glob('*pyc'): os.remove(item)
    if os.path.isdir('__pycache__'): shutil.rmtree('__pycache__')



core_modules=[
'QE_ibrav_lib',
'arguments',
'pysupercell',
'__init__',
]

core_modules = ['pysupercell/{}'.format(item) for item in core_modules]



kwargs_setup=dict(
name='PySupercell',
version='0.0.3',
author='Shunhong Zhang',
author_email='zhangshunhong.pku@gmail.com',
url='https://to_be_posted',
download_url='https://on_request',
keywords=['Python','Crystal structure','supercell'],
py_modules=core_modules,
license="MIT License",
description='Python library for creating and manipulating crystal structures',
long_description="A Open-source Python library for playing with crystal structures, such as supercell, dislocation, slab, and nanotube",
platforms=[platform.system()],
install_requires=['numpy','matplotlib','scipy','termcolor'],
)


if __name__=='__main__':
    print ('{0}\nOperating System: {1}'.format('-'*50,platform.system()))

    print ('\n{0}\nINSTALL\n{0}\n'.format('-'*50))
    setup(**kwargs_setup)
    print ('{0}'.format('-'*50))

    with open('pysupercell/__init__.py','w') as fw:
        for key in ['__name__','__version__','__author__','__author_email__','__url__','__license__','__platforms__']:
            print ('{:<20s}  =  "{}"'.format(key,kwargs_setup[key.strip('__')]),file=fw)

    test_modules(core_modules,'core modules')

    cwd = os.getcwd()
    bindirs = [cwd+'/bin']
    set_path(bindirs)
    print ('\n{0}\nDone\n{0}\n'.format('-'*50))
