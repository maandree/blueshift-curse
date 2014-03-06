#!/usr/bin/env python3
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


class Client(DSocket):
    '''
    Blueshift-curse client
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        sockfile = '/dev/shm/.blueshift-curse-%s-%s'
        sockfile %= (os.environ['USER'], os.environ['DISPLAY'])
        DSocket.__init__(self, sockfile, False)

