from flask import Flask, request
import psycopg2

# Flask App
app = Flask(__name__, static_folder="static")
app.debug = False


# Perform Postgres query to get PostGIS data about selected location
def get_area_by_latlng(lat, lng):
    conn = psycopg2.connect(database='gisdb', user='postgres', password="gisforgovhack", host="localhost")
    curs = conn.cursor()

    poi = (lat, lng)

    print(poi)

    cur_command = "select ST_Area(geom) as AREA, * from building_footprints \
    where st_contains((select geom from parcels_hobart \
    where st_contains(st_transform(geom,4326),ST_SetSRID(ST_MakePoint({0[1]},{0[0]}),4326))), geom); ".format(poi)

    curs.execute(cur_command)

    largest_area = 0
    areas = []

    for row in curs.fetchall():
        print(row[0])
        areas.append(row[0])

    for area in areas:
        if area > largest_area:
            largest_area = area

    return largest_area

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
    return app.send_static_file('index.html')


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
