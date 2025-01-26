import sys
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from UI.addEditCoffeeForm import Ui_Form as AddEditCoffeeFormUI
from UI.main_ui import Ui_MainWindow as MainWindowUI


class AddEditCoffeeForm(QDialog, AddEditCoffeeFormUI):
    def __init__(self, parent=None, record=None):
        super().__init__(parent)
        self.setupUi(self)
        self.record = record
        self.commit_button.clicked.connect(self.save_record)
        if record:
            self.load_record()

    def load_record(self):
        self.line_id.setText(str(self.record.value(0)))
        self.line_title.setText(self.record.value(1))
        self.line_roast.setText(self.record.value(2))
        self.line_ground.setText(self.record.value(3))
        self.line_about.setText(self.record.value(4))
        self.line_price.setText(str(self.record.value(5)))
        self.line_volume.setText(str(self.record.value(6)))

    def save_record(self):
        query = QSqlQuery()
        if self.record:
            query.prepare("""
                UPDATE coffee SET 
                name = ?, roast = ?, type = ?, description = ?, price = ?, volume = ?
                WHERE id = ?
            """)
            query.addBindValue(self.line_title.text())
            query.addBindValue(self.line_roast.text())
            query.addBindValue(self.line_ground.text())
            query.addBindValue(self.line_about.text())
            query.addBindValue(float(self.line_price.text()))
            query.addBindValue(int(self.line_volume.text()))
            query.addBindValue(int(self.line_id.text()))
        else:
            query.prepare("""
                INSERT INTO coffee (name, roast, type, description, price, volume) 
                VALUES (?, ?, ?, ?, ?, ?)
            """)
            query.addBindValue(self.line_title.text())
            query.addBindValue(self.line_roast.text())
            query.addBindValue(self.line_ground.text())
            query.addBindValue(self.line_about.text())
            query.addBindValue(float(self.line_price.text()))
            query.addBindValue(int(self.line_volume.text()))

        if not query.exec():
            print("Ошибка выполнения запроса:", query.lastError().text())
        self.accept()


class MainWindow(QMainWindow, MainWindowUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('data/coffee.sqlite')
        if not db.open():
            print("Ошибка подключения к базе данных")
            return

        self.model = QSqlTableModel(self, db)
        self.model.setTable('coffee')
        self.model.select()
        self.model.setHeaderData(0, QtCore.Qt.Orientation.Horizontal, "ID")
        self.model.setHeaderData(1, QtCore.Qt.Orientation.Horizontal, "Название")
        self.model.setHeaderData(2, QtCore.Qt.Orientation.Horizontal, "Степень обжарки")
        self.model.setHeaderData(3, QtCore.Qt.Orientation.Horizontal, "Тип кофе")
        self.model.setHeaderData(4, QtCore.Qt.Orientation.Horizontal, "Описание")
        self.model.setHeaderData(5, QtCore.Qt.Orientation.Horizontal, "Цена")
        self.model.setHeaderData(6, QtCore.Qt.Orientation.Horizontal, "Объём")
        self.table.setModel(self.model)

        self.addButton.clicked.connect(self.add_record)
        self.editButton.clicked.connect(self.edit_record)

    def add_record(self):
        dialog = AddEditCoffeeForm(self)
        if dialog.exec():
            self.model.select()

    def edit_record(self):
        selected = self.table.selectionModel().selectedRows()
        if selected:
            row = selected[0].row()
            record = self.model.record(row)
            dialog = AddEditCoffeeForm(self, record)
            if dialog.exec():
                self.model.select()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())