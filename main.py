from PyQt5.QtWidgets import QApplication
from database_setting.widget_coffee_setting import Ui_coffee

if __name__ == "__main__":
    app = QApplication([])
    w = Ui_coffee()
    exit(app.exec())
