#! /usr/bin/env python

import os
import random
import time
import RPi.GPIO as GPIO
import alsaaudio
import wave
import random
from creds import *
import requests
import json
import re
import cwiid
from memcache import Client

#Settings
button = 18 #GPIO Pin with button connected
lights = [24, 25] # GPIO Pins with LED's conneted
device = "sysdefault:CARD=Snowball" # Name of your microphone/soundcard in arecord -L

#Setup
recorded = False
servers = ["127.0.0.1:11211"]
mc = Client(servers, debug=1)
path = os.path.realpath(__file__).rstrip(os.path.basename(__file__))


def internet_on():
    print "Checking Internet Connection"
    try:
        r =requests.get('https://api.amazon.com/auth/o2/token')
        print "Connection OK"
        return True
    except:
        print "Connection Failed"
        return False


def gettoken():
        token = mc.get("access_token")
        refresh = refresh_token
        if token:
                return token
        elif refresh:
                payload = {"client_id" : Client_ID, "client_secret" : Client_Secret, "refresh_token" : refresh, "grant_type" : "refresh_token", }
                url = "https://api.amazon.com/auth/o2/token"
                r = requests.post(url, data = payload)
                resp = json.loads(r.text)
                mc.set("access_token", resp['access_token'], 3570)
                return resp['access_token']
        else:
                return False

def connect_wiimote():
        connected = False
        while connected == False:
                try:
                        wii=cwiid.Wiimote()
                        wii.led = 1
                        connected = True
                except RuntimeError:
                        print "Error opening wiimote connection"
                        time.sleep(10)
                        connected=False
                        wii.rpt_mode = cwiid.RPT_BTN
        return wii

def rumble(wii, kind='once'):
        if kind == 'once':
                wii.rumble = 1
                time.sleep(0.5)
                wii.rumble = 0
        if kind =='twice':
                wii.rumble = 1
                time.sleep(0.2)
                wii.rumble = 0
                time.sleep(0.2)
                wii.rumble = 1
                time.sleep(0.2)
                wii.rumble = 0

def alexa(wii):
        #GPIO.output(24, GPIO.HIGH)
        wii.led = 13
        url = 'https://access-alexa-na.amazon.com/v1/avs/speechrecognizer/recognize'
        headers = {'Authorization' : 'Bearer %s' % gettoken()}
        d = {
                "messageHeader": {
                "deviceContext": [
                        {
                        "name": "playbackState",
                        "namespace": "AudioPlayer",
                        "payload": {
                                "streamId": "",
                                        "offsetInMilliseconds": "0",
                                "playerActivity": "IDLE"
                        }
                        }
				]
                },
                "messageBody": {
                "profile": "alexa-close-talk",
                "locale": "en-us",
                "format": "audio/L16; rate=16000; channels=1"
                }
        }
        with open(path+'recording.wav') as inf:
                files = [
                                ('file', ('request', json.dumps(d), 'application/json; charset=UTF-8')),
                                ('file', ('audio', inf, 'audio/L16; rate=16000; channels=1'))
                                ]
                r = requests.post(url, headers=headers, files=files)
        if r.status_code == 200:
                for v in r.headers['content-type'].split(";"):
                        if re.match('.*boundary.*', v):
                        	boundary =  v.split("=")[1]
                data = r.content.split(boundary)
                for d in data:
                        if (len(d) >= 1024):
                                audio = d.split('\r\n\r\n')[1].rstrip('--')
                with open(path+"response.mp3", 'wb') as f:
                        f.write(audio)
                #GPIO.output(25, GPIO.LOW)
                wii.led = 5
                os.system('mpg123 -q {}1sec.mp3 {}response.mp3'.format(path, path))
                #GPIO.output(24, GPIO.LOW)
                wii.led = 1
        else:
                #GPIO.output(lights, GPIO.LOW)
                wii.led = 1
                for x in range(0, 3):
                        time.sleep(.2)
                        #GPIO.output(25, GPIO.HIGH)
                        wii.led = 9
                        time.sleep(.2)
                        #GPIO.output(lights, GPIO.LOW)
                        wii.led = 1




def start(wii):
        #last = GPIO.input(button)
        buttons = wii.state['buttons']
        if (buttons & cwiid.BTN_A):
                last = 0
        else:
                last = 1
        while True:
        	buttons = wii.state['buttons']
                if (buttons & cwiid.BTN_RIGHT):
                        os.system('node /home/pi/Desktop/turnAllOn.js')
                elif (buttons & cwiid.BTN_LEFT):
                        os.system('node /home/pi/Desktop/turnAllOff.js')
                elif (buttons & cwiid.BTN_A):
                        val = 0
                else:
                        val = 1
                #val = GPIO.input(button)
                if val != last:
                        last = val
                        if val == 1 and recorded == True:
                                rf = open(path+'recording.wav', 'w')
                                rf.write(audio)
                                rf.close()
                                inp = None
                                alexa(wii)
                        elif val == 0:
                                #GPIO.output(25, GPIO.HIGH)
                                wii.led = 9
                                inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, device)
                                inp.setchannels(1)
                                inp.setrate(16000)
                                inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
                                inp.setperiodsize(500)
                                audio = ""
                                l, data = inp.read()
                                if l:
                                        audio += data
                                recorded = True
                elif val == 0:
                        l, data = inp.read()
                        if l:
                        	audio += data
                # ----------------------------------------
                # If Plus and Minus buttons pressed
                # together then rumble and quit.
                if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
                        print '\nClosing connection ...'
                        rumble(wii,'twice')
                        wii.close()
                        # Wait for reconnect
                        wii = connect_wiimote()

if __name__ == "__main__":
        GPIO.setwarnings(False)
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(lights, GPIO.OUT)
        GPIO.output(lights, GPIO.LOW)
        while internet_on() == False:
                print "."
        token = gettoken()
        os.system('mpg123 -q {}1sec.mp3 {}hello.mp3'.format(path, path))
        #wii = connect_wiimote()
        #for x in range(0, 3):
                #time.sleep(.1)
                #GPIO.output(24, GPIO.HIGH)
                #wii.led = 5
                #time.sleep(.1)
                #GPIO.output(24, GPIO.LOW)
                #wii.led = 1
        wii = connect_wiimote()
        start(wii)

