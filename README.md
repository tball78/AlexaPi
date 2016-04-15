# AlexaPi

## Contributors
 
* Clayton Walker 
* Sam Machin
 
## Introduction
 
This is the code needed to turn a Raspberry Pi into a client for Amazon's Alexa service. I have developed this against the Raspberry Pi 2, but I see no reason why it shouldn't run on the other models. Feedback is welcome! 

There are 2 versions I have built, one with a physical push button on a breadboard, and one using a Wii Remote through bluetooth. Hopefully this is detailed enough to make this project easy enough for intermediate or even beginners. The only expertise needed is how to troubleshoot whenever your situation deviates from the happy path that I present to you (where everything just works).
 
## Material Requirements

For Both versions:

* A Raspberry Pi (I use the Raspberry Pi 2 B)
* An SD Card with a fresh install of Raspbian (tested against build 2015-11-21 Jessie. I use a 16GB, although 8GB will be plenty)
* An External Speaker with 3.5mm Jack
* A USB Sound Dongle and Microphone
* Power supply for Pi
* Network connection for Pi (I use a WiFi dongle, although Ethernet can be used instead. Whatever you have available)
* (Optionally) 2 single LEDs Connected to GPIO 24 & 25 (I use a red led on 24, and a green led on 25. Both have 220ohm resistors [Red, Red, Brown, Gold])

For Pushbutton version:
* A pushbutton connected between GPIO 18 and GND (I use a resistor on mine, 1k ohm [Brown, Black, Red, Gold])
* Breadboard and female to male jumper cables

For Wii Remote version:
* Bluetooth dongle (I used a UD100-G03 Bluetooth adapter from Sena, which uses BlueSoleil Bluetooth Software. Literally almost any bluetooth adapter should work, including the built in Raspberry Pi 3 bluetooth [I tried and it works with mine])
* Wii Remote (I use the original version from 2006. I'm sure it would work exactly the same with the newer "motion plus" versions)

## Overview

Basically what we will be doing, is signing up to the Amazon developer program, and registering a device to use the Alexa Voice Service. We will then take a Raspberry Pi, and connect some sort of physical button to it, a microphone, and a speaker. When you run the setup script included in this repo, you will download everything needed (at least this was the case off a fresh build of 2015-11-21 Jessie).

After the set up is complete, you will be able to press and hold a button, ask Alexa a question, and release the button. When the button is released, your recording is sent to Alexa and she sends back the response, which is played through your Pi's speaker. This is all done in `main.py`, which will start up automatically when you apply power to the Pi on every reboot after the set up is complete. 

If you are doing the Wii remote version, I have also made it so the script is constantly looking for a Wii remote connection whenever there isn't one established, so you should'nt need a GUI or ssh into the Pi after everthing is set up. This means even if you need to replace the batteries on the Wii remote, you can still just reconnect the remote and it works, without having to touch the Pi or code at all.

# Setup

## Amazon Developer

First, you need to obtain a set of credentials from Amazon to use the Alexa Voice service. Login at http://developer.amazon.com and go to Alexa, then Alexa Voice Service. 

You need to create a new product type as a Device. For the ID use something like AlexaPi. create a new security profile and under the web settings allowed origins put http://localhost:5000 and as a return URL put http://localhost:5000/code you can also create URLs replacing localhost with the IP of your Pi  eg http://192.168.1.123:5000
Make a note of these credentials you will be asked for them during the install process

### Installation

Boot your fresh Pi and login to a command prompt as root.

Make sure you are in /root

Clone this repo to the Pi
`git clone https://github.com/sammachin/AlexaPi.git`
Run the setup script
`./setup.sh`

Follow instructions....

Enjoy :)

### Issues/Bugs etc.

If your alexa isn't running on startup you can check /var/log/alexa.log for errrors.

If the error is complaining about alsaaudio you may need to check the name of your soundcard input device, use 
`arecord -L` 
The device name can be set in the settings at the top of main.py 

You may need to adjust the volume and/or input gain for the microphone, you can do this with 
`alsamixer`

### Advanced Install

For those of you that prefer to install the code manually or tweak things here's a few pointers...

The Amazon AVS credentials are stored in a file called creds.py which is used by auth_web.py and main.py, there is an example with blank values.

The auth_web.py is a simple web server to generate the refresh token via oAuth to the amazon users account, it then appends this to creds.py and displays it on the browser.

main.py is the 'main' alexa client it simply runs on a while True loop waiting for the button to be pressed, it then records audio and when the button is released it posts this to the AVS service using the requests library, When the response comes back it is played back using mpg123 via an os system call, The 1sec.mp3 file is a 1second silent MP3) I found that my soundcard/pi was clipping the beginning of audio files and i was missing the first bit of the response so this is there to pad the audio.

The LED's are a visual indictor of status, I used a duel Red/Green LED but you could also use separate LEDS, Red is connected to GPIO 24 and green to GPIO 25, When recording the RED LED will be lit when the file is being posted and waiting for the response both LED's are lit (or in the case of a dual R?G LED it goes Yellow) and when the response is played only the Green LED is lit. If The client gets an error back from AVS then the Red LED will flash 3 times.

The internet_on() routine is testing the connection to the Amazon auth server as I found that running the script on boot it was failing due to the network not being fully established so this will keep it retrying until it can make contact before getting the auth token.

The auth token is generated from the request_token the auth_token is then stored in a local memcache with and expiry of just under an hour to align with the validity at Amazon, if the function fails to get an access_token from memcache it will then request a new one from Amazon using the refresh token.








---
 

