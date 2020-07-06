import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QDesktopWidget, QFrame, QLabel, QLineEdit
from PyQt5.QtCore import QCoreApplication
from client import Client
                             
class Gui(QWidget):
    
    def __init__(self):
        super().__init__()
        self.client = Client()
        self.client.connected_done.connect(lambda: self.disable_btn(True))
        self.client.connected_close.connect(lambda: self.disable_btn(False))
        self.initUI()
        
    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        self.addr_frame = QFrame()
        addr_layout = QGridLayout()
        self.addr_frame.setLayout(addr_layout)
        
        lbl_host = QLabel('Host:', self)
        lbl_port = QLabel('Port:', self)
        lbl_msg = QLabel('Msg:', self)
        self.lbl_err = QLabel('', self)
        self.lbl_err_msg = QLabel('', self)
        self.edit_host = QLineEdit('localhost')
        self.edit_port = QLineEdit('9090')
        self.edit_msg = QLineEdit()
        self.btn_conn = QPushButton('Connect', self)
        self.btn_dconn = QPushButton('Disconnect', self)
        self.btn_dconn.setDisabled(True)
        self.btn_send = QPushButton('Send', self)
        self.btn_send.setDisabled(True)
        self.btn_ext = QPushButton('Quit', self)
        
        addr_layout.addWidget(lbl_host, 0, 0)
        addr_layout.addWidget(self.edit_host, 0, 1)
        addr_layout.addWidget(lbl_port, 0, 2)
        addr_layout.addWidget(self.edit_port, 0, 3)
        addr_layout.addWidget(self.lbl_err, 1, 0, 1, 4)
        
        grid.addWidget(self.addr_frame, 0, 0, 1, 4)
        grid.addWidget(self.lbl_err, 1, 0, 1, 4)
        grid.addWidget(self.btn_conn, 2, 0, 1, 4)
        grid.addWidget(self.btn_dconn, 3, 0, 1, 4)
        grid.addWidget(lbl_msg, 4, 0)
        grid.addWidget(self.edit_msg, 4, 1, 1, 2)
        grid.addWidget(self.btn_send, 4, 3, 1, 2)
        grid.addWidget(self.lbl_err_msg, 5, 0, 1, 4)
        grid.addWidget(self.btn_ext, 6, 0)
        
        self.btn_ext.clicked.connect(QCoreApplication.instance().quit)
        self.btn_conn.clicked.connect(self.connect)
        self.btn_send.clicked.connect(self.send)
        self.btn_dconn.clicked.connect(self.disconnect)
        
        self.setWindowTitle('TCP Client')
        self.center()
        self.show()
        
    def disable_btn(self, value):
        self.btn_conn.setDisabled(value)
        self.btn_ext.setDisabled(value)
        self.btn_send.setEnabled(value)
        self.btn_dconn.setEnabled(value)
        self.addr_frame.setDisabled(value)
        
    def connect(self):
        host = self.edit_host.text()
        port = self.edit_port.text()
        
        if host and port:
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
        msg = self.edit_msg.text()
        if msg:
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