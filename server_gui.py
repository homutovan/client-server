import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QDesktopWidget, QHBoxLayout, QFrame, QLabel, QLineEdit, QFileDialog, QAction, QSpinBox
from PyQt5.QtCore import QCoreApplication, QThread, pyqtSlot
from server import Server

                             
class Gui(QWidget):
    
    def __init__(self):
        super().__init__()
        self.foldername = None
        self.server = None
        self.initUI()
        
    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        
        lbl_host = QLabel('Host:', self)
        lbl_port = QLabel('Port:', self)
        lbl_msg = QLabel('Msg:', self)
        lbl_spin = QLabel('Group number:', self)
        self.lbl_msg_wr = QLabel('', self)
        self.lbl_err = QLabel('', self)
        self.edit_host = QLineEdit()
        self.edit_port = QLineEdit('9090')
        btn_run = QPushButton('Run server', self)
        btn_stop = QPushButton('Stop server', self)
        btn_dir = QPushButton('Open folder', self)
        btn_ext = QPushButton('Quit', self)
        self.spin = QSpinBox()
        self.spin.setRange(0 , 99)

        grid.addWidget(lbl_host, 0, 0)
        grid.addWidget(self.edit_host, 0, 1)
        grid.addWidget(lbl_port, 0, 2)
        grid.addWidget(self.edit_port, 0, 3)
        grid.addWidget(self.lbl_err, 1, 0, 1, 4)
        grid.addWidget(lbl_spin, 2, 1, 1, 2)
        grid.addWidget(self.spin, 2, 3)
        grid.addWidget(lbl_msg, 3, 0)
        grid.addWidget(self.lbl_msg_wr, 3, 1, 1, 3)
        grid.addWidget(btn_run, 4, 0, 1, 4)
        grid.addWidget(btn_stop, 5, 0, 1, 4)
        grid.addWidget(btn_dir, 6, 3)
        grid.addWidget(btn_ext, 6, 0)

        btn_ext.clicked.connect(QCoreApplication.instance().quit)
        btn_run.clicked.connect(self.start)
        btn_dir.clicked.connect(self.get_filename)
        btn_stop.clicked.connect(self.stop)
        self.spin.valueChanged.connect(self.set_group)
        
        self.setWindowTitle('TCP Server')
        self.center()
        self.show()
        
    def get_filename(self):

        self.foldername = QFileDialog.getExistingDirectory(self, "Set folder",".")
    
    @pyqtSlot(str)
    def show_msg(self, string):
        self.lbl_msg_wr.setText(string)
        
    def set_group(self, value):
        if self.server:
            self.server.group_number = str(value).rjust(2, '0')
        
    def start(self):
        self.thread = QThread()
        file_patch = self.foldername  + '/log.csv' if self.foldername  else 'log.csv'
        self.server = Server(str(self.spin.value()).rjust(2, '0'), file_patch)
        self.server.show_string.connect(self.show_msg)
        if (port := self.edit_port.text()):
            self.server.create(int(port))
            self.server.loop = True
            self.server.moveToThread(self.thread)
            self.thread.started.connect(self.server.run)
            self.thread.setTerminationEnabled()
            self.thread.start()
        
        else:
            self.lbl_err.setText('Error!')
            
    def stop(self):
        if self.server:
            self.server.loop = False
            self.thread.terminate()

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