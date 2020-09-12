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
    blood_sugar_levels = []
    MAX_BLOOD_SUGAR = 3
    SAFE_SUGAR_LEVEL = 20
    UNSAGE_SUGAR_LEVEL = 40
    NEEDLE_EMPTY_CONDUCTIVITY = 20
    INSULIN_MAX_DOSAGE = 50
    INSULIN_MIN_DOSAGE = 10
    INSULIN_MAX_PER_DAY = 500
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
        if(len(self.blood_sugar_levels > 0)):
            displayWrite("sugar:\r\n"+str(self.blood_sugar_levels[-1])+" cc/L", self.DISPPOS_SUGAR)
        else:
            displayWrite("sugar:\r\n--cc/L", self.DISPPOS_SUGAR)
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
            write_string += str(dt.time())+") "+str(message)
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

        reservoir_level_result = reservoirLevel()

        return
    def loop10Minute(self):
        print("LOOP 10 MIN: ",getTime())

        #get the conductivity and turn it into blood sugar
        conductivity = getConductivity()
        blood_sugar = self.conductivity2sugar(conductivity)

        #add the sugar level to the list and remove the oldest value if the list is too long
        self.blood_sugar_levels.append(blood_sugar)
        if(len(self.blood_sugar_levels) >= self.MAX_BLOOD_SUGAR):
            self.blood_sugar_levels.pop(0)

        #send blood sugar to app
        self.logBloodSugar(blood_sugar)

        inject_insulin = False
        #get change in blood sugar levels
        rate_of_change1 = self.blood_sugar_levels[2]-self.blood_sugar_levels[1]
        rate_of_change2 = self.blood_sugar_levels[1]-self.blood_sugar_levels[0]
        #if blood sugar is above safe levels and the blood sugar level is increasing at an increasing rate then inject insulin
        if(blood_sugar >= self.SAFE_SUGAR_LEVEL and rate_of_change1 > 0 and rate_of_change1 > rate_of_change2):
            inject_insulin = True
        #if blood sugar is above unsafe levels and the blood sugar is not decreasing at an increasing rate then inejct insulin
        if(blood_sugar >= self.UNSAFE_SUGAR_LEVEL and not (rate_of_change1 < 0 and rate_of_change1 < rate_of_change2):
            inject_insulin = True
        return

        #if injection isnt needed then end the function
        if(not inject_insulin):
            return

        #get the insulin amount, check if its too small or too big and then turn it into steps of 10mL, round down
        insulin_amount = self.sugar2insulin(blood_sugar)
        if(insulin_amount < self.INSULIN_MIN_DOSAGE):
            insulin_amount = self.INSULIN_MIN_DOSAGE
        elif(insulin_amount > self.INSULIN_MAX_DOSAGE):
            insulin_amount = self.INSULIN_MAX_DOSAGE
        #constrain the amount of insulin given per day
        if(self.total_insulin_today + insulin_amount > self.INSULIN_MAX_PER_DAY):
            insulin_amount = self.INSULIN_MAX_PER_DAY - self.total_insulin_today
        insulin_steps = insulin_amount // 10

        #check if insulin value is still valid and needs to be injected
        if(insulin_steps <= 0):
            #negative or no steps does not require injection
            return
        
        #get the current reservoir level, used to check if the correct amount of insulin was injected
        current_reservoir_level = reservoirLevel()

        #inject the required amount of insulin
        for i in insulin_steps:
            activatePump()
            time.sleep(0.5)
        #get the new reservoir level and the difference between it and the old reservoir level
        new_reservoir_level = reservoirLevel()
        reservoir_difference = current_reservoir_level-new_reservoir_level
        #log the amount of insulin injects and how much was meant to be, add the actual insulin given to the daily amount given
        self.logInsulinInjected(reservoir_difference, insulin_steps*10)
        self.total_insulin_today += reservoir_difference

        
        #check if the amount of insulin that was injected was how much that left the reservoir
        if(reservoir_difference != insulin_steps*10):
            logIssue("Incorrect amount of insulin amount injected.")
        #check to see if there is insulin or something else is in the needle
        if(needleInternalConductivity() > self.NEEDLE_EMPTY_CONDUCTIVITY):
            logIssue("Needle has a blockage.")
    def logIssue(self,issue):
        self.messages.append((getTime(),issue))
        if(len(self.messages) >= self.MAX_MESSAGES):
            self.messages.pop(0)
        #later add connection and send to app

        #trigger alarm
        alarmSetState(True)
        time.sleep(0.5)
        alarmSetState(False)
        return True
    def logBloodSugar(self,blood_sugar):
        return
    def conductivity2sugar(self,conductivity):
        #convert conductivity into blood sugar
        res = conductivity
        return res
    def sugar2insulin(self,sugar):
        #calculate insulin from sugar
        res = sugar
        return res
p = PumpProgram()
setTimeMultiplier(5)
setDisplayPrint(False)
p.mainLoop()
