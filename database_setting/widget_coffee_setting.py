from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from db_connection.coffee_init_service import DBInitService


class Ui_coffee(QWidget):
    def __init__(self):
        super().__init__()
        self.DB = DBInitService()
        self.ui = uic.loadUi("database_setting/coffee.ui")
        self.ui.btn_init.clicked.connect(self.DB.database_init_service)
        self.ui.btn_restore.clicked.connect(self.DB.database_restore_service)
        self.ui.btn_backup.clicked.connect(self.DB.database_backup_service)
        self.ui.show()

