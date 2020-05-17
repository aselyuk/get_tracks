# -*- coding: utf-8 -*-
import datetime
import os
import socket
import json
import argparse


LOG_PATH = ".\\Logs\\"


def create_arg_parser():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--date', help="Date since",
                            default=datetime.datetime.now().strftime('%Y%m%d'))
    arg_parser.add_argument('--offset', help="Day offset. For until (since + offset)", default=0)
    arg_parser.add_argument('--save', help='Save track into folder', default="..\\tmp\\tracks")
    arg_parser.add_argument('--type', help='Track file type. plt or json ', default="plt")
    arg_parser.add_argument('--tspsw', help='Password from track server', default='')
    arg_parser.add_argument('--dbpsw', help='Password from database', default='')
    arg_parser.add_argument('--update', help='Update route in database (y - yes)', default='n')
    return arg_parser


def get_config():
    file_name = os.path.dirname(__file__) + "\\config.json"
    with open(file_name, "r") as read_file:
        conf = json.load(read_file)
    return conf


def get_hostname():
    hostname = socket.gethostname()
    return hostname


def get_ip(hostname=None):
    if hostname is None:
        hostname = socket.gethostname()
    ip = socket.gethostbyname_ex(hostname)
    s = ''
    for x in range(0, len(ip[2])):
        s += ip[2][x] + ","
    return s.strip(',')


def get_mmyy(date):
    return date.strftime("%m%y")


def get_sql_date(date):
    return date.strftime("%Y-%m-%d")


def lead0(number):
    return ("0" if number < 10 else "") + str(number)


def copy_row(row):
    return row.copy()


def get_good_file_name(file_path, file_name):
    file_path = file_path if file_path.endswith("\\") else file_path + "\\"

    if not os.path.isdir(file_path):
        print "Folder not exists [%s]" % file_path
        print "Creating folder..."
        try:
            os.makedirs(file_path)
        except OSError as ex:
            print ex.args
            return None

    count = 0
    new_file_name = file_name
    while os.path.isfile(file_path + new_file_name):
        count += 1
        tmp = os.path.splitext(file_name)
        new_file_name = tmp[0] + "(%d)%s" % (count, tmp[1])

    return file_path + new_file_name


def save_file(file_path, file_name, text):
    file_path = file_path if isinstance(file_path, str) else file_path.encode("utf-8")
    new_file_name = get_good_file_name(file_path, file_name)

    if new_file_name is None:
        return False

    f = open(new_file_name, "w")
    f.writelines(text)
    f.close()

    return os.path.isfile(new_file_name), new_file_name


def save_json_file(file_path, file_name, json_data):
    new_file_name = get_good_file_name(file_path, file_name)

    if new_file_name is None:
        return

    with open(new_file_name, 'w') as f:
        json.dump(json_data, f)


def add_to_log(text, file_name=None):
    if isinstance(text, unicode):
        text = text.encode("utf-8")
    current_date = datetime.datetime.now()
    hostname = get_hostname()
    ip = get_ip(hostname)
    if file_name is None:
        file_name = os.path.abspath(LOG_PATH)
        file_name += "\\Log_%s_%s.log" % (current_date.strftime('%Y-%m-%d'),
                                          ip.replace(".", "").replace(",", "_"))

    strtime = current_date.strftime("[%d.%m-%Y %H.%M.%S ") + hostname + "] "
    text = strtime + text + "\n"

    if not os.path.isfile(file_name):
        save_file(os.path.dirname(file_name), os.path.basename(file_name), text)
    else:
        f = open(file_name, "a")
        f.writelines(text)
        f.close()
