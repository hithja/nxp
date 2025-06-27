import os
import toml
import tarfile
from errors import *
from settings import *

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

def get_size(path):
    size = 0
    try:
        size = round(os.path.getsize(path))
    except:
        catch_err(12)
    if size >= 1024 ** 3:
        return f'{round(size / 1024 ** 3)} GB'
    elif size >= 1024 ** 2:
        return f'{round(size / 1024 ** 2)} MB'
    elif size >= 1024:
        return f'{round(size / 1024)} KB'
    else:
        return f'{round(size)} B'
    
def create_deps():
    if not os.path.exists(os.path.expanduser(f'{config['path']['conf-folder']}/{config['path']['nxpi']}')):
        with open(os.path.expanduser(f'{config['path']['conf-folder']}/{config['path']['nxpi']}'), "x") as f:
            f.write("")
            f.close()
        
    if not os.path.exists(os.path.expanduser(f'{config['path']['conf-folder']}/{config['path']['conf-file']}')):
        with open(os.path.expanduser(f'{config['path']['conf-folder']}/{config['path']['conf-file']}'), "x") as f:
            f.write("")
            f.close()

    if not os.path.exists(os.path.expanduser(f'{config['path']['conf-folder']}/{config['path']['cache']}')):
        os.makedirs(os.path.expanduser(f'{config['path']['conf-folder']}/{config['path']['cache']}'))

    if not os.path.exists(os.path.expanduser(config['path']['conf-folder'])):
        os.makedirs(os.path.expanduser(config['path']['conf-folder']))
    if not os.path.exists(os.path.expanduser(config['path']['bin'])):
        os.makedirs(os.path.expanduser(config['path']['bin']))
def help():
    print("""
\033[1m\x1B[3m\033[32m\tNXP Package Manager\x1B[0m\033[0m
Package Format Version: 0.2

\033[32m+===== Package =====+\033[0m
-i; --install - installs package from repo or from \x1B[3m'.nxp'\x1B[0m file
-u; --update - updates all/one packages to newer version
-U; --upgrade - upgrades nxp to newer version
-p; --purge - removes installed package
-r; --run - runs app
-l; --list - outputs all installed packages
-s; --search - searchs package in repo
-I; --info - outputs info about package
-bp; --build-package - builds \x1B[3m'.nxp'\x1B[0m file

\033[32m+===== Other =====+\033[0m
-v; --version - outputs version of NXP 
-h; --help - outputs this page =)

\033[32m+===== Error Codes =====+\033[0m
You can see all error codes at \x1B[3m'ERRORS.md'\x1B[0m""")

def unpack_pkg(pkg):
    try:
        if pkg.endswith(".nxp"):
            file = tarfile.open(f'{pkg}') 
            file.extractall(os.path.expanduser(f'{config['path']['conf-folder']}/{config['path']['cache']}'), filter='data') 
            file.close()
            pc.print(f'{pkg} has unpacked!', tag='success', tag_color='green', color='white')
        else:
            pc.print(f'No .nxp package!', tag='ERR', tag_color='red', color='white')
    except:
        catch_err(10)

def get_pkg_meta(pkg):
    unpack_pkg(pkg)
    info_file = {}
    pkg = "".join(pkg.split(".nxp"))
    
    try:
        with open(f'{os.path.expanduser(f'{config['path']['conf-folder']}/{config['path']['cache']}')}/{pkg}/meta.toml', 'r') as file:
            info_file_loaded = file.read()
            info_file = toml.loads(info_file_loaded)
    except:
        catch_err(11)
    return info_file

def get_info_table(pkg_info):
    print(f'\033[32m+=== \033[1m{pkg_info['name']}\033[0m\033[32m ===+\033[0m')
    print(f'Version: {pkg_info['version']}')
    print(f'Author: {pkg_info['author']}')