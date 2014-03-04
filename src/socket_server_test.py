#!/usr/bin/python3
'''
blueshift-curse – Blueshift extension with IPC and an ncurses front-end
Copyright © 2014  Mattias Andrée (maandree@member.fsf.org)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import os
import socket
import threading


def accept_function():
    sock.listen(5)
    while True:
        (socket, address) = sock.accept()
        thread = threading.Thread(target = talk_function, args = (socket,))
        thread.setDaemon(False)
        thread.start()


def talk_function(socket):
    while True:
        packet = socket.recv(1024)
        if (packet is None) or (len(packet) == 0):
            break
        print(packet.decode('utf-8', 'replace'))


sockfile = '/dev/shm/blueshift-curse'
if os.path.exists(sockfile):
    os.unlink(sockfile)
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.bind(sockfile)
try:
    thread = threading.Thread(target = accept_function)
    thread.setDaemon(False)
    thread.start()
    thread.join()
except:
    pass
finally:
    sock.close()

