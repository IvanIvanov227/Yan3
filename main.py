import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
import sqlite3


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.pushButton.clicked.connect(self.start)

    def start(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        string = 'SELECT * FROM coffee_info'
        result = cur.execute(string).fetchall()
        title = ['ID', 'Название', 'Степень обжарки', 'Состояние', 'Описание', 'Цена', 'Объём']
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(result):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                item = QTableWidgetItem(str(elem))
                self.tableWidget.setItem(i, j, item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
