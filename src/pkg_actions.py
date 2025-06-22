import toml
import sys
import os
import print_color as pc
import shutil
import stat
import lua_lib
from settings import *
from errors import *
from utils import *

def install(pkg):
    info_file = get_pkg_meta(pkg)

    print("Binaries: ")
    for i in os.listdir(f'{config['path']['cache']}/{pkg}/bin'):
        print('\t- ' + i + ' > ' + get_size(f'{config['path']['cache']}/{pkg}/bin/{i}'))
        
    if (info_file['dep']): 
        print("Dependencies: ")
        for i in info_file['dep']:
            if i:
                print('\t- ' + i)

    yn = input(f'\033[33m[?]\033[0m Do you want to install {pkg} [Y/n]: ')
    if str(yn).lower() == 'y':
        bins = []
        for i in os.listdir(f'{config['path']['cache']}/{pkg}/bin'):
            bins.append(i)
            shutil.copyfile(f'{config['path']['cache']}/{pkg}/bin/{i}', f'{config['path']['bin']}/{i}')
            st = os.stat(f'{config['path']['bin']}/{i}')
            os.chmod(f'{config['path']['bin']}/{i}', st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    
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
                pkg_info.update({f'{info_file['name']}': {'version': f'{info_file['version']}', 'author': f'{info_file['author']}', 'binaries': bins, 'scripts': []}})
                with open(f'{config['path']['nxpi']}', 'w') as f:
                    toml.dump(pkg_info, f)
        except:
            catch_err(20)

        pc.print('Installed!', tag='success', tag_color='green', color='white')
    else:
        pass
    shutil.rmtree(f'{config['path']['cache']}/{pkg}')
    
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
        print(f'\t- {i} > {get_size(f'{config['path']['bin']}/{i}')}')
    
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

def info(pkg):
    info_file = get_pkg_meta(pkg)
    print(f'+=== \033[1m{info_file['name']}\033[0m ===+')
    print(f'Version: {info_file['version']}')
    print(f'Author: {info_file['author']}')
    shutil.rmtree(f'{config['path']['cache']}/{pkg}')