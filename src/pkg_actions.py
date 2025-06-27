import toml
import os
import print_color as pc
import shutil
import stat
import lua_lib
import requests
import sys
import subprocess
import urllib.request
from settings import *
from errors import *
from utils import *

def install(pkg):
    if pkg.endswith('.nxp'):
        info_file = get_pkg_meta(pkg)
        pkg = "".join(pkg.split(".nxp"))

        if len(os.listdir(f'{os.path.expanduser(f'{config['path']['conf-folder']}/{config['path']['cache']}')}/{pkg}/scripts/')) > 0:
            for i in os.listdir(f'{os.path.expanduser(f'{config['path']['conf-folder']}/{config['path']['cache']}')}/{pkg}/scripts/'):
                lua_lib.exec_file(f'{os.path.expanduser(f'{config['path']['conf-folder']}/{config['path']['cache']}')}/{pkg}/scripts/{i}')

        print("Binaries: ")
        for i in os.listdir(f'{os.path.expanduser(f'{config['path']['conf-folder']}/{config['path']['cache']}')}/{pkg}/bin'):
            print('\t- ' + i + ' > ' + get_size(f'{os.path.expanduser(f'{config['path']['conf-folder']}/{config['path']['cache']}')}/{pkg}/bin/{i}'))
        
        if (info_file['dep']): 
            print("Dependencies: ")
            for i in info_file['dep']:
                if i:
                    print('\t- ' + i)

        yn = input(f'\033[33m[?]\033[0m Do you want to install {pkg} [Y/n]: ')
        if str(yn).lower() == 'y':
            if (info_file['dep']): 
                for i in info_file['dep']:
                    if i:
                        print(info_file['dep'])
                        install(i)
            bins = []
            files = os.listdir(f'{os.path.expanduser(f'{config['path']['conf-folder']}/{config['path']['cache']}')}/{pkg}/bin')
            for i in files:
                bins.append(i)
                shutil.copyfile(f'{os.path.expanduser(f'{config['path']['conf-folder']}/{config['path']['cache']}')}/{pkg}/bin/{i}', f'{os.path.expanduser(config['path']['bin'])}/{i}')
                st = os.stat(f'{os.path.expanduser(config['path']['bin'])}/{i}')
                os.chmod(f'{os.path.expanduser(config['path']['bin'])}/{i}', st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
                print(f'Downloaded {((files.index(i)+1)/len(files))*100}%')
            try:
                with open(f'{os.path.expanduser(f'{config['path']['conf-folder']}/{config['path']['cache']}')}/{pkg}/meta.toml', 'r') as file:
                    info_file_loaded = file.read()
                    info_file = toml.loads(info_file_loaded)

                    pkg_info = {}
                    try:
                        with open(f'{os.path.expanduser(os.path.expanduser(f'{config['path']['conf-folder']}/{config['path']['nxpi']}'))}', 'r') as f:
                            packages = f.read()
                            pkg_info = toml.loads(packages)
                    except:
                        catch_err(21)
                    pkg_info.update({f'{info_file['name']}': {'version': f'{info_file['version']}', 'author': f'{info_file['author']}', 'binaries': bins, 'scripts': []}})
                    with open(f'{os.path.expanduser(os.path.expanduser(f'{config['path']['conf-folder']}/{config['path']['nxpi']}'))}', 'w') as f:
                        toml.dump(pkg_info, f)
            except:
                catch_err(20)

            pc.print('Installed!', tag='success', tag_color='green', color='white')
        else:
            pass
        shutil.rmtree(f'{os.path.expanduser(f'{config['path']['conf-folder']}/{config['path']['cache']}')}/{pkg}')
    else:
        pkg = pkg.lower()
        url = config['repos']['def-repo']
    
        try:
            with urllib.request.urlopen(f'{url}/repoc.toml') as f:
                repoc = toml.loads(f.read().decode('utf-8'))
                try:
                    print(f'Installing {repoc['packages'][pkg][0]}')
                    res = requests.get(f'{url}/{repoc['packages'][pkg][0]}')
                    file_path = f'{pkg}.nxp'
                    if res.status_code == 200:
                        with open(file_path, 'wb') as file:
                            file.write(res.content)

                    install(f'{pkg}.nxp')
                    os.remove(f'{os.path.expanduser(f'./{pkg}.nxp')}')
                except:
                    catch_err(23)
        except:
            catch_err(60)

def remove(pkg):
    pkg_info = {}
    try:
        with open(f'{os.path.expanduser(os.path.expanduser(f'{config['path']['conf-folder']}/{config['path']['nxpi']}'))}', 'r') as f:
            packages = f.read()
            pkg_info = toml.loads(packages)
    except:
        catch_err(40) 

    print('Binaries to delete: ')
    try:
        for i in pkg_info[pkg]['binaries']:
            print(f'\t- {i} > {get_size(f'{os.path.expanduser(config['path']['bin'])}/{i}')}')
    except:
        catch_err(41)
    
    delete = input(f'\033[33m[?]\033[0m Do you want to delete this binaries [Y/n]: ')
    for i in pkg_info[pkg]['binaries']:
        if delete.lower() == 'y':
            try:
                os.remove(f'{os.path.expanduser(config['path']['bin'])}/{i}')
            except:
                print('Nothing to delete!')
                exit()
    try:
        del pkg_info[pkg]
        with open(f'{os.path.expanduser(os.path.expanduser(f'{config['path']['conf-folder']}/{config['path']['nxpi']}'))}', 'w') as f:
            toml.dump(pkg_info, f)
    except:
        catch_err(42)
    
    pc.print(f'{pkg} was deleted!', tag='success', tag_color='green', color='white')

def update(pkg):
    if not pkg == "":
        try:
            pkg_info = {}
            try:
                with open(f'{os.path.expanduser(os.path.expanduser(f'{config['path']['conf-folder']}/{config['path']['nxpi']}'))}', 'r') as f:
                    packages = f.read()
                    pkg_info = toml.loads(packages)
            except:
                catch_err(30)

            pkg = pkg.lower()
            url = config['repos']['def-repo']
            with urllib.request.urlopen(f'{url}/repoc.toml') as f:
                repoc = toml.loads(f.read().decode('utf-8'))
                if not repoc['packages'][pkg][1] == pkg_info[pkg]['version']:
                    print(f'Updating {pkg}: \033[31m\x1B[3m{pkg_info[pkg]['version']}\033[0m => \033[32m\x1B[3m{repoc['packages'][pkg][1]}\x1B[0m\033[0m')
                    install(pkg)
                else:
                    print(f'You have the stable version of {pkg}!')
        except:
            catch_err(60)
    else:
        pkg_info = {}
        try:
            with open(f'{os.path.expanduser(os.path.expanduser(f'{config['path']['conf-folder']}/{config['path']['nxpi']}'))}', 'r') as f:
                packages = f.read()
                pkg_info = toml.loads(packages)
        except:
            catch_err(30)

        for pkg_name in pkg_info:
            update(pkg_name)

def list_pkg():
    pkg_info = {}
    try:
        with open(f'{os.path.expanduser(os.path.expanduser(f'{config['path']['conf-folder']}/{config['path']['nxpi']}'))}', 'r') as f:
            packages = f.read()
            pkg_info = toml.loads(packages)
    except:
        catch_err(30)
    
    if len(pkg_info) > 0:
        for i in pkg_info:
            print(f'{i} => Version: {pkg_info[i]['version']}  Author: {pkg_info[i]['author']}')
    else:
        print('You don\'t have any packages! It\'s time to install one!')

def build_pkg(fpath):
    if os.path.exists(os.path.expanduser(fpath)):
        make_tarfile(f'{os.path.basename(fpath)}.nxp', os.path.expanduser(fpath))
        pc.print('Builded!', tag='success', tag_color='green', color='white')
    else:
        catch_err(50)

def search_pkg(pkg):
    pkg = pkg.lower()
    try:
        url = config['repos']['def-repo']
        with urllib.request.urlopen(f'{url}/repoc.toml') as f:
            repoc = toml.loads(f.read().decode('utf-8'))
            if repoc['packages'][pkg.lower()]:
                pc.print('Package Found!', tag='success', tag_color='green', color='white')
                print(f'Name: {pkg.lower()}')
                print(f'Enter \x1B[3m\'{sys.argv[0]} -i {pkg.lower()}\'\x1B[0m to get inforamtion about it!')
    except:
        catch_err(60)

def info(pkg):
    pkg = pkg.lower()
    try:
        url = config['repos']['def-repo']
        with urllib.request.urlopen(f'{url}/repoc.toml') as f:
            repoc = toml.loads(f.read().decode('utf-8'))
            info_file = {
                'name': pkg,
                'version': repoc['packages'][pkg][1],
                'author': repoc['packages'][pkg][2]
            }
            get_info_table(info_file)
    except:
        info_file = get_pkg_meta(pkg)
        get_info_table(info_file)
        shutil.rmtree(f'{config['path']['cache']}/{pkg}')

def update_nxp():
    print('Getting install.sh...')
    try:
        url = "https://raw.githubusercontent.com/hithja/nxp/master/install.sh"
        subprocess.run(f"sudo curl {url} | sudo bash", shell=True)
    except:
        catch_err(62)


def run(pkg, args):
    try:
        print(os.path.expanduser(f'{config['path']['bin']}/{pkg}'))
        subprocess.run([os.path.expanduser(f'{config['path']['bin']}/{pkg}')] + args)
    except:
        catch_err(70)