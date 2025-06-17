import print_color as pc

def catch_err(errcode):
    match str(errcode)[0]:
        case "1":
            pc.print(f'Unpacking error! EC: {errcode}', tag='ERR', tag_color='red', color='white')
            exit(errcode)