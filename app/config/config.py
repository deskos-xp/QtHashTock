import os,sys,json
import inspect,os
def getLocalizedPath():
        filename = inspect.getframeinfo(inspect.currentframe()).filename
        path = os.path.dirname(os.path.abspath(filename))
        return filename,path
class config:
    hour12FMT=False
    mute=False
    def __init__(self):
        with open(os.path.join(getLocalizedPath()[1],".env.json"),"r") as fd:
            conf=json.load(fd)
            self.hour12FMT=conf.get("hour12FMT") 
            self.mute=conf.get("mute")

    def save(self):
        with open(os.path.join(getLocalizedPath()[1],".env.json"),"w") as fd:
            d=dict(hour12FMT=self.hour12FMT,mute=self.mute)
            json.dump(d,fd)

