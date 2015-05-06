#Vintage Radio Control
##Martin O'Hanlon (martin@ohanlonweb.com)
##http://www.stuffaboutcode.com

##Description
A control program for a [Raspberry Pi](http://www.raspberrypi.org) and [Volumio](http://volumio.org) powered Vintage Radio 

For more information see [www.stuffaboutcode.com/p/raspberry-pi-volumio-vintage-radio](http://www.stuffaboutcode.com/p/raspberry-pi-volumio-vintage-radio)

##Structure
* init.d
  * runRadioControl - init.d script to run the radio control application
  * runRadioControl.add - script which will copy init.d script to /etc/init.d and add it to startup
  * runRadioControl.remove - script to remove the application

* poccode - proof of concept code I used to understand how stuff worked

* scripts - some random scripts
  * unmuteiqamp.sh - a script to unmute the IQAudio Amp+
  * muteiqamp.sh - a script to mute the IQAudio Amp+
  * radiocontrol.sh - a script to start the radio control app and shutdown the pi when it exits
 
* sourcecode - source code for the radio control
  * radiocontrol.py - main program
  * analogueswitch.py - class for managing an 'analogue switch'
  * event.py - class to hold a events
  * KY040.py - class for reading a KY0404 rotary encoder module
  * MCP3008.py - class for reading data from an MCP3008 analogue to digital converter
  * onoffswitch.py - class used to raise events from the the on/off switch 
  * playlistselector.py - class used to raise events from the playlist selector
  * skiptrackpause.py - class used to raise events form the rotary encoder
  * volumecontrol.py - class used to raise events from the volume control

##Install

This assumes you are installing it on a volumio image and using an IQAudio DAC+ / AMP+

###Enable DAC

sudo nano /boot/config.txt

add:

dtoverlay=iqaudio-dacplus

###Enable SPI

sudo nano /boot/config.txt

add:

dtparam=spi=on

Reboot and check its running:

lsmod | grep spi_

###Install python modules

####Setuptools

wget https://bootstrap.pypa.io/ez_setup.py -O - | sudo python

####python-mpd2

git clone git://github.com/Mic92/python-mpd2.git
cd python-mpd2
sudo python setup.py install

####rPi.GPIO

```wget http://sourceforge.net/projects/raspberry-gpio-python/files/raspbian-wheezy/python-rpi.gpio_0.5.11-1_armhf.deb/download

mv download python-rpi.gpio_0.5.11-1_armhf.deb

sudo dpkg -i python-rpi.gpio_0.5.11-1_armhf.deb```

####py-spidev

```sudo apt-get install python2.7-dev

sudo apt-get install gcc

mkdir py-spidev

cd py-spidev

wget https://github.com/Gadgetoid/py-spidev/archive/master.zip

unzip master.zip

rm master.zip

cd py-spidev-master

sudo python setup.py install```

##Run

```sudo python sourcecode/radiocontrol.py```

##Version history
* 0.1 - Initial stable version
