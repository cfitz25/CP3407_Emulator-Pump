import time
import datetime
import random
start_time = time.time()
last_time = 0
TIME_NOW = 0
time_multiplier = 5

class Emulator:
    def __init__(self, name):
        self.start_time = time.time()
        self.last_time = self.start_time
        self.TIME_NOW = self.start_time
        self.time_diff = 0
        self.time_multiplier = 5
        self.display_print = True
        self.button_state = False
        self.needle_connected = True
        self.needle_conductivity = 0
        self.battery_voltage = 5
        self.pump_functional = True
        self.pump_active = False
        self.sensor_functional = True
        self.reservoir_level = 100
        self.reservoir_connected = True
        self.blood_conductivity = 0.5
        self.insulin_count = 0
        self.blood_sugar = 20
        self.insulin_active = 0
        self.count = 0

    def bodyCalc(self):
        # multiplier = self.time_diff
        self.insulin_active += 0.1
        self.insulin_count -= 0.1
        if(self.insulin_count <= 0):
            self.insulin_count = 0
            self.insulin_active = 0
        self.blood_sugar += (0.006*self.blood_sugar - 0.5*self.insulin_active)*0.03
        
        if(self.blood_sugar < 0):
            self.blood_sugar = 0

        self.count += 1
        if(self.count > 5):
            self.print("BLOOD SUGAR",str(self.blood_sugar)+" "+str(self.insulin_count))
            self.count = 0
        # if not self.reservoir_connected or not self.needle_connected:
        #     self.pump_functional = False
        # else:
        #     self.pump_functional = True
        
        self.blood_conductivity = self.blood_sugar


    def run(self):
        self.TIME_NOW += 1
        #self.print("TIME",str(self.TIME_NOW-self.start_time))
        self.time_diff = self.TIME_NOW - self.last_time
        # print(self.time_diff)
        if self.time_diff < 60:
            # self.TIME_NOW = time.time()
            # self.time_diff = self.TIME_NOW - self.start_time
            self.bodyCalc()
            self.needle_connected = random.randint(0,100) < 80
            
            self.reservoir_connected = random.randint(0,100) < 80
        else:
            self.last_time = self.TIME_NOW
        if(self.reservoir_level <= 0):
            self.reservoir_level = 100

    def getTime(self):
        # # global TIME_NOW
        # # global last_time
        # # modified time so its all relative to the start of the program, makes it easier to read and understand
        # original_time = (time.time() - self.start_time)
        # # get the time difference between last time and this time, then set the new last_time
        # tmp_time = (original_time - last_time)
        # last_time = original_time
        # # apply multiplier to allow for faster simulation rate
        # tmp_time *= self.time_multiplier
        # # add modified time difference to TIME_NOW as it represents the emulators time
        # TIME_NOW = TIME_NOW + tmp_time

        return self.TIME_NOW

    def getDatetime(self,time):
        dt = datetime.datetime.fromtimestamp(time)
        return dt

    # Emulator -> Program
    # returns conductivity of blood sensor (INT)
    def getConductivity(self):
        # print("Blood Conductivity: " + str(self.blood_conductivity))
        return self.blood_conductivity

    # returns if the reservoir is connected (BOOL)
    def reservoirConnected(self):
        # print("Reservoir Connected: " + str(self.reservoir_connected))
        return self.reservoir_connected

    # returns the level of the reservoir (INT)
    def reservoirLevel(self):
        # print("Reservoir Level: " + str(self.reservoir_level))
        return self.reservoir_level

    # returns the results of the blood sensor self test (BOOL)
    def bloodSensorFunctional(self):
        # print("Blood Sensor Functional: " + str(self.sensor_functional))
        return self.sensor_functional

    # returns the result of the pump self test (BOOL)
    def pumpFunctional(self):
        # print("Pump Functional: " + str(self.pump_functional))
        return self.pump_functional

    # returns the voltage of the battery (INT)
    def batteryVoltage(self):
        # print("Battery Voltage: " + str(self.battery_voltage))
        return self.battery_voltage

    # returns the conductivity of the liquid in the needle (INT)
    def needleInternalConductivity(self):
        # print("Needle Conductivity: " + str(self.needle_conductivity))
        return self.needle_conductivity

    # returns if the needle is connected (BOOL)
    def needleConnected(self):
        # print("Needle Connected: " + str(self.needle_connected))
        return self.needle_connected

    # returns the state of the manual button
    def manualButton(self):
        # print("Manual Button State: " + str(self.button_state))
        return False

    # Program -> Emulator
    # starts a self test of the pump
    def selfTestPump(self):
        # print("Self Test Pump started.")
        return False

    # starts a self test of the blood sensor
    def selfTestBloodSensor(self):
        # print("Self Test Sensor started.")
        return False

    # makes the pump inject 10mL of insulin
    def activatePump(self):
        # print("Pump Activated.")
        multiplier = 10
        self.pump_active = True
        if self.pump_functional & self.reservoir_connected & self.sensor_functional & self.needle_connected & self.pump_active:
            self.insulin_count += multiplier
            self.reservoir_level -= multiplier
            
            # print("INEJCTED")
    def deactivatePump(self):
        # print("Pump De-activated.")
        self.pump_active = False

    # sets the state of the alarm
    def alarmSetState(self,state):
        # print("Alarm: " + str(state))
        return False

    # write text to the display at position (x,y)
    def displayWrite(self,text, pos):
        if (self.display_print):
            print("Display: " + str(text))
        return False

    def setTime(self,time):
        self.TIME_NOW = time
    def printSetup(self,headers):
        self.max_length = 0
        try:
            for h in headers:
                tmp = len(h)
                if(tmp > self.max_length):
                    self.max_length = tmp
        except:
            self.max_length = headers
    def print(self,header, message):
        if(not self.print_on):
            return
        print_string = "["
        left_over = self.max_length - len(header)
        for i in range(int(left_over/2)):
            print_string += " "
        print_string += header
        for i in range(self.max_length-len(print_string)):
            print_string += " "
        print_string += "] "
        print_string += message
        print(print_string)

