import time
import datetime
start_time = time.time()
last_time = 0
TIME_NOW = 0
time_multiplier = 5

display_print = True

button_state = False
needle_connected = False
needle_conductivity = 0
battery_voltage = 5
pump_functional = False
sensor_functional = False
reservoir_level = 100
reservoir_connected = False
blood_conductivity = 0
insulin_count = 0
blood_sugar = 0

def bodyLoop(insulin_count=None, reservoir_level=None, blood_conductivity=None):
    clock = 0
    while clock < 6:
            if pump_functional & reservoir_connected & sensor_functional & needle_connected:
                insulin_count += 10
                reservoir_level -= 10
                blood_conductivity += insulin_count
                blood_sugar = blood_conductivity / 10
            if clock > 2:
                needleConnected = False
            time.sleep(1)
            if not needleConnected:
                print("Needle Disconnected!\n")
                pumpFunctional = False
            print(
                str(blood_sugar) + " mmol/L \nInsulin Count:" + str(insulin_count) + "\nPump is Connected:" + str(
                    pumpFunctional) + "\n")

            clock += 1


def getTime():
    global TIME_NOW
    global last_time
    #modified time so its all relative to the start of the program, makes it easier to read and understand
    original_time = (time.time()-start_time)
    #get the time difference between last time and this time, then set the new last_time
    tmp_time = (original_time-last_time)
    last_time = original_time
    #apply multiplier to allow for faster simulation rate
    tmp_time *= time_multiplier
    #add modified time difference to TIME_NOW as it represents the emulators time
    TIME_NOW = TIME_NOW + tmp_time
    
    return TIME_NOW

def getDatetime(time):
    dt = datetime.datetime.fromtimestamp(time+start_time)
    return dt
#Emulator -> Program
#returns conductivity of blood sensor (INT)
def getConductivity():
    print("Blood Conductivity: "+str(blood_conductivity))
    return blood_conductivity
#returns if the reservoir is connected (BOOL)
def reservoirConnected():
    print("Reservoir Connected: "+str(reservoir_connected))
    return reservoir_connected
#returns the level of the reservoir (INT)
def reservoirLevel():
    print("Reservoir Level: "+str(reservoir_level))
    return reservoir_level
#returns the results of the blood sensor self test (BOOL)
def bloodSensorFunctional():
    print("Blood Sensor Functional: "+str(sensor_functional))
    return sensor_functional
#returns the result of the pump self test (BOOL)
def pumpFunctional():
    print("Pump Functional: "+str(pump_functional))
    return pump_functional
#returns the voltage of the battery (INT)
def batteryVoltage():
    print("Battery Voltage: "+str(battery_voltage))
    return battery_voltage
#returns the conductivity of the liquid in the needle (INT)
def needleInternalConductivity():
    print("Needle Conductivity: "+str(needle_conductivity))
    return needle_conductivity
#returns if the needle is connected (BOOL)
def needleConnected():
    print("Needle Connected: "+str(needle_connected))
    return needle_connected
#returns the state of the manual button
def manualButton():
    print("Manual Button State: "+str(button_state))
    return False

#Program -> Emulator
#starts a self test of the pump
def selfTestPump():
    print("Self Test Pump started.")
    return False
#starts a self test of the blood sensor
def selfTestBloodSensor():
    print("Self Test Sensor started.")
    return False
#makes the pump inject 10mL of insulin
def activatePump():
    print("Pump Activated.")
    return False
#sets the state of the alarm
def alarmSetState(state):
    print("Alarm: "+str(state))
    return False
#write text to the display at position (x,y)
def displayWrite(text,pos):
    if(display_print):
        print("Display: "+str(text))
    return False
