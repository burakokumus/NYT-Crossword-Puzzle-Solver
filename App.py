import json
import sys
import time
from puzzle_scraper import PuzzleScraper
from solver import solve
from Body import Body 
from PyQt5.QtCore import QDate, QSize, QTime, QTimer, Qt
from PyQt5.QtGui import QFont, QFontDatabase, QIcon
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QGridLayout, QHBoxLayout, QLabel, QMainWindow, QVBoxLayout, QWidget

GROUP_NAME = "PROMINI"
APP_SIZE = (1700, 700)

'''
App class builds the main frame of the application
It is inherited from QMainWindow
Includes attributes of the frame itself
Content is handled by another class
Can process data from .json file if specified, from NYT Mini Crossword webpage otherwise
'''
class App(QMainWindow):
    def __init__(self, custom_file=None, trace_mod=False):
        super().__init__()    
        if trace_mod:
            print("Initializing the app window")
        
        # If custom file is not specified, use puzzle scraper to gather data from NYT Mini Crossword webpage
        if custom_file is None:
            ps = PuzzleScraper(trace_mod=trace_mod)
            ps.click_button()
            grid = ps.get_grid()
            across, down = ps.get_clues()
            grid_numbers = ps.get_grid_numbers()
            ps.reveal_puzzle()
            answer = ps.extract_answers()
            time.sleep(3.5)
            ps.close_driver()
            official_sol = {
                "grid": grid,
                "across": across,
                "down": down,
                "grid_numbers": grid_numbers,
                "answer": answer
            }
            
            our_answer = solve(grid, across, down, grid_numbers, trace_mod=trace_mod)
            self.central_widget = MainWidget(official_sol, our_answer, trace_mod=trace_mod)
        
        # Use data from given .json file in PuzzleDatabases folder
        else:
            json_file = open("./PuzzleDatabases/" + custom_file + ".json", 'r')
            data = json.load(json_file)
            date = data["date"]
            our_answer = solve(data["grid"], data["across"], data["down"], data["grid_numbers"], trace_mod)
            self.central_widget = MainWidget(data, our_answer, date=date)

        self.setCentralWidget(self.central_widget)
        self.setWindowTitle("PROMINI NYT Mini CrossWord Solver")
        self.setWindowIcon(QIcon('Resources/nytimes.png')) 
        self.setFixedSize(QSize(*APP_SIZE))
        self.setStyleSheet("background-color: white;") 
        self.center()

    # Makes the app appear on the center of the screen
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

'''
Main widget class represents the main content of the application
It is inherited from QWidget
Takes puzzle and clue information 
Date can be specified for old puzzles, it is today's date by default
Consists of three parts: header, body and footer
Header includes title, date, author's name
Body is imported from another class
Footer includes current time, date and group name
'''
class MainWidget(QWidget):
    def __init__(self, official_sol, our_answer, date = None, trace_mod=False):
        super().__init__()  
        now = QDate.currentDate() 
        # Set date to current date if not specified
        self.todays_date = now.toString(Qt.DefaultLocaleLongDate) if date is None else date
        time = QTime.currentTime()
        self.current_time = time.toString(Qt.DefaultLocaleLongDate)
        self.grid = official_sol["grid"]
        self.grid_numbers = official_sol["grid_numbers"]
        self.answer = official_sol["answer"]
        self.across = official_sol["across"]
        self.down = official_sol["down"]
        self.our_answer = our_answer
        self.trace_mod = trace_mod
        self.initUI()  

    def initUI(self):
        # Import NYT custom font
        QFontDatabase.addApplicationFont("Resources/KarnakPro-CondensedBlack.ttf")

        # Header
        self.header = QVBoxLayout()
        top = QHBoxLayout()

        # Header label containing the title
        header_str = "The Mini Crossword"
        header_label = QLabel(header_str)
        header_label.setFont(QFont("KarnakPro-CondensedBlack", 30))
        header_label.setAlignment(Qt.AlignBottom)
        top.addWidget(header_label)

        # Date label containing the specified or today's date
        date_label = QLabel(self.todays_date)
        date_label.setFont(QFont("Franklin", 17, 10))
        date_label.setAlignment(Qt.AlignBottom)
        date_label.setIndent(7)
        top.addWidget(date_label)

        # Align contents to left
        top.addStretch(1)

        self.header.addLayout(top)

        # Label containing author's name
        joel_label = QLabel("By Joel Fagliano")
        joel_label.setFont(QFont("Franklin", 10))
        self.header.addWidget(joel_label)

        # Body (or middle part)
        self.body = QHBoxLayout()
        self.body.setSpacing(10)
        self.body.addWidget(Body(self.grid, self.grid_numbers, self.answer, self.across, self.down, self.our_answer, parent=self, trace_mod=self.trace_mod))

        # Footer
        self.footer = QHBoxLayout()

        # Creating a timer object to update the time and date every second
        timer = QTimer(self) 
        timer.timeout.connect(self.show_time) 
        timer.start(1000) 
        
        # Footer label containing current date and time along with group name
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
    
    # Updates date and time attributes of the class
    def show_time(self):
        now = QDate.currentDate() 
        self.todays_date = now.toString(Qt.DefaultLocaleLongDate)
        time = QTime.currentTime()
        self.current_time = time.toString(Qt.DefaultLocaleLongDate)
        footer_str = self.todays_date + '\n' + self.current_time + '\n' + GROUP_NAME
        self.footer_label.setText(footer_str)

def main():
    trace_mod = input("Do you want single stepping? (y/n):") in ["y", "Y", "yes", "Yes"]
    app = QApplication(sys.argv)
    window = App(trace_mod=trace_mod)
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()

