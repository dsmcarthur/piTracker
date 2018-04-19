import sys
import time
import serial

class fonaGPS(object):
        
    def __init__(self):
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
               # writeToFile('Sys_Log.txt', ("GPS status is " + gpsPower))
                ser.write("AT+CGNSPWR=1")  # Power on GPS module
        time.sleep(0.5)
        ser.write("AT+CGNSRST=1\r")  # GPS reset set to hot start mode
        
    #def openGPS(self):
    #    print("Turning on the GPS\r")
    #    ser.write("AT+CGNSPWR=1\r")  # Turn on the GPS
    #    time.sleep(1)
        # Check GPS power status is ON!
    #    while True:
    #        ser.write("AT+CGNSPWR=?\r")
    #        gpsPower = ser.readline()
    #        if "1" in gpsPower:
    #            print("GPS is powered on")
    #            return True
    #        if "ERROR" in gpsPower:
    #            print("GPS has no power")
    #            print("GPS is off. Turning on...")
               # writeToFile('Sys_Log.txt', ("GPS status is " + gpsPower))
    #            ser.write("AT+CGNSPWR=1")  # Power on GPS module
    #    time.sleep(0.5)
    #    ser.write("AT+CGNSRST=1\r")  # GPS reset set to hot start mode
    #    return True
        
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
        global deg
        deg = chr(37)
        array = gpsV1.split(",")
        #### Format from DDMM.MMMMMM to DD MM.MMMMMM
        # Latitude
        global latDeg
        global latMin
        lat = array[1]  # text array pull latitude from input
        floatLat = float(lat)  # text to float
        floatLat = floatLat / 100  # float math
        strLat = str(floatLat)  # DD to string
        arrayLat = strLat.split(".")  # split string along .
        latDeg = arrayLat[0]  # DD array member
        latDeg = float(latDeg)
        latMin = arrayLat[1]  # MMMMMM array member
        latMin = float(latMin)  # str to float
        latMin = latMin / 60                  
        latMin = latMin / 10000               
        latitude = latDeg + latMin
        latitude = str(latitude)
        print(latitude + " is decimal degree latitude")
    
        # Longitude
        global lonDeg
        global lonMin
        lon = array[2]  # text array pulling longitude from ,,,
        floatLon = float(lon)  # text to float
        floatLon = floatLon / 100  # float math
        strLon = str(floatLon)
        arrayLon = strLon.split(".")  # split DDMM.MMMM to DD.MMMMMMM along .
        lonDeg = arrayLon[0]  # lonDeg = DD
        lonDeg = float(lonDeg)              
        lonMin = arrayLon[1]  # lonMin = MMMMMM
        lonMin = float(lonMin)  # str to float
        lonMin = lonMin / 60
        lonMin = lonMin / 10000
        longitude = lonDeg + lonMin
        longitude = str(longitude)
        print(longitude + " is decimal degree longitude")
    
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
    
        # Write parsed GPS to Log file
        gpsMsg1 = (latitude + "," + longitude + " Fix Coords in Decimal Degree")
    #    writeToFile('GPS_Log.txt', gpsMsg1)
        gpsMsg2 = ('Altitude: ' + alt + ' meters, Speed: ' + speed + ' knots, Heading: ' + heading + ' Time: ' + utc + ' UTC')
       # writeToFile('GPS_Log.txt', gpsMsg2) 
        
        # Google Maps link
        global gMapsLink
        gMapsLink = ("https://www.google.com/maps/@" + latitude + "," + longitude)
        print(gMapsLink)
        return gMapsLink
    
        # Close GPS
        def closeGPS():
            ser.write("AT+CGNSPWR=0")        # Probably won't need, but hey...
            ser.close()
