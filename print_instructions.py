import socket
import sys
import time

def get_constants(prefix):
    """Create a dictionary mapping socket module constants to their names."""
    return dict( (getattr(socket, n), n)
                 for n in dir(socket)
                 if n.startswith(prefix)
                 )

def send_to_print():
    # Create a TCP/IP socket
    sock = socket.create_connection(('128.122.6.188', 8888))
    # print "connected!"

    raw = open("to_print.txt", "r").read()
    messages = raw.split("***")

    for message in messages:
        # print >>sys.stderr, 'sending "%s"' % message
        sock.sendall(message)
        sock.sendall("")
        time.sleep(3)



    # print >>sys.stderr, 'closing socket'
    sock.close()
