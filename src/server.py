#!/usr/bin/env python3
'''
blueshift-curse – Blueshift extension with IPC and an ncurses front-end
Copyright © 2014  Mattias Andrée (m@maandree.se)

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
        self.sockfile = '/dev/shm/.blueshift-curse-%s~%s'
        self.sockfile %= (os.environ['DISPLAY'], os.environ['USER'])
        self.socket = DSocket(self.sockfile, True)
        self.clients = []
        self.semaphore = threading.Semaphore()
        self.condition = None
        self.inqueue = None
        self.reading = False
    
    
    def close(self):
        '''
        Close the socket
        '''
        self.socket.close()
        self.semaphore.acquire():
        try:
            for client in self.client:
                client.close()
        finally:
            self.semaphore.release()
        os.unlink(self.sockfile)
    
    
    def async_read(self, client):
        '''
        Used by the class itself to read from clients asynchronously
        
        @param  client:DSocket  The client
        '''
        def async_read_():
            while True:
                line = client.read()
                if line is None:
                    break
                self.condition.acquire()
                try:
                    self.inqueue.append((line, client))
                    self.condition.notify()
                finally:
                    self.condition.release()
            self.semaphore.acquire()
            try:
                del self.clients[self.clients.index(client)]
            finally:
                self.semaphore.release()
        thread = threading.Thread(target = async_read_)
        thread.setDaemon(False)
        thread.start()
    
    
    def listen(self, target):
        '''
        Accept all coming connections asynchronously
        
        @param   target:(DSocket)?→void  The function to invoke, with next sockets,
                                         when new connections are accepted
        @return  :Thread                 The created thread
        '''
        def target_(socket):
            self.semaphore.acquire()
            try:
                self.clients.append(socket)
                if self.reading:
                    self.async_read(socket)
            finally:
                self.semaphore.release()
            if target is not None:
                target(socket)
        return self.socket.listen(target_)
    
    
    def read(self):
        '''
        Wait for a message from any client. Once this method
        has be invoked, you cannot read from the clients
        individually and must use this method.
        
        @return  :(str, DSocket)  The message received and which client send the message
        '''
        self.semaphore.acquire()
        try:
            if not self.reading:
                self.reading = True
                self.condition = threading.Condition()
                self.inqueue = []
                for client in self.clients:
                    self.async_read(client)
        finally:
            self.semaphore.release()
        self.condition.acquire()
        try:
            self.condition.wait()
            self.semaphore.acquire()
            try:
                rc, self.inqueue[:] = self.inqueue[-1], self.inqueue[:-1]
            finally:
                self.semaphore.release()
        finally:
            self.condition.release()
        return rc
    
    
    def broadcast(self, text):
        '''
        Broadcast a message to all clients
        
        @param  text:str  The text line to send
        '''
        for client in list(self.client):
            self.write(text, client)
    
    
    def write(self, text, target):
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
                    self.semaphore.acquire()
                    del self.clients[self.clients.index(target)]
                except:
                    pass
                finally:
                    self.semaphore.release()
    
    
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

