import requests
import pandas as pd
import time

import google.protobuf.json_format as json_format
import google.protobuf.text_format as text_format
import json

import gtfs_realtime_pb2 as rt
import os
import zlib

def get_descriptor(message):
    if message is None:
        return pd.DataFrame()
    else:
        df = pd.DataFrame.from_dict([message])
        return df

dirs = os.listdir("res")


for directory in dirs[:1] : 
    ls = os.listdir("res/" + directory)[:5]
    full_df = pd.DataFrame()
    
    for file in ls:
        message = rt.FeedMessage()
        f = open("res/" + directory + "/" + "file", 'rb')
        
        j=0
        
        time.sleep(1)
        uncompressed = zlib.decompress(f.read())
        f.close()
        message.ParseFromString(uncompressed)
        
        data = json.loads(json_format.MessageToJson(message))
        
        for dic in data["entity"]:
            if "vehicle" in dic:
                curr_v = data["entity"][j]["vehicle"]
                
                df = pd.DataFrame()

                df = pd.concat([df,get_descriptor(curr_v.get("trip"))], axis = 1)
                df = pd.concat([df,get_descriptor(curr_v.get("vehicle"))], axis = 1)
                df = pd.concat([df,get_descriptor(curr_v.get("position"))], axis = 1)
                df["current_status"] = curr_v.get("currentStatus")
                df["stop_id"] = curr_v.get("stopID")
                df["timestamp"] = curr_v.get("timestamp")
                df["congestion_level"] = curr_v.get("congestionLevel")
                df["occupancy_status"] = curr_v.get("occupancyStatus")
                df["current_stop_sequence"] = curr_v.get("currentStopSequence")
                
                full_df = pd.concat([df, full_df])
            j+=1

    full_df = full_df.drop_duplicates()

    full_df.to_csv(f"res/" + directory + ".csv", index= False)