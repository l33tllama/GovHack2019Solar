import psycopg2
conn = psycopg2.connect(database='gisdb', user='postgres', password="gisforgovhack", host="localhost")
curs = conn.cursor()

poi = (147.30656109999995, -42.8549318)

cur_command = "select ST_Area(geom) as AREA, * from building_footprints \
where st_contains((select geom from parcels_hobart \
where st_contains(st_transform(geom,4326),ST_SetSRID(ST_MakePoint({0[0]},{0[1]}),4326))), geom); ".format(poi)

cur_command = "SELECT ST_Area(geom) as AREA, heritage_zone, heritage_listed from buildings \
    where st_contains((select geom from parcels \
    where st_contains(st_transform(geom,4326),ST_SetSRID(ST_MakePoint({0[0]},{0[1]}),4326))), st_centroid(geom))".format(poi)

curs.execute(cur_command)

for row in curs.fetchall():
    print(row)