import time
import datetime


class Emulator:
    
    def __init__(self,name):
        self.start_time = time.time()
        self.last_time = 0
        self.TIME_NOW = 0
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
        self.blood_sugar = 0

    def bodyLoop(self):
        if self.TIME_NOW < 6:
            if self.pump_functional & self.reservoir_connected & self.sensor_functional & self.needle_connected & self.pump_active:
                self.insulin_count += 10
                self.reservoir_level -= 10
                self.blood_sugar += self.insulin_count + self.blood_conductivity
            if self.TIME_NOW > 2:
                self.needle_connected = False
            time.sleep(1)
            if not self.needle_connected:
                self.pump_functional = False
                self.blood_sugar-=10
                self.insulin_count-=5


    def getTime(self):
        self.TIME_NOW
        self.last_time
        # modified time so its all relative to the start of the program, makes it easier to read and understand
        original_time = (time.time() - self.start_time)
        # get the time difference between last time and this time, then set the new last_time
        tmp_time = (original_time - self.last_time)
        last_time = original_time
        # apply multiplier to allow for faster simulation rate
        tmp_time *= self.time_multiplier
        # add modified time difference to TIME_NOW as it represents the emulators time
        self.TIME_NOW = self.TIME_NOW + tmp_time

        return self.TIME_NOW

    def getDatetime(self,time):
        dt = datetime.datetime.fromtimestamp(time + self.start_time)
        return dt

    # Emulator -> Program
    # returns conductivity of blood sensor (INT)
    def getConductivity(self):
        print("Blood Conductivity: " + str(self.blood_conductivity))
        return self.blood_conductivity

    # returns if the reservoir is connected (BOOL)
    def reservoirConnected(self):
        print("Reservoir Connected: " + str(self.reservoir_connected))
        return self.reservoir_connected

    # returns the level of the reservoir (INT)
    def reservoirLevel(self):
        print("Reservoir Level: " + str(self.reservoir_level))
        return self.reservoir_level

    # returns the results of the blood sensor self test (BOOL)
    def bloodSensorFunctional(self):
        print("Blood Sensor Functional: " + str(self.sensor_functional))
        return self.sensor_functional

    # returns the result of the pump self test (BOOL)
    def pumpFunctional(self):
        print("Pump Functional: " + str(self.pump_functional))
        return self.pump_functional

    # returns the voltage of the battery (INT)
    def batteryVoltage(self):
        print("Battery Voltage: " + str(self.battery_voltage))
        return self.battery_voltage

    # returns the conductivity of the liquid in the needle (INT)
    def needleInternalConductivity(self):
        print("Needle Conductivity: " + str(self.needle_conductivity))
        return self.needle_conductivity

    # returns if the needle is connected (BOOL)
    def needleConnected(self):
        print("Needle Connected: " + str(self.needle_connected))
        return self.needle_connected

    # returns the state of the manual button
    def manualButton(self):
        print("Manual Button State: " + str(self.button_state))
        return False

    # Program -> Emulator
    # starts a self test of the pump
    def selfTestPump(self):
        print("Self Test Pump started.")
        return False

    # starts a self test of the blood sensor
    def selfTestBloodSensor(self):
        print("Self Test Sensor started.")
        return False

    # makes the pump inject 10mL of insulin
    def activatePump(self):
        print("Pump Activated.")
        self.pump_active = True

    def deactivatePump(self):
        print("Pump De-activated.")
        self.pump_active = False

    # sets the state of the alarm
    def alarmSetState(self,state):
        print("Alarm: " + str(state))
        return False

    # write text to the display at position (x,y)
    def displayWrite(self,text, pos):
        if (self.display_print):
            print("Display: " + str(text))
        return False

    def setTime(self,time):
        self.TIME_NOW = time


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