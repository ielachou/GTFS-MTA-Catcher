import os
from datetime import datetime
import requests
import time

feeds = ["lirr%2Fgtfs-lirr", "nyct%2Fgtfs-ace", "nyct%2Fgtfs-g", "nyct%2Fgtfs-bdfm", "nyct%2Fgtfs-jz", "nyct%2Fgtfs-nqrw", "nyct%2Fgtfs-l", "nyct%2Fgtfs-si", "nyct%2Fgtfs"]


if not os.path.exists("res"):
    os.makedirs('res')
for feed in feeds : 
    if feed == "nyct%2Fgtfs":
        term = "gtfs"
    else:
        term = feed.split('-')[1]
    if not os.path.exists(f"res/{term}"):
        os.makedirs(f'res/{term}')

for i in range(8):
    now = datetime.now()

    dt_string = now.strftime("%Y-%m-%d_%H-%M-%S")
    for feed in feeds:
        x = requests.get(f'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/{feed}', headers={'x-api-key' : 'API-KEY'})    
        if feed == "nyct%2Fgtfs":
            term = "gtfs"
        else:
            term = feed.split('-')[1]
        f = open(f"res/{term}/ny_mta_gtfs_{term}_{dt_string}", 'wb')
        f.write(x.content)
        f.close()
    time.sleep(15)
       
    