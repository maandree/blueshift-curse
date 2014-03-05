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

from dsocket import DSocket


def talk_function(socket):
    while True:
        line = socket.read()
        if line is None:
            break
        print(line)


sockfile = '/dev/shm/blueshift-curse'
if os.path.exists(sockfile):
    os.unlink(sockfile)
with DSocket(sockfile, True) as sock:
    try:
        sock.listen(talk_function).join()
    except KeyboardInterrupt:
        pass
os.unlink(sockfile)

