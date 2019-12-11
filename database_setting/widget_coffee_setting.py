from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMessageBox
from db_connection.coffee_init_service import DBInitService


class Ui_coffee(QWidget):
    def __init__(self):
        super().__init__()
        self.DB = DBInitService()
        self.ui = uic.loadUi("database_setting/coffee.ui")
        self.ui.btn_init.clicked.connect(self.db_init_service)
        self.ui.btn_restore.clicked.connect(self.db_restore_service)
        self.ui.btn_backup.clicked.connect(self.db_backup_service)
        self.ui.show()

    def db_init_service(self):
        self.DB.database_init_service()
        QMessageBox.about(self, 'init', 'init')

    def db_restore_service(self):
        self.DB.data_restore('product')
        self.DB.data_restore('sale')
        QMessageBox.about(self, 'restore', 'restore')

    def db_backup_service(self):
        self.DB.data_backup('product')
        self.DB.data_backup('sale')
        QMessageBox.about(self, 'backup', 'backup')