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
def parse(fn):
    pixels = list()
    line = linecache.getline(fn,line_update) #update date
    update = line[24:40].replace(' ','').replace(':','').replace('-','')

    for j in range(row_size):
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
                    blue = j%256
                    green = probability/100 * 255
                    red = j//256
                    color = [red,green,blue,alpha]
                    # print(color)
                    size = len(pixels)
                    pixels.append(list())
                    pixels[size].append(color)

                    # stock blank
                    blanks.append(probability)
            
            # remove blank row
            blanks = np.array(blanks)
            if blanks.max() < 1:
                for i in range(col_size):
                    pixels.pop()
                    
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


def convert(url,fn,new_fn):
    getData(url,fn)
    pixels = parse(fn)
    array = np.array(pixels,dtype=np.uint8)
    # print(array)
    tmp = int(1024)
    array = np.resize(array,(len(array)//tmp,tmp,4))
    # print(array)
    new_image = Image.fromarray(array,"RGBA")
    new_image.save(new_fn,mode="RGBA")


# Main
if __name__ == "__main__":
    # Output
    #sys.stdout = open('std.out',"w")
    #sys.stderr = open('err.out',"w")
    
    ## File & URL Name
    # path = sys.argv[1]
    # fn = os.path.basename(path)
    # fn = os.path.splitext(fn)[0]

    fn = "Aurora.txt"
    new_fn = sys.argv[1] + ".png"
    url = 'https://services.swpc.noaa.gov/text/aurora-nowcast-map.txt'
    
    print("Start Scraping")

    now = datetime.datetime.now()
    now_str = now.strftime("%Y%m%d%H%M")
    minute_str = now.strftime("%M")
    minute_int = int(minute_str)

    convert(url,fn,new_fn)
    print("Got", now_str)

    while True:
        now = datetime.datetime.now()
        now_str = now.strftime("%Y%m%d%H%M")
        minute_str = now.strftime("%M")
        minute_int = int(minute_str)

        if(minute_int%5 == 0):
            convert(url,fn,new_fn)
            print("Got", now_str)    
            
        time.sleep(60 * 1)