import socket
from PyQt5.QtCore import pyqtSignal, QObject

class Client(QObject):
    
    connected_done = pyqtSignal()
    connected_close = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.peername = None
        self.socket = None
        
    def connect(self, host, port):
        self.socket = socket.socket()
        try:
            self.socket.connect((f'{host}', port))
            self.peername = self.socket.getpeername()
            self.connected_done.emit()
            
        except Exception as e:
            self.error_msg = e
            
    def send(self, msg):
        try:
            self.socket.send(msg.encode())
        except Exception as e:
            self.error_send_msg = e
        
    def recv(self):
        return self.socket.recv(1024)
    
    def close(self):
        if self.socket:
            self.socket.close()
            self.socket = None
            self.connected_close.emit()
        
if __name__ == '__main__':
    
    client = Client()