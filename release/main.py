from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
import sqlite3
from release.addEditCoffeeForm import Ui_Form
from main_ui import Ui_MainWindow


class ErrorLen(Exception):
    pass


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.edit_coffee = None
        self.add_coffee = None
        self.update()
        self.addButton.clicked.connect(self.add_info)
        self.editButton.clicked.connect(self.edit_info)

    def update(self):
        con = sqlite3.connect('../data/coffee.sqlite')
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

    def add_info(self):
        self.add_coffee = AddEditCoffeeForm(parent=self)
        self.add_coffee.show()

    def edit_info(self):
        row = self.tableWidget.currentRow()
        id_coffee = int(self.tableWidget.item(row, 0).text())
        self.edit_coffee = AddEditCoffeeForm(parent=self, coffee_id=id_coffee)
        self.edit_coffee.show()


class AddEditCoffeeForm(QMainWindow, Ui_Form):
    def __init__(self, parent=None, coffee_id=None):
        super().__init__(parent)
        self.setupUi(self)
        self.coffee_id = coffee_id
        self.con = sqlite3.connect('../data/coffee.sqlite')
        self.cur = self.con.cursor()

        if coffee_id is None:
            self.setWindowTitle('Добавление записи')
            self.pushButton.setText('Добавить')
            self.add()
            self.pushButton.clicked.connect(self.save_add)

        else:
            self.setWindowTitle('Редактирование записи')
            self.pushButton.setText('Изменить')
            self.add()
            self.edit()
            self.pushButton.clicked.connect(self.save_edit)

    def add(self):
        self.roasting.addItems(['светлая', 'темная'])
        self.condition.addItems(['молотый', 'в зернах'])

    def edit(self):
        string = 'SELECT * FROM coffee_info WHERE id = ?'
        res = self.cur.execute(string, (self.coffee_id, )).fetchone()
        title = res[1]
        roasting = res[2]
        condition = res[3]
        description = res[4]
        price = res[5]
        volume = res[6]
        self.title.setPlainText(title)
        self.roasting.setCurrentText(roasting)
        self.condition.setCurrentText(condition)
        self.description.setPlainText(description)
        self.price.setPlainText(str(price))
        self.volume.setPlainText(str(volume))

    def save_add(self):
        try:
            title = self.title.toPlainText()
            roasting = self.roasting.currentText()
            condition = self.condition.currentText()
            description = self.description.toPlainText()
            price = round(float(self.price.toPlainText()), 2)
            volume = round(float(self.volume.toPlainText()), 2)
            if title == '' or description == '' or price == '' or volume == '':
                raise ErrorLen

            string = '''INSERT INTO coffee_info(name, roasting, condition, description, price, volume)
                        VALUES (?, ?, ?, ?, ?, ?)'''
            self.cur.execute(string, (title, roasting, condition, description, price, volume))
            self.con.commit()
            self.parent().update()
            self.hide()

        except ValueError:
            pass

        except ErrorLen:
            pass

    def save_edit(self):
        try:
            title = self.title.toPlainText()
            roasting = self.roasting.currentText()
            condition = self.condition.currentText()
            description = self.description.toPlainText()
            price = round(float(self.price.toPlainText()), 2)
            volume = round(float(self.volume.toPlainText()), 2)
            if title == '' or description == '' or price == '' or volume == '':
                raise ErrorLen

            string = '''UPDATE coffee_info SET
                        name = ?, roasting = ?, condition = ?, description = ?, price = ?, volume = ?
                        WHERE id = ?'''
            self.cur.execute(string, (title, roasting, condition, description, price, volume, self.coffee_id))
            self.con.commit()
            self.parent().update()
            self.hide()

        except ValueError:
            pass

        except ErrorLen:
            pass
