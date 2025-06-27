# NXP Package Manager
NXP is a package manager for linux made on Python.
NXP has own [repository](https://github.com/hithja/nxp-repo) and package format (`.nxp`).
NXP Packages can execute Lua-scripts before installing.
# Content
1. [Starting](#starting)
    1. [Installing package](#installing-package)
    2. [Getting all installed packages](#getting-all-installed-packages)
    3. [Arguments](#arguments)
2. [How to build](#how-to-build)
3. [How to make own package]()
4. [Errors](#errors)

# Starting
## Installing package
To install package in nxp, type `nxp -i <pkg name>`. This command will be install package from repository. If you downloaded `.nxp` package and you want to install it, type `nxp -i <pkg name>.nxp`.

## Getting all installed packages
To get all installed packages, type `nxp -l`.
The output will be like this:
```bash
pkg => Version: 15.0  Author: You
```

## Arguments
- `-i; --install` - installs package
- `-r; --remove` - removes package
- `-u; --update` - updates packages
- `-l; --list` - outputs all installed packages
- `-h; --help` - outputs help page
> Please, type `nxp -h` to see all arguments.

# How to build
First, install all requirements (requirements.txt).
Then type 
```sh
pyinstaller ./src/main.py --onefile --add-data "YOUR_LUPA_PATH"
```
After successfuly building type `./dist/main -v`. If it works, you build it successfuly.

# How to create package
> #### This part was taken from [NXP Repo `README.md`](https://github.com/hithja/nxp-repo/blob/main/README.md#how-to-create-package).

First, create `PACKAGE NAME` directory. Then create 2 directories and meta file like this:
>  Package name must be in lower-case!
- `bin` - your binaries
- `scripts` - lua-scripts
- `meta.toml` - info about your package
`meta.toml` must contain `name`, `author`, `version` and `dep` options.
```toml
# meta.toml example
name="your awsome package" # Package name
version="1.0.0" # Package version
author="You" # Package author
dep=[] # Package dependencies (not working yet)
```
To build your package you have to download NXP Package Manager (not avaiable yet).
Then enter in your terminal `nxp -bp <folder with your package>`.
> You can add your folders and change installation with your lua-scripts!

# Errors
All errors codes are in `ERRORS.md`.