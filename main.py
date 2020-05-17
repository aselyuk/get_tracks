# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

import utils
import os
import tracks
from ads import set_ads_settings

if __name__ == '__main__':
    print "START!!"

    parser = utils.create_arg_parser()
    namespace = parser.parse_args()
    save_to = namespace.save  # path to save file
    if save_to.startswith(".\\") or save_to.startswith('..\\'):
        save_to = os.path.dirname(__file__) + "\\" + save_to

    default_type = namespace.type  # default type of track-file (plt or json)
    track_password = namespace.tspsw  # for track server
    db_password = namespace.dbpsw  # for ads
    need_update = namespace.update
    need_update = need_update.lower().startswith('y')

    # since/until
    start_date = datetime.strptime(namespace.date, '%Y%m%d')
    day_offset = int(namespace.offset)
    end_date = start_date + timedelta(days=day_offset)

    if end_date < start_date:
        start_date, end_date = end_date, start_date
    print "Date range: %s - %s" % (
        start_date.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d')
    )

    config = utils.get_config()

    # advantage database settings
    ads = config["ads"]
    ads["password"] = db_password
    set_ads_settings(ads)

    # track server settings
    track_server = config["track_server"]
    track_types = track_server["track_types"]
    tracks.BASE_URL = track_server["url"]
    url_params = track_server["url_params"]
    url_params["password"] = track_password
    url_params["return_type"] = default_type
    tracks.URL_PRMS = url_params

    # todo: save by date
    save_by_date = config["save_by_date"]
    # todo: save by type
    save_by_type = config["save_by_type"]

    logs = config["logs"]
    if logs.startswith(".\\") or logs.startswith('..\\'):
        logs = os.path.dirname(__file__) + "\\" + logs
    utils.LOG_PATH = logs

    # For single route
    # route = tracks.get_route(date=datetime(2020, 05, 7), route_num=23218)
    # track = tracks.gps_track(route, result_type=default_type)
    # saved = tracks.save_track(track, save_to)
    # if saved and need_update:
    #     tracks.update_route_db(track.route)

    # For all routes from db
    current_date = start_date
    while current_date <= end_date:
        print "\nBegin: Current date: %s" % current_date
        routes = tracks.get_routes(current_date)
        routes_count = len(routes)
        tracks_count = 0
        tracks_saved = 0
        tracks_updated = 0
        if routes_count > 0:
            track_list = tracks.gps_tracks(routes, result_type=default_type)
            tracks_count = len(track_list)
            for x in xrange(0, len(track_list)):
                saved = tracks.save_track(track_list[x], save_to)
                if saved:
                    tracks_saved += 1
                    if need_update:
                        updated = tracks.update_route_db(track_list[x].route)
                        tracks_updated += 1 if updated else 0

        print "End: Current date: %s\t[Routes: %d\tTracks: %d\tSaved: %d\tUpdated: %d]" % (
            current_date, routes_count, tracks_count, tracks_saved, tracks_updated
        )
        current_date += timedelta(days=1)

    print "END"
