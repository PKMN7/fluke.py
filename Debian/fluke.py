import subprocess
import csv
import time
import os

def obtainSwitchData():
    subprocess.call('sudo ifconfig enp0s25 down',shell=True)
    subprocess.call('sudo ifconfig enp0s25 hw ether aa:bb:bb:bb:bb:bb',shell=True)
    subprocess.call('sudo ifconfig enp0s25 up',shell=True)
    data = subprocess.check_output(['./fluke.sh'])
    name = data.split(',')[0]
    address = data.split(',')[1]
    port = data.split(',')[2]
    name = name.strip()
    port = port.strip()
    port = port.strip('GigabitEthernet')
    address = address.strip()
    print address

    csvfile = "switch.csv"
    if(name != ""):
        room = raw_input('Enter the room: ')
        jack = raw_input('Enter the jack: ')
        notes = raw_input('Anything of note?: ')
        allData = [room,jack,port,name,address,notes]
        with open('switch.csv','a+b') as file:
            #if os.path.isfile(csvfile) == False:
                #writer = csv.DictWriter(file, fieldnames = ["Room", "Jack #", "Port","Switch Name", "Switch IP"], delimiter = ';')
                #writer.writeheader()
            for line in allData:
                file.write(line+",")
            file.write('\n')
        return True
    else:
        return False

def getEth0Status():
    wiredConnection = subprocess.check_output('ethtool enp0s25 | grep "Link"',shell=True)
    wiredConnection = wiredConnection.split(' ')[2]
    wiredConnection = wiredConnection.strip()
    print len(wiredConnection)
    if (str(wiredConnection)=="yes"):
        return True
    else:
        print str(wiredConnection)

starttime=time.time()
while True:
    if (getEth0Status() == True):
        subprocess.call('sudo ifconfig enp0s25 down',shell=True)
        subprocess.call('sudo ifconfig enp0s25 hw ether 12:aa:aa:aa:aa:aa',shell=True)
        subprocess.call('sudo ifconfig enp0s25 up',shell=True)
        x=0
        while(x<2):
            if(obtainSwitchData()):
                x=2
            else:
                print "Did not return data"
                x=x+1
            
        while (getEth0Status() == True):
            print "Still plugged in"
            time.sleep(1.0 - ((time.time() - starttime) % 1.0))
    print "Not Plugged in"
    time.sleep(1.0 - ((time.time() - starttime) % 1.0))



