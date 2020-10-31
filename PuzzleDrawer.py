import sys
from PyQt5.QtCore import QDate, QSize, QTime, QTimer, Qt
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QMainWindow, QVBoxLayout, QWidget

GROUP_NAME = "PROMINI"

# Default 5x5 crossword puzzle. 
grid =[ 
        [1, 0, 0, 0, 1], 
        [0, 1, 0, 1, 0], 
        [0, 0, 1, 0, 0], 
        [0, 0, 1, 0, 0], 
        [0, 0, 1, 0, 0], 
    ] 

class App(QMainWindow):
    def __init__(self):
        super().__init__()  
        self.central_widget = MainWidget()
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle("PROMINI NYT Mini CrossWord Solver")
        self.setWindowIcon(QIcon('nytimes.png')) 
        self.setFixedSize(QSize(1280, 720))

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()  
        # Get today's date and time
        now = QDate.currentDate() 
        self.todays_date = now.toString(Qt.DefaultLocaleLongDate)
        time = QTime.currentTime()
        self.current_time = time.toString(Qt.DefaultLocaleLongDate)

        self.initUI()  

    def initUI(self):
        # Header
        self.header = QHBoxLayout()
        header_str = "The Mini Crossword " + self.todays_date + '\n' + "By Joel Fagliano" 
        header_label = QLabel(header_str)
        self.header.addWidget(header_label)

        # Body (or middle part)
        self.body = QHBoxLayout()

        # Footer
        self.footer = QHBoxLayout()

        # creating a timer object 
        timer = QTimer(self) 
  
        # adding action to timer 
        timer.timeout.connect(self.show_time) 
  
        # update the timer every second 
        timer.start(1000) 
        
        footer_str = self.todays_date + '\n' + self.current_time + '\n' + GROUP_NAME
        self.footer_label = QLabel(footer_str)

        # Send footer label to the right
        self.footer.addStretch(1)
        self.footer.addWidget(self.footer_label)

        vbox = QVBoxLayout()
        # Add header on top
        vbox.addLayout(self.header)

        # Add body after header
        vbox.addLayout(self.body)

        # Send footer to the bottom
        vbox.addStretch(1)
        vbox.addLayout(self.footer)


        self.setLayout(vbox)
        self.show()
    
    def show_time(self):
        now = QDate.currentDate() 
        self.todays_date = now.toString(Qt.DefaultLocaleLongDate)
        time = QTime.currentTime()
        self.current_time = time.toString(Qt.DefaultLocaleLongDate)
        footer_str = self.todays_date + '\n' + self.current_time + '\n' + GROUP_NAME
        self.footer_label.setText(footer_str)

def main():
    app = QApplication(sys.argv)
    window = App()
    window.show()



    app.exec_()
    


if __name__ == '__main__':
    main()

