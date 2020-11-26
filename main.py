import PyQt5.QtWidgets as QW
import sys
import sqlite3
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets


class CoffeeInfo(QW.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.comboBox.setCurrentText("-")
        self.comboBox.currentTextChanged.connect(self.set_info)
        self.btn.clicked.connect(self.add_coffee)
        self.btn2.clicked.connect(self.edit_coffee)
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()
        self.title = ["ID",
                      "Название",
                      "Сорт",
                      "Степень обжарки",
                      "Вид",
                      "Описание вкуса",
                      "Цена",
                      "Объем упаковки"]

    def add_coffee(self):
        self.dialog = AddDialog(par=self)
        self.dialog.show()

    def edit_coffee(self):
        self.dialog = AddDialog(self.comboBox.currentText(), self)
        self.dialog.show()

    def set_info(self):
        try:
            self.tableWidget.setColumnCount(1)
            self.tableWidget.setRowCount(8)
            self.tableWidget.setVerticalHeaderLabels(self.title)
            self.tableWidget.setHorizontalHeaderLabels(["Характеристики"])
            title = self.comboBox.currentText()
            info = self.cur.execute(f"""SELECT * FROM coffee WHERE Name = '{title}'""").fetchall()[0]
            for i, elem in enumerate(info):
                self.tableWidget.setItem(i, 0, QW.QTableWidgetItem(str(elem)))
            self.tableWidget.setColumnWidth(0, 360)
        except:
            pass


class AddDialog(QW.QMainWindow):
    def __init__(self, title="", par=None):
        super().__init__()
        self.title = title
        self.par = par
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()
        uic.loadUi("addEditCoffeeForm.ui", self)
        if self.title != "":
            self.set_params()
        self.save_btn.clicked.connect(self.accept)

    def accept(self):
        if self.check_all():
            Id = list(map(lambda x: str(x[0]), self.cur.execute("""SELECT ID FROM coffee""").fetchall()))
            if self.lineEdit_1.text() in Id and self.title == "":
                message = QW.QMessageBox.question(
                    self, '', f"Кофе с таким ID уже существует! Попробуйте другой",
                    QW.QMessageBox.Ok)
            else:
                self.cur.execute(f"""DELETE FROM coffee
                            WHERE Name = '{self.lineEdit_2.text()}'""")
                self.cur.execute(f"""INSERT INTO coffee
                                VALUES ('{self.lineEdit_1.text()}', '{self.lineEdit_2.text()}',
                                '{self.lineEdit_3.text()}', '{self.lineEdit_4.text()}',
                                '{self.lineEdit_5.text()}', '{self.lineEdit_6.text()}',
                                '{self.lineEdit_7.text()}', '{self.lineEdit_8.text()}');""")
                self.con.commit()
                self.par.comboBox.clear()
                content = self.cur.execute("""SELECT DISTINCT Name, ID FROM coffee
                        ORDER BY ID ASC""").fetchall()
                content = list(map(lambda x: [x[0], int(x[1])], content))
                content.sort(key=lambda x: x[1])
                for i in content:
                    self.par.comboBox.addItem(i[0])
                self.destroy()
        else:
            message = QW.QMessageBox.question(
                self, '', f"Не все поля заполнены! Заполните всё.",
                QW.QMessageBox.Ok)

    def set_params(self):
        params = self.cur.execute(f"""SELECT * FROM coffee WHERE Name = '{self.title}'""").fetchall()[0]
        for i in range(8):
            eval(f"self.lineEdit_{i + 1}.setText('{params[i]}')")

    def check_all(self):
        c = 0
        for i in range(1, 9):
            if eval(f"self.lineEdit_{i}.text() == ''"):
                break
            c += 1
        return c == 8


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QW.QApplication(sys.argv)
    ex = CoffeeInfo()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
