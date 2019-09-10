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

## date
update = ""


# function
## Convert to Pixels
def parse(fn,begin,end):
    pixels = list()
    line = linecache.getline(fn,line_update) #update date
    update = line[24:40].replace(' ','').replace(':','').replace('-','')

    for j in range(begin,end):
        try:
            line = linecache.getline(fn,line_data + j) #Aurora data
            res = re.findall(pattern,line)
            blanks = list()
            for i in range(col_size):
                probability = int(res[i])
                if probability >= 0:
                    if probability >= 1:
                        alpha = 255
                    else:
                        alpha = 0
                    blue = 0
                    green = probability/100 * 255
                    red = 0
                    color = [red,green,alpha]
                    # print(color)
                    size = len(pixels)
                    pixels.append(list())
                    pixels[size].append(color)

                    # stock blank
                    blanks.append(probability)
                    
        except:
            break
    if(len(pixels) == 0):
        pixels.append(list())
        pixels[0].append([255,255,255,255])
    return pixels

## Get Data
def getData(url,fn):
    r = requests.get(url)
    txt = r.text
    r.close()
    f = open(fn,'w')
    f.write(txt)
    f.close()


def printOut(pixels,size,new_fn):
    array = np.array(pixels,dtype=np.uint8)
    # print(array)
    tmp = int(size)
    array = np.resize(array,(len(array)//tmp,tmp,len(array[0][0])))
    # print(array)
    new_image = Image.fromarray(array,"RGB")
    new_image.save(new_fn,mode="RGB")


def convert(url,fn,north_fn,south_fn):
    getData(url,fn)
    pixels = parse(fn,0,128)
    printOut(pixels,1024,north_fn)
    pixels = parse(fn,384,512)
    printOut(pixels,1024,south_fn)

# Main
if __name__ == "__main__":
    fn = "Aurora.txt"
    north_fn = sys.argv[1] + "_north.png"
    south_fn = sys.argv[1] + "_south.png"
    url = 'https://services.swpc.noaa.gov/text/aurora-nowcast-map.txt'
    
    print("Start Scraping")

    now = datetime.datetime.now()
    now_str = now.strftime("%Y%m%d%H%M")
    minute_str = now.strftime("%M")
    minute_int = int(minute_str)

    convert(url,fn,north_fn,south_fn)
    print("Got", now_str)

    while True:
        now = datetime.datetime.now()
        now_str = now.strftime("%Y%m%d%H%M")
        minute_str = now.strftime("%M")
        minute_int = int(minute_str)

        if(minute_int%5 == 0):
            convert(url,fn,north_fn,south_fn)
            print("Got", now_str)    
            
        time.sleep(60 * 1)