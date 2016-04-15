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
* (Optionally) 2 single LEDs Connected to GPIO 24 & 25 (I use a green led on 24, and a red led on 25. Both have 220ohm resistors [Red, Red, Brown, Gold])

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

First, you need to obtain a set of credentials from Amazon to use the Alexa Voice service. Login at http://developer.amazon.com and go to Apps and Services, then Alexa, then Alexa Voice Service (Get Started). 

Choose Register a Product Type > Device. Here is an example of what you can do in the setup. Feel free to us my exact setup names, as it doesn't really matter. Just make sure you use the SAME NAME that you create because it matters. That's why it's easiest to keep the same name for everything.

Device Type ID: AlexaPi
Display Name: AlexaPi

Hit Next. Click on Security Profile -> Create a new profile.

Security Profile Description: AlexaPi

Hit Save. It will then create a Security Profile ID , Client ID, and Client Secret for you. These are unique and what will be used to authenticate your device for use with the service. *Make a note of these credentials, you will be asked for them during the install process.*

While under Security Profile, go on the Web Settings tab.

Allowed Origins: 
http://localhost:5000
http://IPaddressofyourPi:5000

Allowed Return URLs:
http://localhost:5000/code
http://IPaddressofyourPi:5000/code

*For some reason, localhost would never work for me, but adding the actual IP of my Pi did. You can add both just to be safe, it won't hurt anything.

Hit Save.

Device Details:
-You don't need an image
-Category: Other
-Description: AlexaPi
-Expected timeline: Longer than 4 months/TBD
-Devices planned for commercialization: 0

Hit Next

I personally hit NO for the Amazon Music. If you choose YES and have issues, I would not be an expert on what's going on.

# Raspberry Pi Setup

Now that you have signed up for the Alexa Service, go ahead and boot up your Pi. Make sure you have internet connection. Feel free to expand the filesystem, change the timezone, etc. under `sudo raspi-config`. While under hear, I went to advanced settings, audio, and forced 3.5mm jack for the speaker. You can use HDMI for the audio, but I went with a speaker. I also go ahead and set my microphone as the default through audio settings.

## Bluetooth Setup

Next, go ahead and install bluetooth, even if you aren't going to be doing the Wii remote version. In case you change your mind later, this saves time.

`sudo apt-get install --no-install-recommends bluetooth`

Check the status with `sudo service bluetooth status` to make sure everything is working properly.

You can test the Wii Remote after you clone the repo, by `cd wii_remote_examples/` and running one of the scripts.
`python wii_remote.py` just tests the button presses. Connect by pressing 1 and 2 at the same time.
`python wiimote.py` is a little more advanced, but basically works the same. The player 1 LED will light up when you are successfully connected, and you can even view the Wii mote accelerometer data if you hold down the home button.

## Code Installation

Login to a terminal as root. Make sure you are in /root

`sudo su`
`cd /root`

Clone this repo to the Pi
`git clone https://github.com/cwalk/AlexaPi.git`

*THE DEFAULT `main.py` USES THE WII REMOTE. IF YOU WANT TO USE THE PUSHBUTTON, RENAME THE `mainPushButton.py` TO `main.py` AND RENAME THE OTHER TO `mainWiiRemote.py` INSTEAD.*

Run the setup script
`./setup.sh`

Follow instructions....you will need to copy and paste your Device Type ID, Security Profile Description, Security Profile ID , Client ID, and Client Secret. If you followed the instructions exactly above, Device Type ID and Security Profile Description would both be 'AlexaPi'. The rest is unique to your device.

After the setup script finished running, you will need to open a browser to http://IPaddressofyourPi:5000

This will take you to the Amazon Developer login scree. Login with your account credentials, and agree that this is your device. Then an authentication token will be displayed in the browser. The setup script automatically takes this token, and appends it to your cred.py file, so you dont need to do anything else. Close the browser.

You can now quit out of the setup with Control + C. You should be able to test the code with `python main.py` and hear Alexa say 'Hello'. Feel free to close the terminal, and shutdown your Pi.

## Circuit Setup

