#!/usr/bin/python3

"""
Socket binds to 0.0.0.0 instead of localhost so it responds to its public IP address

New filestreams must start with segId=0, with f_newTransaction=1
Subsequent segIds simply add the current segId and the number of msg bytes received

The server acks every packet received

Additional cmd line option --verbose added to make server noisy
Options -s to save file, -o to indicate output file name
"""

import socket
from struct import *
import argparse

def runReceiver(verbose, savefile, output_filename):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = '0.0.0.0'
    server_port = 5555
    sock.bind((server_address, server_port))
    
    
    if verbose:
        print("Server started. Listening on %s at port %d" % (server_address, server_port))
    s = bytearray()
    
    while True:
        recv = sock.recvfrom(65535)
        data, client_addr = recv
        client_ip = client_addr[0]
        msg_length = len(data) - 13
        flags, tr_id, segId, total_len, msg = unpack('!BIII' + str(msg_length) + 's', data)
        
        fin = flags & 2**3
        f_newTransaction = flags & 2**0
        if f_newTransaction:
            print('new filestream started')
            s = bytearray(total_len)
        
        # store data into s
        if msg_length:
            s[segId:segId+msg_length] = msg
        
        if verbose:
            print("segId:%d,msg_length:%d" % (segId, msg_length))
            print('flags:', flags)
            print('f_newTransaction:', flags & 2**0)
            print('f_endTransaction:', (flags & 2**1) >> 1)
            print('f_fin:', (flags & 2**3) >> 3)
        
        # create flags
        f_endTransaction = (flags & 2**1) >> 1
        f_newTransaction = 0
        f_ack = 1
        f_fin = 1 if fin else 0
        flags = f_newTransaction + (f_endTransaction << 1) + (f_ack << 2) + (f_fin << 3)

        # send ack
        payload = pack('!BII', flags, segId, msg_length)
        sock.sendto(payload, client_addr)
        
        if fin:
            print('endTr, file size:', len(s))
            if savefile:
                with open(output_filename, 'wb') as of:
                    of.write(s)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Prints data and addresses')
    parser.add_argument('-s', '--savefile', action='store_true', default=False, help='Indicate whether to save data to file')
    parser.add_argument('-o', dest='output_filename', default='output', help="Indicate name of file to output. Defaults to 'output' in the same directory")
    
    args = parser.parse_args()

    runReceiver(args.verbose, args.savefile, args.output_filename)
        
