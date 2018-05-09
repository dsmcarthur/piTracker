import sys
import time
import serial
import trackerUtils

class fonaGPS(object):
    global ser
    ser = trackerUtils.openSerialPort()

    def openGPS(self):
        print("Turning on the GPS\r")
        ser.write("AT+CGNSPWR=1\r")  # Turn on the GPS
        time.sleep(1)
        # Check GPS power status is ON!
        while True:
            ser.write("AT+CGNSPWR=?\r")
            gpsPower = ser.readline()
            if "1" in gpsPower:
                print("GPS is powered on")
                return True
            if "ERROR" in gpsPower:
                print("GPS has no power")
                print("GPS is off. Turning on...")
                #writeToFile('Sys_Log.txt', ("GPS status is " + gpsPower))
                ser.write("AT+CGNSPWR=1")  # Power on GPS module
        time.sleep(0.5)
        ser.write("AT+CGNSRST=1\r")  # GPS reset set to hot start mode
        return True
        
    # Check to see if the GPS has aquired any satellites
    def getGPSFix(self):
        print("Checking for GPS Fix")
        ser.write("AT+CGPSSTATUS?\r")
        gpsFix = ser.readline()
        while "+CGPSSTATUS: Location Not Fix" in gpsFix:
            time.sleep(5) # Wait for GPS fix
            ser.write("AT+CGPSSTATUS?\r")
        print("GPS location is fixed")
        return True    
        
    # Get GPS Coordinates
    def getGPS(self):
        print("Getting GPS Data\r")
        while True:
            ser.write("AT+CGNSINF \r")
            global gpsCoord
            gpsCoord = ser.readline()
            if "+CGNSINF: " in gpsCoord:  # 1 = gps fix, 0 = no fisx
                print(gpsCoord)
                return gpsCoord
                return True
            if "ERROR" in gpsCoord:
    #                writeToFile('Sys_Log.txt', ("Error in GPS Coord: " + gpsCoord))
                ser.write("AT+CGNSINF=0\r")

    # converts Rx data to Decimal Degree format
    def convertGPS(self, gpsV1):
        array = gpsV1.split(",")
        #### Format from DDMM.MMMMMM to DD MM.MMMMMM
        # Latitude
        lat = array[1]
        DDlat = int(float(lat)/100)            # Retrieves DD
        MMlat = float(lat)-DDlat*100
        MMlat = MMlat/60
        Lat = DDlat+MMlat
        Lat = str(Lat)
        print(Lat)
    
        # Longitude
        lon = array[2]                      # text array pulling longitude
        DDlon = int(float(lon)/100)
        MMlon = float(lon)-DDlon*100
        MMlon = MMlon/60
        Lon = DDlon+MMlon
        Lon = str(Lon)
        print(Lon)
    
        # Altitude
        global alt
        alt = array[3]
        print("GPS Altitude is " + alt)
    
        # Time UTC
        global utc
        utc = array[4]
        print("UTC time is " + utc)
    
        # Speed in knots
        global speed
        speed = array[7]
        print("speed in knots is " + speed)
    
        # Heading in Degrees
        global heading
        heading = array[8]
        print("Heading is " + heading + " degrees")
    
        # Google Maps link
        global gMapsLink
        gMapsLink = ("https://www.google.com/maps/search/?api=1&query=" + Lat + "," + Lon)
        print(gMapsLink)
        return gMapsLink
    
        # Write to GPS Log file
        gpsMsg1 = (Lat + "," + Lon + " Fix Coords in Decimal Degree")
        gpsMsg2 = ('Altitude: ' + alt + ' meters, Speed: ' + speed + ' knots, Heading: ' + heading + ' Time: ' + utc2 + ' UTC')
#        writeToFile(gpsFileName, gpsMsg1)
#        writeToFile(gpsFileName, gpsMsg2)     
#        writeToFile(gpsFileName, gpsV1)                 # Writing Original data to file for T/S purposes
#        writeToFile(gpsFileName, gMapsLink)             # Write Map Link to file

        
    
        # Close GPS
        def closeGPS():
            ser.write("AT+CGNSPWR=0")        # Probably won't need, but hey...
            ser.close()
