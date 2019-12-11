from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMessageBox
from db_connection.coffee_init_service import DBInitService


class Ui_coffee(QWidget):
    def __init__(self):
        super().__init__()
        self.DB = DBInitService()
        self.ui = uic.loadUi("database_setting/coffee.ui")
        # 슬롯시그널
        self.ui.btn_init.clicked.connect(self.db_init_service)
        self.ui.btn_restore.clicked.connect(self.db_restore_service)
        self.ui.btn_backup.clicked.connect(self.db_backup_service)
        self.ui.show()

    def db_init_service(self):
        res = self.DB.database_init_service()
        if res is True:
            QMessageBox.about(self, 'init', 'init')
        else:
            QMessageBox.about(self, 'init', 'Failed')

    def db_restore_service(self):
        a = self.DB.data_restore('product')
        b = self.DB.data_restore('sale')
        if (a & b) is True:
            QMessageBox.about(self, 'restore', 'restore')
        else:
            QMessageBox.about(self, 'restore', 'Failed')

    def db_backup_service(self):
        a = self.DB.data_backup('product')
        b = self.DB.data_backup('sale')
        if (a & b) is True:
            QMessageBox.about(self, 'backup', 'backup')
        else:
            QMessageBox.about(self, 'backup', 'Failed')
