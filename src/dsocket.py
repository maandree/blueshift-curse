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
import socket
import threading


class DSocket:
    '''
    Domain socket
    
    @variable  scoket:socket  The socket
    '''
    
    def __init__(self, pathname, server = None):
        '''
        Constructor
        
        @param  pathname:str  The pathname of the socket
        @param  server:bool   Whether to act as a server, otherwise as a client
        
        -- OR --
        
        @param  :socket  The socket
        '''
        if server == None:
            self.socket = pathname
        else:
            self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            (self.socket.bind if server else self.socket.connect)(pathname)
        self.buffer = ''
    
    
    def write(self, text):
        '''
        Send a text line
        
        @param  text:str  The line
        '''
        self.socket.send((text + '\n').encode('utf-8'))
    
    
    def read(self):
        '''
        Read a line of text
        
        @return  :str?  The next line, `None` if the connection has closed,
                        in which case, close the connection on your end
        '''
        while True:
            got = self.socket.recv(1024).decode('utf-8', 'error')
            if len(got) == 0:
                return None
            self.buffer += got
            if '\n' in self.buffer:
                i = self.buffer.find('\n')
                rc, self.buffer = self.buffer[:i], self.buffer[i + 1:]
                return rc
    
    
    def listen(self, target):
        '''
        Accept all coming connections asynchronously
        
        @param   target:(DSocket)→void  The function to invoke, with next sockets,
                                        when new connections are accepted
        @return  :Thread                The created thread
        '''
        def listen_():
            self.socket.listen(5)
            while True:
                (sock, _address) = self.socket.accept()
                sock = DSocket(sock)
                thread = threading.Thread(target = target, args = (sock,))
                thread.setDaemon(True)
                thread.start()
        thread = threading.Thread(target = listen_)
        thread.setDaemon(True)
        thread.start()
        return thread
    
    
    def close(self):
        '''
        Close the socket
        '''
        self.socket.close()
    
    
    def __enter__(self):
        '''
        Called when `with` enters
        '''
        return self
    
    
    def __exit__(self, _type, _value, _traceback):
        '''
        Called when `with` exits
        '''
        self.close()

