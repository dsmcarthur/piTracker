import sys
import time
import serial

class fonaSMS(object):
    global ctrlZ
    ctrlZ = '\x1a'
        
    # CHECK FONA
    def checkFONA(self):
        # SETUP SERIAL MODEM FOR PI/FONA
        while True:
            ser.write("AT\r")
            fonaStatus = ser.readline()
            if "OK" in fonaStatus:
                print("The FONA is " + fonaStatus)
                return True
            if "ERROR" in fonaStatus:
             #   writeToFile(logFileName, ("FONA status is " + fonaStatus)) 
                print("The FONA is " + fonaStatus)
        return True
            
    def initSMS(self):
        smsStatus = "SMS Status Default"
        while True:
            ser.write(b'AT+CMGF=1\r')            # Set SMS mode to TEXT
            smsStatus = ser.readline()
            if "OK" in smsStatus:
                print("SMS status is " + smsStatus)
                return True
            if "ERROR" in smsStatus:
                #writeToFile(logFileName, (("SMS status is " + smsStatus)))
                ser.write(b'AT+CMGF=1\r')
            time.sleep(1)
    
    # Send SMS
    def sendSMS(self, recipient, message):
        try:
            def get_num(x):
                return str("".join(ele for ele in x if ele.isdigit()))
        
            time.sleep(0.5)
            ser.write('AT\r\n')
            print(ser.readline())
            time.sleep(0.5)
            ser.write('AT+CMGF=1\r\n')
            time.sleep(0.5)
            ser.write('AT+CMGW="'+ recipient +'"\r\n')
            out = ''
            time.sleep(1)
            while ser.inWaiting() > 0:
                out += ser.read(1)
            if out != '':
                print('>>' + out)
            ser.write(message)
            ser.write('\x1a')
            out = ''
            time.sleep(1)
            while ser.inWaiting() > 0:
                out += ser.read(1)
            if out != '':
                print('>>' + out)
                number = get_num(out)
                ser.write('AT+CMSS='+number+'\r\n')
            out = ''
            time.sleep(1)
            while ser.inWaiting() > 0:
                out += ser.read(1)
            if out != '':
                print('>>' + out)
            #print("Sending SMS message " + smsMessage + " to " + smsRecipient)
            #ser.write('ATZ') # Reset the FONA
            #ser.write('AT+CMGF=1\r\n')
            #sleep(0.5)
            #ser.write('AT+CMGS=')
            #ser.write(smsRecipient)
            #ser.write('\r\n')
            #ser.write(smsMessage.encode())
            #ser.write('\x1a')
            #sleep(3)
            #smsStatus = ser.readlines()
            #while "OK" in smsStatus:
            #    print("Sending status is: " + smsStatus)
        finally:
            ser.close()