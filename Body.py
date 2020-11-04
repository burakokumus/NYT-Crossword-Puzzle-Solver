from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QBrush, QColor, QFont, QPainter, QPen
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QScrollArea, QVBoxLayout, QWidget

CELL_SIZE = 95

class Body(QWidget):
    def __init__(self, grid, grid_numbers, answer, across, down, parent=None, trace_mod=False):
        super().__init__(parent)
        self.trace_mod = trace_mod
        self.grid = grid
        self.puzzle_grid = PuzzleGrid(grid, grid_numbers, answer, parent=self)
        self.clue_bar = Toolbar(parent=self)
        self.across_clues = ClueListWrapper("across", across, parent=self)
        self.down_clues = ClueListWrapper("down", down, parent=self)
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout()
        buttons_and_grid = QVBoxLayout()
        buttons_and_grid.addWidget(self.clue_bar)
        buttons_and_grid.addWidget(self.puzzle_grid)
        hbox.addLayout(buttons_and_grid)
        hbox.addWidget(self.across_clues)
        hbox.addWidget(self.down_clues)
        self.setLayout(hbox)
        self.show()

class Toolbar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.setMaximumWidth(16 + CELL_SIZE * len(self.parent().grid[0]))

    def initUI(self):
        hbox = QHBoxLayout()
        puzzle_grid = self.parent().puzzle_grid

        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(puzzle_grid.clear)

        reveal_btn = QPushButton("Reveal")
        reveal_btn.clicked.connect(puzzle_grid.fill)

        solve_btn = QPushButton("Solve")
        hbox.addSpacing(3)
        hbox.addWidget(clear_btn)
        hbox.addSpacing(3)
        hbox.addWidget(reveal_btn)
        hbox.addSpacing(3)
        hbox.addWidget(solve_btn)
        self.setLayout(hbox)

class ClueListWrapper(QWidget):
    def __init__(self, title, clues, parent=None):
        super().__init__(parent)
        if self.parent().trace_mod:
            print("Initializing {} clues".format(title))
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
            str1 = ''.join(clue)
            object = QLabel(str1)          
            self.vbox.addWidget(object)

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
        if self.parent().trace_mod:
            print("Initializing the grid")
        self.grid = grid
        self.grid_numbers = grid_numbers
        self.current_fill = []
        self.answers = answers
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        self.setMinimumSize(10 + CELL_SIZE * len(self.grid[0]), 10 + CELL_SIZE * len(self.grid))
        self.show()

    def fill(self):
        self.current_fill = self.answers
        self.update()

    def clear(self):
        self.current_fill = [] 
        self.update()

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
                if len(self.current_fill) != 0:
                    if self.current_fill[i][j] != ' ':
                        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
                        font = QFont("Helvetica", 40)
                        painter.setFont(font)
                        painter.translate(0, 18)
                        painter.drawText(rect, Qt.AlignCenter, self.current_fill[i][j])
                        painter.translate(0, -18)
                
        # Paint the outer rectangle
        painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.transparent))
        painter.drawRect(7, 7, CELL_SIZE * len(self.grid[0]), CELL_SIZE * len(self.grid))