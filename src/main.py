#!/usr/bin/env python3

#! NXP Manager
#! Made by hithja
#! Under ... License

import tarfile
import toml
import sys
import os
import print_color as pc
import shutil
from errors import *
from utils import *

config = {}
with open('conf.toml', 'r') as f:
    config = toml.loads(f.read())

def unpack(package_name):
    try:
        file = tarfile.open(f'{package_name}.nxp') 

        file.extractall(config['path']['cache'], filter='data') 
        file.close()
    except:
        catch_err(10)

    pc.print('Unpacking app...')
    info_file = {}
    
    try:
        with open(f'{config['path']['cache']}/{package_name}/meta.toml', 'r') as file:
            info_file_loaded = file.read()
            info_file = toml.loads(info_file_loaded)
        pc.print(f'{info_file['name']} v{info_file['version']} unpacked!', tag='success', tag_color='green', color='white')

        print("Binaries: ")
        for i in os.listdir(f'{config['path']['cache']}/{package_name}/bin'):
            print('\t- ' + i + ' > ' + get_size(f'{config['path']['cache']}/{package_name}/bin'))
        
        if (info_file['dep']): 
            print("Dependencies: ")
            for i in info_file['dep']:
                if i:
                    print('\t- ' + i)

        yn = input(f'\033[33m[?]\033[0m Do you want to install {package_name} [Y/n]: ')
        if str(yn).lower() == 'y':
            install(package_name)
        else:
            shutil.rmtree(f'{config['path']['cache']}/{package_name}')
    except:
        catch_err(11)

def install(pkg):
    bins = []
    for i in os.listdir(f'{config['path']['cache']}/{pkg}/bin'):
        bins.append(i)
        shutil.copyfile(f'{config['path']['cache']}/{pkg}/bin/{i}', f'{config['path']['bin']}/{i}')
    
    try:
        with open(f'{config['path']['cache']}/{pkg}/meta.toml', 'r') as file:
            info_file_loaded = file.read()
            info_file = toml.loads(info_file_loaded)

            pkg_info = {}
            try:
                with open(f'{config['path']['nxpi']}', 'r') as f:
                    packages = f.read()
                    pkg_info = toml.loads(packages)
            except:
                catch_err(21)
            pkg_info.update({f'{info_file['name']}': {'version': f'{info_file['version']}', 'author': f'{info_file['author']}', 'binaries': bins}})
            with open(f'{config['path']['nxpi']}', 'w') as f:
                toml.dump(pkg_info, f)
    except:
        catch_err(20)

    shutil.rmtree(f'{config['path']['cache']}/{pkg}')
    pc.print('Installed!', tag='success', tag_color='green', color='white')

def list_pkg():
    pkg_info = {}
    try:
        with open(f'{config['path']['nxpi']}', 'r') as f:
            packages = f.read()
            pkg_info = toml.loads(packages)
    except:
        catch_err(30)
    
    for i in pkg_info:
        print(f'Package: {i}\tVersion: {pkg_info[i]['version']}\tAuthor: {pkg_info[i]['author']}')
    
def remove(pkg):
    pkg_info = {}
    try:
        with open(f'{config['path']['nxpi']}', 'r') as f:
            packages = f.read()
            pkg_info = toml.loads(packages)
    except:
        catch_err(40)

    print('Binaries to delete: ')
    for i in pkg_info[pkg]['binaries']:
        print(f'\t- {i}')
    
    delete = input(f'\033[33m[?]\033[0m Do you want to delete this binaries [Y/n]: ')
    for i in pkg_info[pkg]['binaries']:
        if delete.lower() == 'y':
            try:
                os.remove(f'{config['path']['bin']}/{i}')
            except:
                print('Nothing to delete!')
                exit()
    try:
        del pkg_info[pkg]
        with open(f'{config['path']['nxpi']}', 'w') as f:
            toml.dump(pkg_info, f)
    except:
        catch_err(41)
    
    pc.print(f'{pkg} was deleted!', tag='success', tag_color='green', color='white')

if __name__ == '__main__':
    if sys.argv[1] == '-i':
        if len(sys.argv[2]) > 0:
            unpack(sys.argv[2])
    elif sys.argv[1] == '-r':
        if len(sys.argv[2]) > 0:
            remove(sys.argv[2])
    elif sys.argv[1] == '-l':
        list_pkg()