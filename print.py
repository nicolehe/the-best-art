import socket
import sys
import time

def get_constants(prefix):
    """Create a dictionary mapping socket module constants to their names."""
    return dict( (getattr(socket, n), n)
                 for n in dir(socket)
                 if n.startswith(prefix)
                 )

# Create a TCP/IP socket
sock = socket.create_connection(('192.168.0.102', 8888))
print "connected!"

raw = open("to_print.txt", "r").read()
messages = raw.split("***")

for message in messages:
    # # message = the_best_art.generate_message("$$$$")
    # strs = ["05:52 PM, March 25, 2017",
    #            "Good afternoon, human, moderate rain today.",
    #            "I have calculated the best art for the current state of the world. Today's Art Index is 0.0194890717792, and this project has a very close rating of 0.0166666666667.",
    #            "Execute the following:",
    #            "1490478746: Create a carrot that evokes larger social issues.", ""]


    print >>sys.stderr, 'sending "%s"' % message
    sock.sendall(message)
    time.sleep(3)



print >>sys.stderr, 'closing socket'
sock.close()
