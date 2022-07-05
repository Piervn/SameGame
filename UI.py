from operator import eq, ne
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QMessageBox
import sys

class Window(QMainWindow):
    def __init__(self, ax, ay, width, height, size = 10):
        super().__init__()
        self.size = size
        self.setGeometry(ax, ay, width, height)
        self.setWindowTitle("SameGame")
        self.initUI()
        self.show()
        
    def initUI(self):
        widget = QWidget()
        self.setCentralWidget(widget)
        self.init_board(widget)
        
    def init_board(self, widget):
        self.board = QWidget()
        self.grid = QGridLayout()
        self.grid_buttons = {}
        for i in range(self.size):
            for j in range(self.size):
                x = self.size - i - 1
                y = j
                button = QPushButton(f'{x} {y}')
                button.setMinimumSize(50, 50)
                self.grid_buttons[x, y] = button
                self.grid.addWidget(self.grid_buttons[x, y], i, j)
        widget.setLayout(self.grid)
    
    
def RunWindow():
    WIDTH = 600
    HEIGHT = 600
    AX = 600
    AY = 300
    app = QApplication(sys.argv)
    win = Window(AX, AY, WIDTH, HEIGHT)
    sys.exit(app.exec())
    
RunWindow()