# emulator = Emulator("emulator")
# emulator.activatePump()
# clock = 0
# while clock < 10:
#     emulator.setTime(clock)
#     emulator.bodyLoop()
#     if(clock==6):
#         emulator.deactivatePump()
#     print("Blood Sugar    : " + str(emulator.blood_sugar) + " mmol/L \nInsulin Count  : " + str(emulator.insulin_count) + "\n"+ "Pump Funcional : " + str(emulator.pump_functional) + "\n")
#     clock+=1
#     print(emulator.getTime())
# emulator.getTime()
# emulator.getDatetime(0)
# emulator.getConductivity()
# emulator.reservoirConnected()
# emulator.reservoirLevel()
# emulator.bloodSensorFunctional()
# emulator.pumpFunctional()
# emulator.batteryVoltage()
# emulator.needleInternalConductivity()
# emulator.needleConnected()
# emulator.manualButton()
# emulator.selfTestPump()
# emulator.selfTestBloodSensor()
# emulator.activatePump()
# emulator.deactivatePump()
# emulator.alarmSetState(True)
# emulator.displayWrite("test", (0,0))
# emulator.setTime(0)
# emulator.printSetup(20)
# emulator.print("Test","This is a Test.")
# emulator.print("TestTestTest","This is a Test.")
# emulator.print("TestTestest","This is a Test.")

    def setTime(self, time):
        self.TIME_NOW = time
        return False


# emulator = Emulator("emulator")
# emulator.activatePump()
# start = time.time()
# diff = time.time() - start
# while diff < 10:
#     emulator.setTime(time.time())
#     emulator.run()
#     if (diff>= 6):
#         emulator.deactivatePump()
#     elif (diff >= 5):
#         state = emulator.selfTestPump()
#     #     print("Is Pump Functional? " + str(state))
#     # print("Blood Sugar    : " + str(emulator.blood_sugar) + " mmol/L \nInsulin Count  : " + str(
#     #     emulator.insulin_count) + "\n" + "Pump Funcional : " + str(
#     #     emulator.pump_functional) + "\n" + "Pumnp Active   : " + str(emulator.pump_active) + "\n")
#     diff = time.time() - start
#     time.sleep(1)
