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
    print >>sys.stderr, 'sending "%s"' % message
    sock.sendall(message)
    sock.sendall("")
    time.sleep(3)



print >>sys.stderr, 'closing socket'
sock.close()
