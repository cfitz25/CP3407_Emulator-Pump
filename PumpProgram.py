from Emulator import *

class PumpProgram:
    DISPPOS_SUGAR = (0,0)
    DISPPOS_RESERV = (20,0)
    DISPPOS_TOTAL_INSULIN = (40,0)
    DISPPOS_BATTERY = (60,0)
    DISPPOS_LAST_INJECT = (20,20)
    DISPPOS_MESSAGES = (0,40)
    last_injection = (0,0)
    messages = []
    MAX_MESSAGES = 5
    current_message = 0
    sugar_level = 0
    reservoir_level = 0
    total_insulin_today = 0
    battery_level = 0

    def __init__(self):
        return

    def mainLoop(self):
        last_time_30s = getTime()
        last_time_10min = last_time_30s
        last_time_5s = last_time_30s
        while True:
            tmp_time = getTime()
            #run if it has been atleast 30 seconds since last run
            if(tmp_time-last_time_5s >= 5):
                last_time_5s = tmp_time
                loop5Second()
            #run if it has been atleast 30 seconds since last run
            if(tmp_time-last_time_30s >= 30):
                last_time_30s = tmp_time
                loop30Second()
            #run if it has been atleast 10 minutes since last run
            if(tmp_time-last_time_10min >= 10*60):
                last_time_10min = tmp_time
                loop10Minute()
            time.sleep(1)
        return
    def loop5Second(self):
        displayWrite("sugar:\r\n"+str(self.sugar_level)+" cc/L", self.DISPPOS_SUGAR)
        displayWrite("left:\r\n"+str(self.sugar_level)+"mL", self.DISPPOS_SUGAR)
        displayWrite("total:\r\n"+str(self.sugar_level)+"mL", self.DISPPOS_SUGAR)
        displayWrite("battery:\r\n"+str(self.sugar_level)+"%", self.DISPPOS_SUGAR)
        displayWrite("last injection:\r\n"+str(self.sugar_level)+"mL\r\n("+str(time.), self.DISPPOS_SUGAR)
        displayWrite("sugar:\r\n"+str(self.sugar_level)+" cc/L", self.DISPPOS_SUGAR)
        return
    def loop30Second(self):
        print("LOOP 30 SEC: ",getTime())
        #check if the blood sensor is working
        selfTestBloodSensor()
        blood_result = bloodSensorFunctional()
        #check if the pump is working
        selfTestPump()
        pump_result = pumpFunctional()
        #check if the needle is connected
        needle_connected = needleConnected()
        #check if reservoir is connected
        reservoir_connected = reservoirConnected()


        return
    def loop10Minute(self):
        print("LOOP 10 MIN: ",getTime())
        return
mainLoop()