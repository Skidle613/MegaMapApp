import os
import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication
import requests


class Map(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 650, 450)
        self.setWindowTitle('MegsMapApp')
        self.initUI()

    def initUI(self):
        self.label = QLabel(self)
        self.label.move(0, 0)
        self.label.resize(650, 450)

        map_params = {
            "ll": '40.496638,52.895678',
            "l": "map",
            'size': '650,450',
            'z': '10'

            # "pt": f'{centre},pm2dol1'
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
        if not response:
            print("Ошибка выполнения запроса:")
            print(response.url)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        with open('map.png', 'wb') as file:
            file.write(response.content)
        self.pixmap = QPixmap('map.png')
        self.label.setPixmap(self.pixmap)

    def closeEvent(self, event):
        os.remove('map.png')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Map()
    ex.show()
    sys.exit(app.exec())
