# -*-coding: utf-8 -*-
import os


path = '/opt/work/web/data/custom.ini'
path_0 = '/opt/work/web/data/oem/0/custom.ini'
path_D = '/opt/work/web/data/oem/D/custom.ini'
path_W = '/opt/work/web/data/oem/W/custom.ini'
path_X = '/opt/work/web/data/oem/X/custom.ini'
path_Q = '/opt/work/web/data/oem/Q/custom.ini'
oem_sh = '/opt/work/web/data/oem/oem.sh'


def get_cur_version(path):
    cur_version = ''
    title = ''
    with open(path, 'r') as f:
        lines = f.readlines()
        cur_version = lines[0].strip()
        for line in lines:
            if '=' in line and 'title' in line:
                title = line.split('=')[1].strip()
    return cur_version, title


def run():
    try:
        oem = 'X'
        cur_ver, title = get_cur_version(path)
        if cur_ver in ['#0', '#W' '#D', '#Q', '#X']:
            oem = cur_ver[1]
        elif title == get_cur_version(path_0)[1]:
            oem = '0'
        elif title == get_cur_version(path_D)[1]:
            oem = 'D'
        elif title == get_cur_version(path_W)[1]:
            oem = 'W'
        elif title == get_cur_version(path_Q)[1]:
            oem = 'Q'
        elif title == get_cur_version(path_X)[1]:
            oem = 'X'
        os.popen('sudo {} {}'.format(oem_sh, oem))
    except Exception as err:
        print(err)


if __name__ == '__main__':
    run()
