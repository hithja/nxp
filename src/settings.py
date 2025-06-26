import toml
import os
#! Global variables are here!

config = {}
with open('conf.toml', 'r') as f:
    config = toml.loads(f.read())

USER=os.getlogin()