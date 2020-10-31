import sys
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QBrush, QColor, QFont, QFontDatabase, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QScrollArea, QSizePolicy, QVBoxLayout, QWidget

CELL_SIZE = 82

# Default 5x5 crossword puzzle. 
grid = [[1, 1, 0, 0, 0], 
        [1, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0], 
        [0, 0, 0, 1, 0], 
        [1, 1, 0, 0, 0]]

question_numbers = [[1, 1, 1, 2, 3], 
                    [1, 4, 0, 0, 0], 
                    [5, 0, 0, 0, 0], 
                    [6, 0, 0, 1, 0], 
                    [1, 1, 7, 0, 0]]

class Body(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout()
        clue_and_grid = QVBoxLayout()
        self.clue_bar = ClueBar(parent=self)
        self.puzzle_grid = PuzzleGrid(parent=self)
        clue_and_grid.addWidget(self.clue_bar)
        clue_and_grid.addWidget(self.puzzle_grid)
        hbox.addLayout(clue_and_grid)
        hbox.addWidget(ClueListWrapper("Across", [str(i) for i in range(3)], parent=self))
        hbox.addWidget(ClueListWrapper("Down", [str(i) for i in range(50)], parent=self))
        self.setLayout(hbox)
        self.show()

class ClueBar(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.setMaximumWidth(7 + CELL_SIZE * len(grid[0]))

    def initUI(self):
        self.setFont(QFont("Franklin", 10))
        self.setStyleSheet("background-color: rgb(220, 239, 255); padding:10px")
        self.setText("Clue bar")
        self.setWordWrap(True)

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
        self.initUI(title)
        
    def initUI(self, title):
        self.setFont(QFont("Franklin", 10))
        self.setText(title)       
        self.setAlignment(Qt.AlignLeft)

class ClueList(QScrollArea):
    def __init__(self, clues, parent=None):
        super().__init__(parent)
        self.initUI(clues)
        
    def initUI(self, clues):      
        self.content = QWidget()
        self.vbox = QVBoxLayout()      

        for clue in clues:
            object = QLabel(clue)          
            self.vbox.addWidget(object)

        self.vbox.addStretch(1)
        self.content.setLayout(self.vbox)

        #Scroll Area Properties
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setWidget(self.content)

class PuzzleGrid(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        self.setMinimumSize(7 + CELL_SIZE * len(grid[0]), 7 + CELL_SIZE * len(grid))
        self.show()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(QPen(QColor(171,171,172), 1, Qt.SolidLine))
        font = QFont("Helvetica", 20)
        painter.setFont(font)
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if cell == 1:
                    painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
                else:
                    painter.setBrush(QBrush(Qt.white, Qt.SolidPattern))  
                rect = QRect(7 + CELL_SIZE * j, 7 + CELL_SIZE * i, CELL_SIZE, CELL_SIZE)
                painter.translate(-5, -5)
                painter.setPen(QPen(QColor(105,105,105), 1, Qt.SolidLine))
                painter.drawRect(rect)
                painter.translate(5, 5)
                painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
                if question_numbers[i][j] != 0:
                    painter.drawText(rect, Qt.AlignTop, str(question_numbers[i][j]))
        painter.translate(-5, -5)
        painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.transparent))
        painter.drawRect(7, 7, CELL_SIZE * len(grid[0]), CELL_SIZE * len(grid))

def main():
    app = QApplication(sys.argv)
    window = Body()
    window.show()
    app.exec_()
    


if __name__ == '__main__':
    main()