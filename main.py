import PyQt5.QtWidgets as QW
import sys
import sqlite3
from PyQt5 import uic


class CoffeeInfo(QW.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.comboBox.setCurrentText("-")
        self.comboBox.currentTextChanged.connect(self.set_info)
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

    def set_info(self):
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(8)
        self.tableWidget.setVerticalHeaderLabels(self.title)
        self.tableWidget.setHorizontalHeaderLabels(["Характеристики"])
        title = self.comboBox.currentText()
        info = self.cur.execute(f"""SELECT * FROM coffee WHERE Name = '{title}'""").fetchall()[0]
        for i, elem in enumerate(info):
            self.tableWidget.setItem(i, 0, QW.QTableWidgetItem(str(elem)))
        self.tableWidget.setColumnWidth(0, 350)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QW.QApplication(sys.argv)
    ex = CoffeeInfo()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
