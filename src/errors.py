import print_color as pc

def catch_err(errcode):
    pc.print(f'Error! EC: {errcode}', tag='ERR', tag_color='red', color='white')
    exit(errcode)