from Emulator import *
import socket
class PumpProgram:
    #screen positions
    DISPPOS_SUGAR = (0,0)
    DISPPOS_RESERV = (20,0)
    DISPPOS_TOTAL_INSULIN = (40,0)
    DISPPOS_BATTERY = (60,0)
    DISPPOS_LAST_INJECT = (20,20)
    DISPPOS_MESSAGES = (0,40)  
    #blood sugar levels
    SAFE_SUGAR_LEVEL = 20
    UNSAFE_SUGAR_LEVEL = 40
    blood_sugar_levels = [0, 0, 0]
    MAX_BLOOD_SUGAR = 3
    #insulin levels
    INSULIN_MAX_DOSAGE = 50
    INSULIN_MIN_DOSAGE = 10
    INSULIN_MAX_PER_DAY = 500
    last_injection = (0,0)
    total_insulin_today = 0
    #battery
    BATT_MAX_VOLTAGE = 3.3
    BATT_MIN_VOLTAGE = 1.2
    battery_level = 2
    #reservoir
    RESERVOIR_MIN_LEVEL = 10
    reservoir_level = 0

    #device info
    DEVICE_MODEL = "Prototype_1"
    #other
    NEEDLE_EMPTY_CONDUCTIVITY = 20
    messages = []
    MAX_MESSAGES = 5
    message_ind = 0
    trigger_manual = False
    



    def __init__(self,emulator):
        self.e = emulator
        return
    def start_server(self,port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("localhost", port))
        self.sock.listen(1)
        self.sock.setblocking(0)
    def stop_server(self):
        self.sock.close()
    def connectionSetup(self,IP,port):
        self.IP = IP
        self.port = port
    def recvProcess(self,sock):
        message = sock.recv(1024).decode()
        if(message == "TRIGGER_MANUAL"):
            self.trigger_manual = True
        sock.close()
    def send(self,message):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.IP, self.port))
        except:
            return False
        s.send(message.encode())
        s.close()
        return True
    def mainLoop(self):
        last_time_30s = self.e.getTime()
        last_time_10min = last_time_30s
        last_time_5s = last_time_30s
        while True:
            tmp_time = self.e.getTime()
            try:
                (clientsocket, address) = self.sock.accept()
                self.recvProcess(clientsocket)
            except:
                p = 0
            #run if it has been atleast 30 seconds since last run
            if(tmp_time-last_time_5s >= 5):
                last_time_5s = tmp_time
                print("####################################")
                self.loop5Second()

            #run if it has been atleast 30 seconds since last run
            if(tmp_time-last_time_30s >= 30):
                last_time_30s = tmp_time
                print("####################################")
                self.loop30Second()

            #run if it has been atleast 10 minutes since last run or if a manual trigger has been activated
            if(tmp_time-last_time_10min >= 10*60 or self.trigger_manual):
                self.trigger_manual = False
                last_time_10min = tmp_time
                print("####################################")
                self.loop10Minute()
            time.sleep(1)
        return

    def loop5Second(self):

        #display blood sugar levels
        if(len(self.blood_sugar_levels) > 0):
            self.e.displayWrite("sugar:\r\n"+str(self.blood_sugar_levels[-1])+" cc/L", self.DISPPOS_SUGAR)
        else:
            self.e.displayWrite("sugar:\r\n--cc/L", self.DISPPOS_SUGAR)

        #display how much is left in the reservoir
        self.e.displayWrite("left:\r\n"+str(self.reservoir_level)+"mL", self.DISPPOS_RESERV)

        #display how much insulin has been given today
        self.e.displayWrite("total:\r\n"+str(self.total_insulin_today)+"mL", self.DISPPOS_TOTAL_INSULIN)

        #display battery left
        self.e.displayWrite("battery:\r\n"+str(self.battery_level)+"%", self.DISPPOS_BATTERY)

        #if the last injection has occured display it otherwise display dummy info
        write_string = "last injection:\r\n"
        if(self.last_injection[0] != -1):
            dt = self.e.getDatetime(self.last_injection[0])

            write_string += str(self.last_injection[1])+"mL\r\n("+str(dt)+")"
        else:
            write_string += "--mL\r\n()"
        self.e.displayWrite(write_string, self.DISPPOS_LAST_INJECT)
        write_string = "("

        #if messages exist then display it otherwise display dummy info
        if(len(self.messages) > 0):
            time,message = self.messages[self.message_ind]
            self.message_ind += 1
            if(self.message_ind >= len(self.messages)):
                self.message_ind = 0
            dt = self.e.getDatetime(time)
            write_string += str(dt.time())+") "+str(message)
        else:
            write_string += ") ---------------"
        self.e.displayWrite(write_string, self.DISPPOS_MESSAGES)

    def loop30Second(self):
        print("LOOP 30 SEC: ",self.e.getTime())

        #check if the blood sensor is working, log error if not

        self.e.selfTestBloodSensor()
        blood_result = self.e.bloodSensorFunctional()
        if(not blood_result):
            self.logIssue("Sensor Test Failed.")

        #check if the pump is working, log error if not
        self.e.selfTestPump()
        pump_result = self.e.pumpFunctional()
        if(not pump_result):
            self.logIssue("Pump Test Failed.")

        #check if the needle is connected, log error if not
        needle_result = self.e.needleConnected()
        if(not needle_result):
            self.logIssue("Needle not connected.")

        #check if reservoir is connected, log error if not
        reservoir_result = self.e.reservoirConnected()
        if(not reservoir_result):
            self.logIssue("Reservoir not connected.")

        #check to see if there is insulin or something else is in the needle
        if(self.e.needleInternalConductivity() > self.NEEDLE_EMPTY_CONDUCTIVITY):
            self.logIssue("Needle has a blockage.")

        #check if the reservoir is leaking and check if it needs replacing
        old_reservoir_level = self.reservoir_level
        self.reservoir_level = self.e.reservoirLevel()
        if(old_reservoir_level != self.reservoir_level):
            self.logIssue("Reservoir is leaking.")

        if(self.reservoir_level < self.RESERVOIR_MIN_LEVEL):
            self.logIssue("Reservoir is almost empty.")

        battery_voltage = self.e.batteryVoltage()
        if(battery_voltage < self.BATT_MIN_VOLTAGE):
            self.logIssue("Battery voltage is low.")

        #do other non error things
        #get battery voltage
        self.battery_level = self.batteryVolt2Level(battery_voltage)

        #log general device info
        self.logDeviceInfo(self.battery_level,self.reservoir_level)

    def loop10Minute(self):
        

        #get the conductivity and turn it into blood sugar
        conductivity = self.e.getConductivity()
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

        #make print message
        message_str = "Blood Levels: "
        for i in range(self.MAX_BLOOD_SUGAR):
            message_str += "  ["+str(i)+"] "+str(self.blood_sugar_levels[i])
        self.e.print("Blood", message_str)
        self.e.print("Blood", "RoC: "+str(rate_of_change1)+", "+str(rate_of_change2))
        #if blood sugar is above safe levels and the blood sugar level is increasing at an increasing rate then inject insulin
        if(blood_sugar >= self.SAFE_SUGAR_LEVEL and rate_of_change1 > 0 and rate_of_change1 > rate_of_change2):
            inject_insulin = True
            self.e.print("Blood", "Insulin allowed. Blood sugar above SAFE and rate of change increasing increasingly.")
        #if blood sugar is above unsafe levels and the blood sugar is not decreasing at an increasing rate then inejct insulin
        if(blood_sugar >= self.UNSAFE_SUGAR_LEVEL and not (rate_of_change1 < 0 and rate_of_change1 < rate_of_change2)):
            inject_insulin = True
            self.e.print("Blood", "Insulin allowed. Blood sugar above HIGH and rate of change not decreasing increasingly.")
        #if injection isnt needed then end the function
        if(not inject_insulin):
            self.e.print("Insulin", "Insulin not needed.")
            return

        #get the insulin amount, check if its too small or too big and then turn it into steps of 10mL, round down
        insulin_amount = self.sugar2insulin(blood_sugar)
        if(insulin_amount < self.INSULIN_MIN_DOSAGE):
            insulin_amount = self.INSULIN_MIN_DOSAGE
            self.e.print("Insulin", str(insulin_amount)+"mL is too low, increasing to "+str(self.INSULIN_MIN_DOSAGE)+".")
        elif(insulin_amount > self.INSULIN_MAX_DOSAGE):
            insulin_amount = self.INSULIN_MAX_DOSAGE
            self.e.print("Insulin", str(insulin_amount)+"mL is too high, decreasing to "+str(self.INSULIN_MAX_DOSAGE)+".")

        #constrain the amount of insulin given per day
        if(self.total_insulin_today + insulin_amount > self.INSULIN_MAX_PER_DAY):
            insulin_amount = self.INSULIN_MAX_PER_DAY - self.total_insulin_today
            self.e.print("Insulin", "Had "+str(self.total_insulin_today)+"mL of "+str(self.INSULIN_MAX_PER_DAY)+"mL, decreasing dosage to "+str(insulin_amount)+"mL.")
        insulin_steps = insulin_amount // 10
        self.e.print("Insulin", str(insulin_amount)+"mL converted to "+str(insulin_steps)+" of 10mL.")
        #check if insulin value is still valid and needs to be injected
        if(insulin_steps <= 0):
            #negative or no steps does not require injection
            self.e.print("Insulin", "Zero steps so no insulin is needed.")
            return
        
        #get the current reservoir level, used to check if the correct amount of insulin was injected
        current_reservoir_level = self.e.reservoirLevel()

        #inject the required amount of insulin
        for i in insulin_steps:
            self.e.activatePump()
            time.sleep(0.1)

        #get the new reservoir level and the difference between it and the old reservoir level
        self.reservoir_level = self.e.reservoirLevel()
    
        reservoir_difference = current_reservoir_level-self.reservoir_level

        #log the amount of insulin injects and how much was meant to be, add the actual insulin given to the daily amount given
        self.logInsulinInjected(reservoir_difference, insulin_steps*10,False)
        self.total_insulin_today += reservoir_difference
        self.last_injection = (self.e.getTime(),reservoir_difference)

        #check if the amount of insulin that was injected was how much that left the reservoir
        if(reservoir_difference != insulin_steps*10):
            self.logIssue("Incorrect amount of insulin amount injected.")

    def logInsulinInjected(self,actually_injected, desired_amount, is_manual):
        self.e.print("Insulin Log", "{ Actual: "+str(actually_injected)+"mL, Desired: "+str(desired_amount)+", Manual: "+str(is_manual)+" }.")
        self.send("INSULIN "+str(self.e.getDatetime(self.e.getTime()))+" "+str(actually_injected)+" "+str(desired_amount)+" "+str(is_manual))

        return
    def logIssue(self,issue):
        self.messages.append((self.e.getTime(),issue))
        if(len(self.messages) >= self.MAX_MESSAGES):
            self.messages.pop(0)
        #later add connection and send to app
        self.send("ISSUE "+str(self.e.getDatetime(self.e.getTime()))+" {{{"+str(issue)+"}}}")

        #trigger alarm
        self.e.alarmSetState(True)
        time.sleep(0.5)
        self.e.alarmSetState(False)
        self.e.print("Issue Log",issue)
        
        return True
    def logBloodSugar(self,blood_sugar):
        self.send("BLOOD "+str(self.e.getDatetime(self.e.getTime()))+" "+str(blood_sugar))

        self.e.print("Blood Log",str(blood_sugar)+"cc/L }.")
        return
    def logDeviceInfo(self,battery_level, reservoir_level):
        self.send("DEVICE_INFO "+str(self.e.getDatetime(self.e.getTime()))+" "+str(round(battery_level,1))+" "+str(reservoir_level))
        self.e.print("Info Log","{"+str(round(battery_level,0))+"%, "+str(reservoir_level)+"mL }.")
        return
    def conductivity2sugar(self,conductivity):

        #convert conductivity into blood sugar
        res = conductivity
        self.e.print("Blood",str(conductivity)+"Ohm-m -> "+str(res)+"cc/L.")
        return res
    def sugar2insulin(self,sugar):

        #calculate insulin from sugar
        res = sugar
        self.e.print("Insulin",str(sugar)+"cc/L -> "+str(res)+"mL.")
        return res
    def batteryVolt2Level(self,volt):
        
        res = (volt-self.BATT_MIN_VOLTAGE)/(self.BATT_MAX_VOLTAGE-self.BATT_MIN_VOLTAGE) * 100
        self.e.print("Battery",str(volt)+"V -> "+str(round(res,0))+"%.")
        return res
    
e = Emulator("Emulator1")
e.printSetup(20)
p = PumpProgram(e)
p.connectionSetup("localhost", 5555)
e.time_multiplier = 5
e.display_print = False
p.mainLoop()

# p.send("Test 1")
# p.send("Test 2")
