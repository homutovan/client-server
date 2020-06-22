import socket

class Client:
    
    def __init__(self):
        self.peername = None
        
    def connect(self, host, port):
        self.socket = socket.socket()
        try:
            self.socket.connect((f'{host}', port))
            self.peername = self.socket.getpeername()
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
        self.socket.close()
        
        
if __name__ == '__main__':
    
    client = Client()