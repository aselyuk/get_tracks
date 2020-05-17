# coding: utf-8

import adsdb
from utils import add_to_log

DATA_SOURCE = ''
LOGIN = ""
PASSWORD = ""
LAN_PORT = 0
HOST = ""


def set_ads_settings(ads_config):
    ads_data_source = ads_config["data_source"]
    ads_login = ads_config["login"]
    ads_password = ads_config["password"]
    ads_host = ads_config["host"]
    ads_lan_port = ads_config["lan_port"]

    global DATA_SOURCE
    global LOGIN
    global PASSWORD
    global LAN_PORT
    global HOST

    DATA_SOURCE = ads_data_source
    HOST = ads_host
    LAN_PORT = ads_lan_port
    LOGIN = ads_login
    PASSWORD = ads_password

    print u"Database: '%s'" % DATA_SOURCE


def get_connection(data_source=DATA_SOURCE, login=LOGIN):
    if data_source == u"":
        data_source = DATA_SOURCE.encode("utf-8")
    if login == u"":
        login = LOGIN.encode("utf-8")
    conn = None
    try:
        conn = adsdb.connect(DataSource=data_source, UserID=login, ServerType='local or remote')
    except Exception as ex:
        print ex.args
        add_to_log(ex.args)
    return conn


def select_sql(sql, connection=None, parameters=()):
    conn = connection
    result = None
    fields = {}
    curs = None

    try:
        if conn is None:
            conn = get_connection()
        curs = conn.cursor()
        curs.execute(sql, parameters)
        result = curs.fetchall()
        for x in range(0, len(curs.description)):
            fields.update({str(curs.description[x][0]): x})
    except Exception as ex:
        print ex
        add_to_log(ex.args)
    finally:
        if connection is None and curs is not None:
            curs.close(True)
            conn.close()

    return result, fields


def exec_sql(sql, connection=None, parameters=()):
    conn = connection
    affected = 0
    curs = None

    try:
        if conn is None:
            conn = get_connection()
        conn.begin_transaction()
        curs = conn.cursor()
        curs.execute(sql, parameters)
        conn.commit()
        affected = curs.rowcount
    except Exception as ex:
        if connection is not None:
            conn.rollback()
        print ex
        add_to_log(ex.args)
    finally:
        if connection is None and curs is not None:
            curs.close(True)
            conn.close()

    return affected
