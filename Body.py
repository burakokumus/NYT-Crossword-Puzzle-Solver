import sys
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QBrush, QColor, QFont, QFontDatabase, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QPushButton, QScrollArea, QSizePolicy, QVBoxLayout, QWidget

CELL_SIZE = 95

class Body(QWidget):
    def __init__(self, grid, grid_numbers, answer, across, down, parent=None):
        super().__init__(parent)
        self.grid = grid
        self.puzzle_grid = PuzzleGrid(grid, grid_numbers, answer, parent=self)
        self.across_clues = ClueListWrapper("Across", across, parent=self)
        self.down_clues = ClueListWrapper("Down", down, parent=self)
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout()
        hbox.addWidget(self.puzzle_grid)
        hbox.addWidget(self.across_clues)
        hbox.addWidget(self.down_clues)
        self.setLayout(hbox)
        self.show()

class ClueListWrapper(QWidget):
    def __init__(self, title, clues, parent=None):
        super().__init__(parent)
        self.initUI(title, clues)

    def initUI(self, title, clues):
        layout = QVBoxLayout()
        self.title = ClueListTitle(title, parent=self)
        self.list = ClueList(clues, parent=self)
        layout.addWidget(self.title)
        layout.addWidget(self.list)
        self.setLayout(layout)

class ClueListTitle(QLabel):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.title = title.upper()
        self.initUI()
        
    def initUI(self):
        self.setFont(QFont("Helvetica"))
        self.setStyleSheet("font-size:10pt; font-weight: 700;");
        self.setText(self.title)       
        self.setAlignment(Qt.AlignLeft)

class ClueList(QScrollArea):
    def __init__(self, clues, parent=None):
        super().__init__(parent)
        self.initUI(clues)
        
    def initUI(self, clues):      
        self.content = QWidget()
        self.vbox = QVBoxLayout()      

        for clue in clues:
            hbox = QHBoxLayout()
            str1 = ''.join(clue)
            number_label = QLabel()
            number_label.setText("<span style='font-size:10pt; font-weight:500;'>{}</span>".format(clue[0]))
            number_label.setMaximumSize(15, 25)
            clue_label = QLabel()   
            clue_label.setText("<span style='font-size:10pt; font-weight:200;'>{}</span>".format(clue[1]))  
            clue_label.setWordWrap(True)
            hbox.addWidget(number_label, 0, Qt.AlignTop)
            hbox.addWidget(clue_label)
            self.vbox.addLayout(hbox)
            self.vbox.addSpacing(5)

        self.vbox.addStretch(1)
        self.content.setLayout(self.vbox)

        #Scroll Area Properties
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setWidget(self.content)

class PuzzleGrid(QWidget):
    def __init__(self, grid, grid_numbers, answers, parent=None):
        super().__init__(parent)
        self.grid = grid
        self.grid_numbers = grid_numbers
        self.answers = answers
        self.initUI()

    def initUI(self):
        self.setMinimumSize(10 + CELL_SIZE * len(self.grid[0]), 10 + CELL_SIZE * len(self.grid))
        self.show()

    def paintEvent(self, e):
        painter = QPainter(self)

        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                # If cell is filled, set brush to black, white otherwise
                if cell == 1:
                    painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
                else:
                    painter.setBrush(QBrush(Qt.white, Qt.SolidPattern))  
                
                # Create the corresponding grid cell
                rect = QRect(7 + CELL_SIZE * j, 7 + CELL_SIZE * i, CELL_SIZE, CELL_SIZE)
                painter.setPen(QPen(QColor(105,105,105), 1, Qt.SolidLine))
                painter.drawRect(rect)

                # Write the question number into the cell (if any) 
                if self.grid_numbers[i][j] != 0:
                    # Move the painter by 5 pixels to write question numbers in a cell
                    painter.translate(5, 5)
                    painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
                    font = QFont("Helvetica", 15)
                    painter.setFont(font)
                    painter.drawText(rect, Qt.AlignTop, str(self.grid_numbers[i][j]))
                    painter.translate(-5, -5)

                # Write the letter into the cell (if any) 
                if len(self.answers) != 0:
                    if self.answers[i][j] != ' ':
                        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
                        font = QFont("Helvetica", 40)
                        painter.setFont(font)
                        painter.translate(0, 18)
                        painter.drawText(rect, Qt.AlignCenter, self.answers[i][j])
                        painter.translate(0, -18)
                
        # Paint the outer rectangle
        painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.transparent))
        painter.drawRect(7, 7, CELL_SIZE * len(self.grid[0]), CELL_SIZE * len(self.grid))