#!/usr/bin/env python3

#! NXP Package Manager
#! Made by hithja

import sys
import print_color as pc
from settings import *
from errors import *
from utils import *
from pkg_actions import *

if __name__ == '__main__':
    create_deps()

    args = {
        'i': ['-i', '--install'],
        'u': ['-u', '--update'],
        'r': ['-r', '--remove'],
        'run': ['--run'],
        'l': ['-l', '--list'],
        's': ['-s', '--search'],
        'I': ['-I', '--info'],
        'bp': ['-bp', '--build-package'],
        'h': ['-h', '--help'],
        'v': ['-v', '--version']
    }

    if len(sys.argv) > 1:
        if sys.argv[1] in args['i']:
            if len(sys.argv[2]) > 0:
                install(sys.argv[2])
        elif sys.argv[1] in args['u']:
            if len(sys.argv) > 3:
                update(sys.argv[2])
            else:
                update("")
        elif sys.argv[1] in args['r']:
            if len(sys.argv[2]) > 0:
                remove(sys.argv[2])
        elif sys.argv[1] in args['l']:
            list_pkg()
        elif sys.argv[1] in args['run']:
            if len(sys.argv[2]) > 0:
                run(sys.argv[2])
        elif sys.argv[1] in args['s']:
            if len(sys.argv[2]) > 0:
                search_pkg(sys.argv[2])
        elif sys.argv[1] in args['I']:
            if len(sys.argv[2]) > 0:
                info(sys.argv[2])
        elif sys.argv[1] in args['h']:
            help()
        elif sys.argv[1] in args['bp']:
            if len(sys.argv[2]) > 0:
                build_pkg(sys.argv[2])
        elif sys.argv[1] in args['v']:
            print(f'\x1B[3m{config['info']['name'].upper()} Package Manager {config['info']['version']}-{config['info']['codev']}\x1B[0m')
        else:
            pc.print(f'Invalid Argument!', tag='ERR', tag_color='red', color='white')
    else:
        pc.print(f'No Arguments!', tag='ERR', tag_color='red', color='white')