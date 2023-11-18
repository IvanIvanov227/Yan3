import sys

from PyQt5.QtWidgets import QApplication

from main import MyWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
