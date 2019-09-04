import requests
from datetime import datetime
import time
import json

class SolarWind():
    count = int(0)
    solarwinds = []

    def __init__(self,time_tag,density,speed,tempareture):
        self.time_tag = time_tag.replace("-","").replace(":","").replace(".","").replace(" ","").replace("00000","")
        self.density = float(density)
        self.speed = float(speed)
        self.tempareture = int(tempareture)
        
        SolarWind.solarwinds.append(self)

    def cov2json(fn):
        sw = SolarWind.solarwinds[-1] 
        tmp = {
            "time": sw.time_tag,
            "density": sw.density,
            "speed": sw.speed,
            "tempareture": sw.tempareture
        }
        f = open("SolarWind.json","w")
        json.dump(tmp,f,ensure_ascii=False,sort_keys=False,indent=4,separators=(",", ": "))

if __name__ == "__main__":
    fn = "SolarWind.json"
    url = "https://services.swpc.noaa.gov/products/solar-wind/plasma-5-minute.json"

    while True:
        SolarWind.solarwinds = list()

        r = requests.get(url)
        txt = r.text

        loaded = json.loads(txt)
        
        for data in loaded[1:]:
            sw = SolarWind(data[0],data[1],data[2],data[3])

        SolarWind.cov2json(fn)

        print("Complte:",datetime.now().strftime("%y/%m/%d|%H:%M"))

        time.sleep(60)