If you only want to use the Wii remote, you can skip this part. For those of you wanting to use a pushbutton on a breadboard, OR wanting the optional LEDS, listen up.

The circuit diagram provided below works as follows:
-A push button is wired between GND and BCM Pin 18. So a wire goes from GND on the Pi, to a 1k ohm resistor on the bread board. The other leg of the resistor is with the first leg of the push button. The second leg of the pushbutton is wired to Pin 18.

-A green LED has a wire from GND to one leg of a 220ohm resistor. The other leg of the resistor connects to the 1st leg of the LED. The 2nd leg of the LED is wired to BCM PIN 24.

-A red LED has a wire from GND to one leg of a 220ohm resistor. The other leg of the resistor connects to the 1st leg of the LED. The 2nd leg of the LED is wired to BCM PIN 25.

There are 2 types of GPIO readings. BCM and BOARD. BCM uses a specific number, while BOARD uses the actual physical pin number. *This python script uses BCM, so don't use the BOARD layout!* Here is a link to the GPIO on the Raspberry Pi: https://pinout.xyz



# Usage

After you set up everything above, you can finally apply power to your Pi. You should hear Alexa say 'Hello', which means `main.py` is successfully running on reboot. If you decided to wire up the optional LEDs, the green LED will blink 3 times when Alexa is ready to be asked questions.

To connect your Wii remote, hold the 1 and 2 buttons at the same time for a couple seconds, and let go. If it connects successfully, you should see the Player 1 LED light up.

Here is the process if you wired up the optional LEDs. You press a button (pushbutton, or A button on Wii remote) and the red LED turns on. Hold your button, ask your question, and let go of the button. When you let go of the button, the green LED should come on. This lets us know we captured your recording, and it's being sent to Alexa. The red LED should turn off when it's finished processing. Then Alexa will speak her response through the speaker. The green LED will turn off when she is done speaking, and you are free to ask another question. 

If the client gets an error back from AVS, then the Red LED will flash 3 times. This usually means something went wrong (is your pushbutton snug in the breadboard? Mine popped out once or twice during recording, causing this to happen).

In case you don't know much about Alexa, here is a good resource for how to talk to her: https://www.amazon.com/gp/help/customer/display.html?nodeId=201549800

### Issues/Bugs etc.

If your alexa isn't running on startup you can check /var/log/alexa.log for errrors.

Check to see if the python service is running by typing this command in the terminal: `ps aux | grep python`

If there is an error complaining about alsaaudio you may need to check the name of your soundcard input device, use 
`arecord -L`. The device name can be set in the settings at the top of `main.py`, under the device variable.

You may need to adjust the volume and/or input gain for the microphone, you can do this with `alsamixer`.

### Advanced Install

For those of you that prefer to install the code manually or tweak things here's a few pointers...

The Amazon AVS credentials are stored in a file called creds.py which is used by auth_web.py and main.py, there is an example with blank values.

The auth_web.py is a simple web server to generate the refresh token via oAuth to the amazon users account, it then appends this to creds.py and displays it on the browser.

main.py is the 'main' alexa client it simply runs on a while True loop waiting for the button to be pressed, it then records audio and when the button is released it posts this to the AVS service using the requests library, When the response comes back it is played back using mpg123 via an os system call (The 1sec.mp3 file is a 1second silent MP3. I found that my soundcard/pi was clipping the beginning of audio files and I was missing the first bit of the response so this is there to pad the audio).

The LED's are a visual indictor of status, I used separate LEDS. Green is connected to BCM GPIO 24 and red to BCM GPIO 25. When recording the RED LED will be lit. When the file is being posted and waiting for the response, both LED's are lit. When the response is played, only the Green LED is lit. If the client gets an error back from AVS, then the Red LED will flash 3 times.

The internet_on() routine is testing the connection to the Amazon auth server as I found that running the script on boot it was failing due to the network not being fully established so this will keep it retrying until it can make contact before getting the auth token.

The auth token is generated from the request_token the auth_token is then stored in a local memcache with and expiry of just under an hour to align with the validity at Amazon, if the function fails to get an access_token from memcache it will then request a new one from Amazon using the refresh token.
