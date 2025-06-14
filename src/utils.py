import os

def get_size(path):
    size = os.path.getsize(path)
    if size >= 1024 ** 3:
        return f'{size / 1024 ** 3} GB'
    elif size >= 1024 ** 2:
        return f'{size / 1024 ** 2} MB'
    elif size >= 1024:
        return f'{size / 1024} KB'
    else:
        return f'{size} B'