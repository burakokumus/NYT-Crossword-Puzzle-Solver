import json
import sys
from puzzle_scraper import PuzzleScraper
from Body import Body 
from PyQt5.QtCore import QDate, QSize, QTime, QTimer, Qt
from PyQt5.QtGui import QFont, QFontDatabase, QIcon
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QGridLayout, QHBoxLayout, QLabel, QMainWindow, QVBoxLayout, QWidget

TRACE_MODE = True
GROUP_NAME = "PROMINI"
APP_SIZE = (1200, 700)
EMPTY_GRID = [  [' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' '] ]

class App(QMainWindow):
    def __init__(self, custom_file=None):
        super().__init__()    
        if TRACE_MODE:
            print("Initializing the app window")
        
        if custom_file is None:
            ps = PuzzleScraper(trace_mod=TRACE_MODE)
            ps.click_button()
            grid = ps.get_grid()
            across, down = ps.get_clues()
            grid_numbers = ps.get_grid_numbers()
            ps.reveal_puzzle()
            answer = ps.extract_answers()
            ps.close_driver()
            self.central_widget = MainWidget(grid, grid_numbers, answer, across, down)
        
        else:
            json_file = open("./PuzzleDatabases/" + custom_file + ".json", 'r')
            data = json.load(json_file)
            date = data["date"]
            grid = data["grid"]
            across, down = data["across"], data["down"]
            grid_numbers = data["grid_numbers"]
            answer = data["answer"]
            self.central_widget = MainWidget(grid, grid_numbers, answer, across, down, date)

        
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle("PROMINI NYT Mini CrossWord Solver")
        self.setWindowIcon(QIcon('Resources/nytimes.png')) 
        self.setFixedSize(QSize(*APP_SIZE))
        self.setStyleSheet("background-color: white;") 
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class MainWidget(QWidget):
    def __init__(self, grid, grid_numbers, answer, across, down, date = None):
        super().__init__()  
        # Get today's date and time
        now = QDate.currentDate() 
        self.todays_date = now.toString(Qt.DefaultLocaleLongDate) if date is None else date
        time = QTime.currentTime()
        self.current_time = time.toString(Qt.DefaultLocaleLongDate)
        self.grid = grid
        self.grid_numbers = grid_numbers
        self.answer = answer
        self.across = across
        self.down = down
        self.initUI()  

    def initUI(self):
        QFontDatabase.addApplicationFont("Resources/KarnakPro-CondensedBlack.ttf")

        # Header
        self.header = QVBoxLayout()
        top = QHBoxLayout()
        header_str = "The Mini Crossword"
        header_label = QLabel(header_str)
        header_label.setFont(QFont("KarnakPro-CondensedBlack", 30))
        header_label.setAlignment(Qt.AlignBottom)
        top.addWidget(header_label)
        date_label = QLabel(self.todays_date)
        date_label.setFont(QFont("Franklin", 17, 10))
        date_label.setAlignment(Qt.AlignBottom)
        date_label.setIndent(7)
        top.addWidget(date_label)
        top.addStretch(1)
        self.header.addLayout(top)
        joel_label = QLabel("By Joel Fagliano")
        joel_label.setFont(QFont("Franklin", 10))
        self.header.addWidget(joel_label)

        # Body (or middle part)
        self.body = QHBoxLayout()
        self.body.setSpacing(10)
        self.body.addWidget(Body(self.grid, self.grid_numbers, self.answer, self.across, self.down, parent=self, trace_mod=TRACE_MODE))

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
    app = QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()

