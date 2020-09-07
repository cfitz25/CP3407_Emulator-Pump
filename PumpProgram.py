from Emulator import *

def mainLoop():
    last_time_30s = getTime()
    last_time_10min = last_time_30s

    while True:
        tmp_time = getTime()
        #print(tmp_time)
        if(tmp_time-last_time_30s >= 30):
            last_time_30s = tmp_time
            loop30Second()
        if(tmp_time-last_time_10min >= 10*60):
            last_time_10min = tmp_time
            loop10Minute()
        time.sleep(1)
    return
def loop30Second():
    print("LOOP 30 SEC: ",getTime())
    return
def loop10Minute():
    print("LOOP 10 MIN: ",getTime())
    return
mainLoop()