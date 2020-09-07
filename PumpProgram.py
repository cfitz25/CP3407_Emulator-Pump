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
    message_ind = 0
    sugar_level = 0
    reservoir_level = 0
    total_insulin_today = 0
    battery_level = 2

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
                self.loop5Second()
            #run if it has been atleast 30 seconds since last run
            if(tmp_time-last_time_30s >= 30):
                last_time_30s = tmp_time
                self.loop30Second()
            #run if it has been atleast 10 minutes since last run
            if(tmp_time-last_time_10min >= 10*60):
                last_time_10min = tmp_time
                self.loop10Minute()
            time.sleep(1)
        return

    def loop5Second(self):
        #display blood sugar levels
        displayWrite("sugar:\r\n"+str(self.sugar_level)+" cc/L", self.DISPPOS_SUGAR)
        #display how much is left in the reservoir
        displayWrite("left:\r\n"+str(self.sugar_level)+"mL", self.DISPPOS_RESERV)
        #display how much insulin has been given today
        displayWrite("total:\r\n"+str(self.sugar_level)+"mL", self.DISPPOS_TOTAL_INSULIN)
        #display battery left
        displayWrite("battery:\r\n"+str(self.sugar_level)+"%", self.DISPPOS_BATTERY)
        #if the last injection has occured display it otherwise display dummy info
        write_string = "last injection:\r\n"
        if(self.last_injection[0] != -1):
            dt = getDatetime(self.last_injection[0])

            write_string += str(self.last_injection[1])+"mL\r\n("+str(dt)+")"
        else:
            write_string += "--mL\r\n()"
        displayWrite(write_string, self.DISPPOS_LAST_INJECT)
        write_string = "("
        #if messages exist then display it otherwise display dummy info
        if(len(self.messages) > 0):
            time,message = self.messages[self.message_ind]
            self.message_ind += 1
            if(self.message_ind >= len(self.messages)):
                self.message_ind = 0
            dt = getDatetime(time)
            write_string += str(datetime.time())+") "+str(message)
        else:
            write_string += ") ---------------"
        displayWrite(write_string, self.DISPPOS_MESSAGES)
        return
    def loop30Second(self):
        print("LOOP 30 SEC: ",getTime())
        #check if the blood sensor is working, log error if not
        selfTestBloodSensor()
        blood_result = bloodSensorFunctional()
        if(not blood_result):
            self.logIssue("Sensor Test Failed.")
        #check if the pump is working, log error if not
        selfTestPump()
        pump_result = pumpFunctional()
        if(not pump_result):
            self.logIssue("Pump Test Failed.")
        #check if the needle is connected, log error if not
        needle_result = needleConnected()
        if(not needle_result):
            self.logIssue("Needle not connected.")
        #check if reservoir is connected, log error if not
        reservoir_result = reservoirConnected()
        if(not reservoir_result):
            self.logIssue("Reservoir not connected.")

        #if any issue occurs then alarm the user
        if(not blood_result or not pump_result or not needle_result or not reservoir_result):
            alarmSetState(True)
            time.sleep(0.5)
            alarmSetState(False)
        return
    def loop10Minute(self):
        print("LOOP 10 MIN: ",getTime())
        return
    def logIssue(self,issue):
        self.messages.append((getTime(),issue))
        if(len(self.messages) >= self.MAX_MESSAGES):
            self.messages.pop(0)
        return True
p = PumpProgram()
setTimeMultiplier(5)
setDisplayPrint(False)
p.mainLoop()
