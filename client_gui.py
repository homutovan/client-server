import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QDesktopWidget, QHBoxLayout, QFrame, QLabel, QLineEdit
from PyQt5.QtCore import QCoreApplication
from client import Client
                             
class Gui(QWidget):
    
    def __init__(self):
        super().__init__()
        self.client = Client()
        self.initUI()
        
    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        
        lbl_host = QLabel('Host:', self)
        lbl_port = QLabel('Port:', self)
        lbl_msg = QLabel('Msg:', self)
        self.lbl_err = QLabel('', self)
        self.lbl_err_msg = QLabel('', self)
        self.edit_host = QLineEdit('localhost')
        self.edit_port = QLineEdit('9090')
        self.edit_msg = QLineEdit()
        btn_conn = QPushButton('Connect', self)
        btn_dconn = QPushButton('Disconnect', self)
        btn_send = QPushButton('Send', self)
        btn_ext = QPushButton('Quit', self)

        grid.addWidget(lbl_host, 0, 0)
        grid.addWidget(self.edit_host, 0, 1)
        grid.addWidget(lbl_port, 0, 2)
        grid.addWidget(self.edit_port, 0, 3)
        grid.addWidget(self.lbl_err, 1, 0, 1, 4)
        grid.addWidget(btn_conn, 2, 0, 1, 4)
        grid.addWidget(btn_dconn, 3, 0, 1, 4)
        
        grid.addWidget(lbl_msg, 4, 0)
        grid.addWidget(self.edit_msg, 4, 1, 1, 2)
        grid.addWidget(btn_send, 4, 3, 1, 2)
        grid.addWidget(self.lbl_err_msg, 5, 0, 1, 4)
        
        grid.addWidget(btn_ext, 6, 0)
        
        btn_ext.clicked.connect(QCoreApplication.instance().quit)
        btn_conn.clicked.connect(self.connect)
        btn_send.clicked.connect(self.send)
        btn_dconn.clicked.connect(self.disconnect)
        
        self.setWindowTitle('TCP Client')
        self.center()
        self.show()
        
    def connect(self):
        if (host := self.edit_host.text()) and (port := self.edit_port.text()):
            self.client.connect(host, int(port))
            if self.client.peername:
                self.lbl_err.setText(f'Connected to: {self.client.peername[0]}:{self.client.peername[1]}')
            else:
                self.lbl_err.setText(str(self.client.error_msg))
        else:
            self.lbl_err.setText('Error!')
            
    def disconnect(self):
        self.client.close()
        self.lbl_err.setText('')
        
    def send(self):
        if (msg := self.edit_msg.text()):
            self.client.send(msg)
            self.lbl_err_msg.setText('')
        else:
            self.lbl_err_msg.setText('Error!')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')         
    gui = Gui()
    sys.exit(app.exec_())