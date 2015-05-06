mkdir /home/pi/logs
sudo python /home/pi/radiocontrol/sourcecode/radiocontrol.py > /home/pi/logs/radiocontrol.$(date +%F_%R).log 2>&1
sudo halt
