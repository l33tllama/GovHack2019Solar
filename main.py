from flask import Flask, request, render_template
import configparser
import psycopg2

# Flask App
app = Flask(__name__, static_folder="static")
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.debug = False

config_filename = "config.cfg"

config = configparser.ConfigParser()
config.read(config_filename)

api_key = config['Main']['GoogleAPIKey']


# Perform query to get PostGIS data about whether location is within area of heritage area
def check_if_heritage_area(lat, lng):
    pass


# Perform Postgres query to get PostGIS data about selected location
def get_area_by_latlng(lat, lng):
    conn = psycopg2.connect(database='gisdb', user='postgres', password="gisforgovhack", host="localhost")
    curs = conn.cursor()

    poi = (lat, lng)

    print(poi)

    """cur_command = "select ST_Area(geom) as AREA, * from building_footprints \
    where st_contains((select geom from parcels_hobart \
    where st_contains(st_transform(geom,4326),ST_SetSRID(ST_MakePoint({0[1]},{0[0]}),4326))), geom); ".format(poi)
    """
    """
    cur_command = "SELECT ST_Area(geom) as AREA, heritage_zone, heritage_listed from buildings \
        where st_contains((select geom from parcels \
        where st_contains(st_transform(geom,4326),ST_SetSRID(ST_MakePoint({0[1]},{0[0]}),4326))), st_centroid(geom))".format(poi)
    """

    cur_command = "SELECT ST_Area(geom) as AREA, heritage_zone, heritage_listed from buildings \
        where st_contains((select geom from parcels where \
        st_contains(st_transform(geom,4326),ST_SetSRID(ST_MakePoint({0[1]},{0[0]}),4326)) \
        order by st_area(geom) desc limit 1), st_centroid(geom))".format(poi)

    curs.execute(cur_command)

    largest_area = 0
    largest_area_heritage_zone = 0
    largest_area_heritage_listed = 0
    areas = []
    results = curs.fetchall()
    for row in results:
        print(row[0])
        areas.append([row[0], row[1], row[2]])
    if len(results) > 0:
        largest_area_heritage_zone = areas[0][1]
        largest_area_heritage_listed = areas[0][1]

        for area in areas:
            if area[0] > largest_area:
                print(area)
                try:
                    largest_area = area[0]
                    largest_area_heritage_zone = area[1]
                    largest_area_heritage_listed = area[2]
                except IndexError as e:
                    print("ERROR!! index out range")
                    print(e)

        return str(largest_area) + "," + str(largest_area_heritage_zone) + "," + str(largest_area_heritage_listed)
    else:
        return "0,0,0"

# Disable caching!
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route("/")
def main():
    return render_template('index.html', google_api_key=api_key)


@app.route("/get_area")
def get_area():
    lat = float(request.args.get("lat"))
    lng = float(request.args.get("lng"))
    print(lat)
    print(lng)
    area = get_area_by_latlng(lat, lng)
    return str(area)


def run():
    app.run(host="0.0.0.0", port=80)


run()
