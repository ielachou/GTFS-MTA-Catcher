import os
from datetime import datetime
import requests
import time
import zlib

feeds = ["lirr%2Fgtfs-lirr", "nyct%2Fgtfs-ace", "nyct%2Fgtfs-g", "nyct%2Fgtfs-bdfm", "nyct%2Fgtfs-jz", "nyct%2Fgtfs-nqrw", "nyct%2Fgtfs-l", "nyct%2Fgtfs-si", "nyct%2Fgtfs"]

key = 'FfSOCa2mwf4rWzKPG651t7ZOPgFRO3E2DzpEnyR1'

if not os.path.exists("res"):
    os.makedirs('res')
for feed in feeds : 
    if feed == "nyct%2Fgtfs":
        term = "gtfs"
    else:
        term = feed.split('-')[1]
    if not os.path.exists("res/"+ term):
        os.makedirs('res/'+term)
if not os.path.exists("res/bus"):
        os.makedirs('res/bus')
i = -1
while i < 40320:
    try:
        i+=1
        now = datetime.now()

        dt_string = now.strftime("%Y-%m-%d_%H-%M-%S")
        for feed in feeds:
            x = requests.get('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/' + feed, headers={'x-api-key' : key})    
            if feed == "nyct%2Fgtfs":
                term = "gtfs"
            else:
                term = feed.split('-')[1]
            f = open("res/"+term+"/ny_mta_gtfs_"+term+"_"+dt_string, 'wb')
            compressed_text = zlib.compress(x.content)
            f.write(compressed_text)
            f.close()
        
        x = requests.get( 'http://gtfsrt.prod.obanyc.com/vehiclePositions?key='+key)
        f = open("res/bus/ny_mta_gtfs_bus_" + dt_string, 'wb')
        compressed_text = zlib.compress(x.content)
        f.write(compressed_text)
        f.close()

        time.sleep(15)
    except:
        pass
