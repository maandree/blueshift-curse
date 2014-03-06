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
import threading

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
        self.clients = []
        self.semaphore = threading.Semaphore()
    
    
    def close(self):
        '''
        Close the socket
        '''
        self.socket.close()
        if self.semaphore.acquire(blocking = True):
            for client in self.client:
                client.close()
            self.semaphore.release()
        os.unlink(self.sockfile)
    
    
    def listen(self, target):
        '''
        Accept all coming connections asynchronously
        
        @param   target:(DSocket)?→void  The function to invoke, with next sockets,
                                         when new connections are accepted
        @return  :Thread                 The created thread
        '''
        def target_(socket):
            if self.semaphore.acquire(blocking = True):
                self.clients.append(socket)
                self.semaphore.release()
            if target is not None:
                    target(socket)
        return self.socket.listen(target_)
    
    
    def broadcast(self, text):
        '''
        Broadcast a message to all clients
        
        @param  text:str  The text line to send
        '''
        for client in list(self.client):
            self.send(text, client)
    
    
    def send(self, text, target):
        '''
        Send a message to a client
        
        @param  text:str         The text line to send
        @param  target:DSocket?  The client, `None` for all
        '''
        if self.target is None:
            self.broadcast(text)
        else:
            try:
                target.write(text)
            except:
                try:
                    if self.semaphore.acquire(blocking = True):
                        del self.clients[self.clients.index(target)]
                        self.semaphore.release()
                except:
                    pass
    
    
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

