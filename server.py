import socket
import time
import csv
import select
import re
from PyQt5.QtCore import pyqtSignal, QObject

def jprint(*args):
    print(time.strftime("%H.%M.%S", time.localtime()), *args)

class Server(QObject):
    
    show_string = pyqtSignal(str)
    
    def __init__(self, group_number, file_patch = 'log.csv', ):
        super().__init__()
        self.handler = String_handler()
        self.loop = True
        self.file_patch = file_patch
        self.connect = None
        self.data = None
        self.inputs = []
        self.outputs = []
        self.group_number = group_number
        
    def create(self, port, host = '', backlog = 1):
        self.socket = socket.socket()
        self.socket.setblocking(0)
        try:
            self.socket.bind((host, port))
        except Exception as e:
            self.error_msg = e
        self.socket.listen(backlog)
        self.inputs.append(self.socket)
        
    def handle_read(self, readables):

        for resource in readables:

            if resource is self.socket:
                connection, client_address = resource.accept()
                connection.setblocking(0)
                self.inputs.append(connection)
                jprint(f'Connected: {client_address}')
                
            else:
                try:
                    self.data = resource.recv(1024).decode("utf-8")

                except ConnectionResetError:
                    jprint('Connection aborted')

                if self.data:
                    jprint(f'Getting data: {self.data}')

                    if resource not in self.outputs:
                        self.outputs.append(resource)
                        
                else:
                    self.clear_resource(resource)
          
    def run(self):
        jprint('Server started')
        with open(self.file_patch, 'w') as file:
            while self.loop:
                readables, writables, exceptional = select.select(self.inputs, self.outputs, self.inputs, 1)
                self.handle_read(readables)
                
                if self.data:
                    self.handler.parse(self.data)
                    
                    if self.handler.parse_status:
                        writer = csv.writer(file)
                        writer.writerow([self.data])
                        
                        if self.handler.group_number == self.group_number:
                            self.show_string.emit(self.handler.get_parse_string())
                    
                    self.data = None
            
        jprint('Server stopped')
        
    def clear_resource(self, resource):
        
        if resource in self.outputs:
            self.outputs.remove(resource)
            
        if resource in self.inputs:
            self.inputs.remove(resource)
            
        resource.close()

        jprint(f'Disconnected: {str(resource)}')
                
    def stop(self):
        self.stopped.set()
        self.proc.join()
        if self.connect:
            self.connect.close()
        if self.socket:
            self.socket.close()       
            
class String_handler():
    
    def __init__(self):
        super().__init__()
        self.pattern = '(\d{4})\s(..)\s(\d{2}:\d{2}:\d{2}).(\d{3})\s(\d{2,})(\WCR\W)'
    
    def parse(self, string):
        match = re.fullmatch(self.pattern, string)
        if match:
            self.groups = match.groups()
            self.number = self.groups[0]
            self.id = self.groups[1]
            self.time_sec = self.groups[2]
            self.time_msec = self.groups[3]
            self.group_number = self.groups[4]
            self.parse_status = True
            
        else: 
            self.parse_status = False
            
    def get_parse_string(self):
        return f'Cпортсмен, нагрудный номер {self.number} прошёл отсечку {self.id} в {self.time_sec}:{self.time_msec[0]}'
      
if __name__ == '__main__':
    pass