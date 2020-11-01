from puzzle_scraper import PuzzleScraper
import sys
from Body import Body 
from PyQt5.QtCore import QDate, QSize, QTime, QTimer, Qt
from PyQt5.QtGui import QFont, QFontDatabase, QIcon

from PyQt5.QtWidgets import QApplication, QDesktopWidget, QGridLayout, QHBoxLayout, QLabel, QMainWindow, QVBoxLayout, QWidget

GROUP_NAME = "PROMINI"
APP_SIZE = (1000, 800)
EMPTY_GRID = [  [' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' '] ]

class App(QMainWindow):
    def __init__(self, grid=EMPTY_GRID, answer=EMPTY_GRID, across=[], down=[]):
        super().__init__()  
        self.central_widget = MainWidget(grid, answer, across, down)
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle("PROMINI NYT Mini CrossWord Solver")
        self.setWindowIcon(QIcon('nytimes.png')) 
        self.setMinimumSize(QSize(*APP_SIZE))
        self.setStyleSheet("background-color: white;") 
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class MainWidget(QWidget):
    def __init__(self, grid, answer, across, down):
        super().__init__()  
        # Get today's date and time
        now = QDate.currentDate() 
        self.todays_date = now.toString(Qt.DefaultLocaleLongDate)
        time = QTime.currentTime()
        self.current_time = time.toString(Qt.DefaultLocaleLongDate)
        self.grid = grid
        self.answer = answer
        self.across = across
        self.down = down
        self.initUI()  

    def initUI(self):
        QFontDatabase.addApplicationFont("Resources/KarnakPro-CondensedBlack.ttf")

        # Header
        self.header = QVBoxLayout()
        header_str = "The Mini Crossword"
        header_label = QLabel(header_str)
        header_label.setFont(QFont("KarnakPro-CondensedBlack", 30))
        self.header.addWidget(header_label)
        joel_label = QLabel("By Joel Fagliano")
        joel_label.setFont(QFont("Franklin", 10))
        self.header.addWidget(joel_label)

        # Body (or middle part)
        self.body = QHBoxLayout()
        self.body.setSpacing(10)
        self.body.addWidget(Body(self.grid, self.answer, self.across, self.down, parent=self))

        # Footer
        self.footer = QHBoxLayout()

        # creating a timer object to update the time and date every second
        timer = QTimer(self) 
        timer.timeout.connect(self.show_time) 
        timer.start(1000) 
        
        footer_str = self.todays_date + '\n' + self.current_time + '\n' + GROUP_NAME
        self.footer_label = QLabel(footer_str)
        self.footer_label.setFont(QFont("Franklin", 10))

        # Send footer label to the right
        self.footer.addStretch(1)
        self.footer.addWidget(self.footer_label)


        main_layout = QGridLayout()

        # Add header on top
        main_layout.addLayout(self.header, 0, 0, 1, 1)

        # Add body after header
        main_layout.addLayout(self.body, 1, 0, 5, 1)

        # Send footer to the bottom
        main_layout.addLayout(self.footer, 6, 0, 1, 1)

        self.setLayout(main_layout)
        self.show()
    
    def show_time(self):
        now = QDate.currentDate() 
        self.todays_date = now.toString(Qt.DefaultLocaleLongDate)
        time = QTime.currentTime()
        self.current_time = time.toString(Qt.DefaultLocaleLongDate)
        footer_str = self.todays_date + '\n' + self.current_time + '\n' + GROUP_NAME
        self.footer_label.setText(footer_str)


def main():
    ps = PuzzleScraper()
    ps.click_button()
    grid = ps.get_grid()
    across, down = ps.get_clues()
    answer = ps.reveal_puzzle()
    ps.close_driver()
    app = QApplication(sys.argv)
    window = App(grid, answer, across, down)
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()

