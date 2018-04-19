import serial
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from curses.ascii import ascii
from time import sleep
from FONA_GPS import fonaGPS
from FONA_SMS import fonaSMS

# Fetch the service account key JSON file contents
cred = credentials.Certificate('/home/pi/piTracker/node-client-app/service-account.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pitracker-1521337480618.firebaseio.com'
})

# As an admin, the app has access to read and write all data, regradless of Security Rules
ref = db.reference('restricted_access/secret_document')
print(ref.get())
    
#Get GPS Data
GPSData = fonaGPS()
GPSData.openGPS()
GPSData.getGPSFix()
rawGPS = GPSData.getGPS()
fullLocData = GPSData.convertGPS(rawGPS)

# Send GPS data to text
device = fonaSMS()
device.checkFONA()
device.initSMS()

smsRecipient = "6145882596" #Ron's ser
smsMessage = fullLocData

device.sendSMS(smsRecipient, smsMessage)
