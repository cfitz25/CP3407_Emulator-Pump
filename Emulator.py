import time
import datetime
start_time = time.time()
last_time = 0
TIME_NOW = 0
time_multiplier = 10
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
def setTimeMultiplier(val):
    global time_multiplier
    time_multiplier = val
def getDatetime(time):
    dt = datetime.fromtiestamp(time+start_time)
    return dt
#Emulator -> Program
#returns conductivity of blood sensor (INT)
def getConductivity():
    return 0
#returns if the reservoir is connected (BOOL)
def reservoirConnected():
    return False
#returns the level of the reservoir (INT)
def reservoirLevel():
    return 0
#returns the results of the blood sensor self test (BOOL)
def bloodSensorFunctional():
    return False
#returns the result of the pump self test (BOOL)
def pumpFunctional():
    return False
#returns the voltage of the battery (INT)
def batteryVoltage():
    return 0
#returns the conductivity of the liquid in the needle (INT)
def needleInternalConductivity():
    return 0
#returns if the needle is connected (BOOL)
def needleConnected():
    return False
#returns the state of the manual button
def manualButton():
    return False

#Program -> Emulator
#starts a self test of the pump
def selfTestPump():
    return False
#starts a self test of the blood sensor
def selfTestBloodSensor():
    return False
#makes the pump inject 10mL of insulin
def activatePump():
    return False
#sets the state of the alarm
def alarmSetState(state):
    return False
#write text to the display at position (x,y)
def displayWrite(text,pos):
    return False
