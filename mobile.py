#Author     : Jose R de la Vega
#email      : j.r.delavega17@gmail.com
#description: Homework #2 of the course CCOM4017. This program is a mobile client that will send messages to scheduler.py

import socket
import sys
from random import randrange
import time

#when not all parameters were given
if len(sys.argv) != 4:
    sys.exit("ERROR: %s needs exactly 4 parameters:\n %s <mobile ID> <server address> <server port>" %(sys.argv[0], sys.argv[0]))
 
# create udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    sys.exit('Socket not created')

mID = str(sys.argv[1])
host = sys.argv[2]
port = int(sys.argv[3])

#maxTime is the maximum number that can be generated
maxTime = 10
#numJobs is the number of random numbers to be generated
numJobs = 5
#Tlist is a list with all the random numbers
Tlist = []
#max time to wait before sending a message
randtime = 5

#this loop creats a list with random numbers converted to strings
for k in range(numJobs):
    Tlist.append(randrange(maxTime)+1)
 
for e in Tlist:
    #create a mesage with the id of the mobile device and the time of the job (3:7)
    msg = mID+':'+ str(e)
    random = randrange(randtime)+1
    time.sleep(random)
    try :
        #send the message to the server
        s.sendto(msg, (host, port))
         
        #receive data from the server
        rep = s.recvfrom(port)
        reply = rep[0]
        addr = rep[1]
         
        print 'Server replied: ' + reply
     
    except socket.error:
        sys.exit('Error sending the message')

