import socket
import sys
import the_best_art
import time

def get_constants(prefix):
    """Create a dictionary mapping socket module constants to their names."""
    return dict( (getattr(socket, n), n)
                 for n in dir(socket)
                 if n.startswith(prefix)
                 )

# Create a TCP/IP socket
sock = socket.create_connection(('192.168.0.102', 8888))
print "connecting..."



for i in range(int(sys.argv[1])):
    message = the_best_art.generate_message()
    print >>sys.stderr, 'sending "%s"' % message
    sock.sendall(message)
    time.sleep(1)



print >>sys.stderr, 'closing socket'
sock.close()
