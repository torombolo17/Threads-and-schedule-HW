#Author     : Jose R de la Vega
#email      : j.r.delavega17@gmail.com
#description: Homework #2 of the course CCOM4017. This program is a server that will recieve messages from
#             mobile.py. it uses 2 threads to execute some tasks such as putting messages in a queue and
#             then sleep the time extracted from the message picked from the queue.

import sys
import socket
from Queue import Queue
from threading import Thread, BoundedSemaphore
import time

#when not all parameters were given
if len(sys.argv) != 2:
    sys.exit("ERROR: %s needs exactly 2 parameters:\n %s <server port>" %(sys.argv[0], sys.argv[0]))

HOST = ''
PORT = int(sys.argv[1])
Qtip = Queue(maxsize = 0)
num_threads = 2
M = {}
maxMsg = 7
countmsg = 0

#semaphore named lock. This will protect the critical region
lock = BoundedSemaphore()

#this function is for the producer thread. This will take the message recieved from mobile devices
#and put them in a queue
def recieve(msg):
    global countmsg
    lock.acquire()
    countmsg += 1
    Qtip.put(msg)
    lock.release()

#this function is for the consumer thread. This will get the message out of the queue
#and will sleep the time extracted from the message 
def makeJob():
    #critical region is getting things in and out of the queue
    #block the other threads of accesing the queue while you are accesing it
    lock.acquire()
    msg = Qtip.get()
    #release the lock so that another thread may use the queue
    lock.release()
    dataList = msg.split(":")#split the id of the mobile device and the job time
    mobileID = dataList[0]
    jobTime = int(dataList[1])
    #if the id is already in the map then ad the time to get the total
    if mobileID in M:
        M[mobileID] = M[mobileID] + jobTime
    #if not then add a new item to the map and give it a value of jobTime
    else:
        M[mobileID] = jobTime
    #sleep :D
    time.sleep(jobTime)

#create udp socket
try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print "Socket created."
except socket.error:
    sys.exit('Socket not created.')
 
#bind the socket to host and port
try:
    print "Socket binded."
    s.bind((HOST, PORT))
except socket.error:
    sys.exit('Failed to do the bind.')
 
#now keep talking with the client
while countmsg < maxMsg:
    # receive data from client (data, addr)
    d = s.recvfrom(1024)
    data = d[0]
    addr = d[1]

    if not data: 
        break

    #create a thread that will recieve the message
    producer = Thread(target=recieve, args=(data,))
    producer.setDaemon(True)
    producer.start()

    #create a thread that will take things from the queue and do a job with that info
    consumer = Thread(target=makeJob)
    consumer.setDaemon(True)
    consumer.start()
     
    #create a reply for the mobile device
    reply = 'OK...' + data
    
    #send the reply to the mobile device
    s.sendto(reply , addr)
    #print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()
    #print the total time used in the CPU for each mobile device

producer.join()
consumer.join()

s.close()

for e in M:
    print 'Mobile '+ e + ' consumed ' + str(M[e]) +' seconds of CPU time. \n'