from Adafruit_Thermal import *
import textwrap
import socket
import sys
from thread import *

printer = Adafruit_Thermal("/dev/ttyUSB0", 9600, timeout=5)

w = textwrap.TextWrapper(width=31,break_long_words=False,replace_whitespace=False)


message = ''

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
    s.close()

print 'Socket bind complete'

#Start listening on socket
s.listen(10)
print 'Socket now listening'

def process_message(i):
    encoded = i.encode("utf-8")
    strings = encoded.split("$$$$")
    return strings



def wrap(strings):
    if len(strings) > 1:
        printer.wake()
        printer.setDefault() # Restore printer to defaults
        buff = "\n\n\n"
        border = "-------"
        printer.setSize('S')
        current = '\n'.join(w.wrap(strings[0]))
        printer.underlineOn()
        printer.println(current)
        printer.underlineOff()

        for s in strings[1:-2]:
            output = '\n'.join(w.wrap(s))
            printer.println(output)
            printer.feed(1)
        printer.justify('C')
        printer.boldOn()
        printer.setSize('M')
        command = '\n'.join(w.wrap(strings[-2]))
        printer.println(command)
        printer.println(border)
        printer.boldOff()
        printer.setSize('S')
        printer.justify('R')
        printer.println("-- Computer")
        printer.println(buff)
        printer.sleep()


#Function for handling connections. This will be used to create threads
def clientthread(conn):

    #infinite loop so that function do not terminate and thread do not end.
    while True:

        #Receiving from client
        data = conn.recv(1024)
        message = ''
        strings = process_message(data)
        print strings
        wrap(strings)
        if not data:
            break


    #came out of loop
    conn.close()

#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))

s.close()
