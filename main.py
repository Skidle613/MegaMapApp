import os
import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication
from PyQt5.QtCore import Qt
import requests


class Map(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 650, 450)
        self.setWindowTitle('MegsMapApp')
        self.z = 10
        self.x_cor = 40.496638
        self.y_cor = 52.895678
        self.label = QLabel(self)
        self.label.move(0, 0)
        self.label.resize(650, 450)
        self.load_map()

    def closeEvent(self, event):
        os.remove('map.png')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown:
            if self.z > 0:
                self.z -= 1
                self.load_map()
        elif event.key() == Qt.Key_PageUp:
            if self.z < 17:
                self.z += 1
                self.load_map()
        if event.key() == Qt.Key_Up:
            self.y_cor += (170 / self.z) * 0.005 + (8.5 - self.z) * 0.01
            if self.z <= 6:
                self.y_cor += ((170 / self.z) * 0.005 + (8.5 - self.z) * 0.01) * 2
            self.load_map()
        elif event.key() == Qt.Key_Down:
            self.y_cor -= (170 / self.z) * 0.005 + (8.5 - self.z) * 0.01
            if self.z <= 6:
                self.y_cor -= ((170 / self.z) * 0.005 + (8.5 - self.z) * 0.01) * 2
            self.load_map()
        elif event.key() == Qt.Key_Left:
            self.x_cor -= (170 / self.z) * 0.005 + (8.5 - self.z) * 0.01
            if self.z <= 6:
                self.x_cor -= ((170 / self.z) * 0.005 + (8.5 - self.z) * 0.01) * 2
            self.load_map()
        elif event.key() == Qt.Key_Right:
            self.x_cor += (170 / self.z) * 0.005 + (8.5 - self.z) * 0.01
            if self.z <= 6:
                self.x_cor += ((170 / self.z) * 0.005 + (8.5 - self.z) * 0.01) * 2
            self.load_map()

    def load_map(self):
        map_params = {
            "ll": f'{self.x_cor},{self.y_cor}',
            "l": "map",
            'size': '650,450',
            'z': self.z

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Map()
    ex.show()
    sys.exit(app.exec())
