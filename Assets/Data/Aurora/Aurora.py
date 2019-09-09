import os
import sys
import time
import datetime

# scpaping
import requests
import linecache
import re

# Convert to Image
from PIL import Image
import numpy as np

# Global Parameter
## Size
row_size = int(512)
col_size = int(1024)

## Line
line_update = int(4)
line_data = int(18)

## Geo Position
init_long = 0
max_long = 360
init_lat = 0
max_lat = 180

div_long = 360 / 1024
div_lat = 180 / 512

## regax
pattern = "\d{1,3}"

## Image Parameter
max_probability = 100


# function
## Convert to Pixels
def parse(fn):
    pixels = list()
    line = linecache.getline(fn,line_update) #update date
    update = line[24:40].replace(' ','').replace(':','').replace('-','')

    for j in range(row_size):
        try:
            line = linecache.getline(fn,line_data + j) #Aurora data
            res = re.findall(pattern,line)
            latitude = init_lat + j * div_lat
            latitude = int(latitude / max_lat * 255)
            pixels.append(list())
            for i in range(col_size):
                longditute = init_long + i * div_long
                longditute = int(longditute/max_long * 255)
                probability = int(res[i])
                probability = int(probability/max_probability * 255)
                if probability > 0:
                    transparent = 255
                else:
                    transparent = 0
                # rgba = [longditute,latitude,probability,transparent]
                ga = [0,probability,0,transparent]
                ga = tuple(ga)
                pixels[j].append(ga)

            print("Complte:", line[24:40])

        except:
            break
    return pixels

## Get Data
def getData(url,fn):
    r = requests.get(url)
    txt = r.text
    f = open(fn,'w')
    f.write(txt)
    f.close()

# Main
if __name__ == "__main__":
    # Output
    sys.stdout = open('std.out',"w")
    sys.stderr = open('err.out',"w")
    
    ## File & URL Name
    fn = "Aurora.txt"
    new_fn = "Aurora"
    url = 'https://services.swpc.noaa.gov/text/aurora-nowcast-map.txt'
    
    print("Start Scraping")

    while True:
        now = datetime.datetime.now()
        now_str = now.strftime("%Y%m%d%H%M")
        minute_str = now.strftime("%M")
        minute_int = int(minute_str)
        
        getData(url,fn)
        pixels = parse(fn)
        array = np.array(pixels,dtype=np.uint8)
        new_image = Image.fromarray(array)
        new_image.save(new_fn)

        if(minute_int%5 == 0):
            getData(url,fn)
            pixels = parse(fn)
            array = np.array(pixels,dtype=np.uint8)
            new_image = Image.fromarray(array)
            new_image.save(new_fn + ".png")
            
        time.sleep(60 * 1)
