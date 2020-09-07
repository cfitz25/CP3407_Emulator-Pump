class Emulator:
    #Emulator -> Program
    #returns conductivity of blood sensor (INT)
    def getConductivity(self):
        return 0
    #returns if the reservoir is connected (BOOL)
    def reservoirConnected(self):
        return False
    #returns the level of the reservoir (INT)
    def reservoirLevel(self):
        return 0
    #returns the results of the blood sensor self test (BOOL)
    def bloodSensorFunctional(self):
        return False
    #returns the result of the pump self test (BOOL)
    def pumpFunctional(self):
        return False
    #returns the level of the battery (INT)
    def batteryLevel(self):
        return 0
    #returns the conductivity of the liquid in the needle (INT)
    def needleInternalConductivity(self):
        return 0
    #returns if the needle is connected (BOOL)
    def needleConnected(self):
        return False
    #returns the state of the manual button
    def manualButton(self):
        return False

    #Program -> Emulator
    #starts a self test of the pump
    def selfTestPump(self):
        return False
    #starts a self test of the blood sensor
    def selfTestBloodSensor(self):
        return False
    #makes the pump inject 10mL of insulin
    def activatePump(self):
        return False
    #sets the state of the alarm
    def alarmSetState(self,state):
        return False
    #write text to the display at position (x,y)
    def displayWrite(self,text,x,y):
        return False
