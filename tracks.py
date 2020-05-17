# -*- coding: utf-8 -*-

import datetime
import time
import urllib
import urllib2

import sql_queries
import ads
import utils
from utils import add_to_log

BASE_URL = ""
URL_PRMS = {}


class Route(object):
    def __init__(self):
        self.__datdoc = datetime.datetime.now()
        self.gps_id = None
        self.__car_num = None
        self.route_num = None
        self.__datetime_out = None
        self.__datetime_in = None
        self.__user_time = None

    @property
    def car_num(self):
        return self.__car_num

    @car_num.setter
    def car_num(self, value):
        self.__car_num = value

    @property
    def datetime_out(self):
        return self.__datetime_out

    @datetime_out.setter
    def datetime_out(self, value):
        self.__datetime_out = int(time.mktime(value.timetuple()) * 1000)

    @property
    def datetime_in(self):
        return self.__datetime_in

    @datetime_in.setter
    def datetime_in(self, value):
        self.__datetime_in = int(time.mktime(value.timetuple()) * 1000)

    @property
    def user_time(self):
        return self.__user_time

    @user_time.setter
    def user_time(self, value):
        self.__user_time = int(time.mktime(value.timetuple()) * 1000)

    @property
    def datdoc(self):
        return self.__datdoc

    @datdoc.setter
    def datdoc(self, value):
        self.__datdoc = value


class Track(object):
    def __init__(self, route, track_type, filename, track_data):
        self.route = route
        self.type = track_type if isinstance(track_type, str) else track_type.encode("utf-8")
        self.filename = filename
        self.track_data = track_data


def get_carnum(car_num):
    # О126ХН31 -> О126ХН
    if car_num is None or car_num is "":
        return car_num

    i = 0
    k = len(car_num)

    while car_num[k - 1:].isdigit():
        car_num = car_num[:k - 1]
        k = len(car_num)
        i += 1
    return car_num


def get_route(date=datetime.datetime.now(), route_num=None):
    if route_num is None or not isinstance(route_num, int):
        return None

    sql = sql_queries.sql_rth1_one
    sql = sql.replace(":date", utils.get_sql_date(date))
    sql = sql.replace(":mmyy", utils.get_mmyy(date))
    sql = sql.replace(":lr_num", "%d" % route_num)

    q, fields = ads.select_sql(sql)
    route = None

    if q is not None:
        for x in range(0, len(q)):
            route = Route()
            route.datdoc = q[x][fields["DATDOC"]]
            route.gps_id = q[x][fields["GPS_ID"]]
            route.car_num = get_carnum(q[x][fields["GOS_NUM"]])
            route.route_num = q[x][fields["LR_NUM"]]
            route.datetime_out = q[x][fields["DATE_OUT"]]
            route.datetime_in = q[x][fields["DATE_IN"]]
            route.user_time = datetime.datetime.now()
    return route


def get_routes(date=datetime.datetime.now()):
    sql = sql_queries.sql_rth1_any
    sql = sql.replace(":date", utils.get_sql_date(date))
    sql = sql.replace(":mmyy", utils.get_mmyy(date))

    routes = []

    q, fields = ads.select_sql(sql)
    if q is not None:
        for x in range(0, len(q)):
            route = Route()
            route.datdoc = q[x][fields["DATDOC"]]
            route.gps_id = q[x][fields["GPS_ID"]]
            route.car_num = q[x][fields["GOS_NUM"]]
            route.route_num = q[x][fields["LR_NUM"]]
            route.datetime_out = q[x][fields["DATE_OUT"]]
            route.datetime_in = q[x][fields["DATE_IN"]]
            route.user_time = datetime.datetime.now()
            routes.append(route)
    return routes


def gps_track(route, result_type):
    if not isinstance(route, Route):
        return None
    url = BASE_URL
    params = URL_PRMS
    track = None
    response = None
    try:
        params["usertime"] = "%d" % route.user_time
        params["obj"] = "%s" % route.gps_id
        params["begin"] = "%d" % route.datetime_out
        params["end"] = "%d" % route.datetime_in
        params["return_type"] = result_type

        data = urllib.urlencode(params)
        print url + data
        response = urllib2.urlopen(url + data)
        if response.code != 200:
            raise Exception("Error! Server response code: " + response.code)
        response_text = response.read()

        if result_type == "plt":
            response_text = set_reserved(response_text, "Reserved 3", route.car_num)
        filename = get_filename(route, result_type)
        track = Track(route, result_type, filename, response_text)
    except Exception as ex:
        print ex.args
        add_to_log(ex.args)
    finally:
        if response is not None:
            response.close()

    return track


def gps_tracks(routes, result_type):
    if not isinstance(routes, list):
        return []

    tracks = []

    for x in range(0, len(routes)):
        if isinstance(routes[x], Route):
            track = gps_track(routes[x], result_type)
            if isinstance(track, Track):
                tracks.append(track)
    return tracks


def set_reserved(string, old="Reserved 3", new=None):
    if new is None:
        return string

    source = string.replace(old, new)
    return source


def get_filename(route, result_type):
    if not isinstance(route, Route):
        return None

    date_out = datetime.datetime.fromtimestamp(route.datetime_out / 1000)
    date_in = datetime.datetime.fromtimestamp(route.datetime_in / 1000)

    filename = "%s-%s-%s-%s.%s" % (route.car_num, route.route_num,
                                   date_out.strftime("%Y%m%d-%H%M"),
                                   date_in.strftime("%Y%m%d-%H%M"),
                                   result_type.encode("utf-8"))
    return filename


def save_track(track, path):
    if not isinstance(track, Track):
        return False
    saved = utils.save_file(path, track.filename, track.track_data)
    log = "saved track :" if saved[0] else "not saved track: "
    log += saved[1]
    print log
    add_to_log(log)
    return saved[0]


def update_route_db(route):
    if not isinstance(route, Route):
        return 0

    sql = sql_queries.sql_rth1_update
    datdoc = route.datdoc
    mmyy = utils.get_mmyy(datdoc)
    sql = sql.replace(":mmyy", mmyy)
    route_num = str(route.route_num)

    updated = ads.exec_sql(sql, None, (datdoc, route_num))
    return updated > 0
