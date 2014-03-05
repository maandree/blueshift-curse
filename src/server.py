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


class Server:
    '''
    Blueshift-curse server
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.sockfile = '/dev/shm/.blueshift-curse-%s-%s'
        self.sockfile %= (os.environ['USER'], os.environ['DISPLAY'])
        self.socket = DSocket(self.sockfile, True)
        os.chmod(self.sockfile, 0o600)
    
    
    def close(self):
        '''
        Close the socket
        '''
        self.socket.close()
        os.unlink(self.sockfile)
        
        
    def listen(self, target):
        '''
        Accept all coming connections asynchronously
        
        @param   target:(DSocket)→void  The function to invoke, with next sockets,
                                        when new connections are accepted
        @return  :Thread                The created thread
        '''
        return self.socket.listen(target)
    
    
    def __enter__(self):
        '''
        Called when `with` enters
        '''
        return self
    
    
    def __exit__(self, _type, _value, _trace):
        '''
        Called when `with` exits
        '''
        self.close()

