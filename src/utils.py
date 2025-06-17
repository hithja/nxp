import os

def get_size(path):
    size = round(os.path.getsize(path))
    if size >= 1024 ** 3:
        return f'{round(size / 1024 ** 3)} GB'
    elif size >= 1024 ** 2:
        return f'{round(size / 1024 ** 2)} MB'
    elif size >= 1024:
        return f'{round(size / 1024)} KB'
    else:
        return f'{round(size)} B'
    
def create_deps(config):
    if os.path.exists(config['path']['nxpi']):
        pass
    else:
        f = open(config['path']['nxpi'], "x")
        f.close()

    if os.path.exists(config['path']['cache']):
        pass
    else:
        os.makedirs(config['path']['cache'])

def help(config):
    with open(f'{config['path']['help-file']}', 'r') as f:
        help_file = f.read()
        print(help_file.encode().decode('unicode_escape'))