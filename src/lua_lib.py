import lupa
import os
from settings import *
from errors import *
from utils import *

nxp_lib = {
    #! Functions
    "getInfo": get_pkg_meta,
    "getSize": get_size,
    "help": lambda: ", ".join(nxp_lib.keys()),
    "gcp": os.getcwd,
    #! Vars
    "USER": USER,
    "config": config,
}

lua = lupa.LuaRuntime(unpack_returned_tuples=True)
lua.globals().nxp = nxp_lib

def execute(code):
    lua.execute(code)

def exec_file(path):
    try:
        with open(path, "r") as f:
            lua_code = f.read()
            execute(lua_code)
    except:
        catch_err(22)