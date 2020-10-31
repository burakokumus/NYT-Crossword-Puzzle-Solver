import sys
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QBrush, QColor, QFont, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QVBoxLayout, QWidget

CELL_SIZE = 82

# Default 5x5 crossword puzzle. 
grid = [[1, 1, 0, 0, 0], 
        [1, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0], 
        [0, 0, 0, 1, 0], 
        [1, 1, 0, 0, 0]]

question_numbers = [[1, 1, 0, 0, 0], 
                    [1, 0, 0, 0, 0], 
                    [0, 0, 0, 0, 0], 
                    [0, 0, 0, 1, 0], 
                    [1, 1, 0, 0, 0]]

class PuzzleGrid(QWidget):
    def __init__(self, parent=None):
        super(PuzzleGrid, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setStyleSheet("margin:0; border:1px solid rgb(0, 255, 0); ")
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
                rect = QRect(14 + CELL_SIZE * j, 14 + CELL_SIZE * i, CELL_SIZE, CELL_SIZE)
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
        painter.drawRect(13, 13, CELL_SIZE * len(grid[0]), CELL_SIZE * len(grid[0]))

def main():
    app = QApplication(sys.argv)
    window = PuzzleGrid()
    window.show()
    app.exec_()
    


if __name__ == '__main__':
    main()