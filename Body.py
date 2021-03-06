from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QBrush, QColor, QFont, QPainter, QPen
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QScrollArea, QVBoxLayout, QWidget

# Side of a cell square in pixels
CELL_SIZE = 95

'''
Body class represents the body part of the app
It is inherited from QWidget
It has three parts: puzzle grid, across clues, down clues
'''
class Body(QWidget):
    def __init__(self, grid, grid_numbers, answer, across, down, our_answer, parent=None, trace_mod=False):
        super().__init__(parent)
        self.trace_mod = trace_mod
        # Initialize components
        self.official = PuzzleGrid(grid, grid_numbers, answer, parent=self)
        self.across_clues = ClueListWrapper("across", across, self.official.height(), parent=self)
        self.down_clues = ClueListWrapper("down", down, self.official.height(), parent=self)
        self.promini_sol = PuzzleGrid(grid, grid_numbers, our_answer, parent=self)
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout()
        hbox.addWidget(self.official)
        hbox.addWidget(self.across_clues)
        hbox.addWidget(self.down_clues)
        hbox.addWidget(self.promini_sol)
        self.setLayout(hbox)
        self.show()

'''
ClueListWrapper is a container for clue list and its title
It is inherited from QWidget
'''
class ClueListWrapper(QWidget):
    def __init__(self, title, clues, height, parent=None):
        super().__init__(parent)
        if self.parent().trace_mod:
            print("Initializing {} clues".format(title))
        self.initUI(title, clues, height)

    def initUI(self, title, clues, height):
        # Adjust height to match puzzle grid
        self.setFixedHeight(height + 15)
        layout = QVBoxLayout()
        self.title = ClueListTitle(title, parent=self)
        self.list = ClueList(clues, parent=self)
        layout.addWidget(self.title)
        layout.addWidget(self.list)
        self.setLayout(layout)

'''
ClueListTitle represents the title of a clue list
It is a specialized QLabel
Turns title string to uppercase and displays in bold Helvetice font
'''
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

'''
ClueList is a container for clue instances
It is inherited from QScrollArea and is scrollable
Requires clue list with their numbers
'''
class ClueList(QScrollArea):
    def __init__(self, clues, parent=None):
        super().__init__(parent)
        self.initUI(clues)
        
    def initUI(self, clues):      
        self.content = QWidget()
        self.vbox = QVBoxLayout()      

        # Add each clue to a horizontal box and then add the horizontal box to scroll area
        for clue in clues:
            hbox = QHBoxLayout()

            # Create a label with bold text for clue numbers
            number_label = QLabel()
            number_label.setText("<span style='font-size:10pt; font-weight:500;'>{}</span>".format(clue[0]))
            number_label.setMaximumSize(15, 25)

            # Create a label for clue text faithful to the original
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
    
'''
PuzzleGrid class displays the puzzle grid cells, question numbers and the answers
It is inherited from QWidget
'''
class PuzzleGrid(QWidget):
    def __init__(self, grid, grid_numbers, answers, parent=None):
        super().__init__(parent)
        if self.parent().trace_mod:
            print("Initializing the grid")
        self.grid = grid
        self.grid_numbers = grid_numbers
        self.answers = answers
        self.initUI()

    def initUI(self):
        self.setMinimumSize(10 + CELL_SIZE * len(self.grid[0]), 10 + CELL_SIZE * len(self.grid))
        self.setMaximumHeight(10 + CELL_SIZE * len(self.grid))
        self.show()

    '''
    Rendering function of the PuzzleGrid class
    Creates perfect square cells, paints them properly, puy little question numbers on top left of cells,
    put correct letter in the cells 
    '''
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