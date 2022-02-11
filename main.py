import os
import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
import requests
from sob import size


class Map(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 650, 550)
        self.setWindowTitle('MegsMapApp')
        self.z = 10
        self.x_cor = 40.496638
        self.y_cor = 52.895678
        self.mods = ['map', 'sat', 'sat,skl']
        self.l = 0
        self.label = QLabel(self)
        self.label.move(0, 0)
        self.label.resize(650, 450)
        self.lineEdit = QLineEdit(self)
        self.lineEdit.move(0, 450)
        self.lineEdit.resize(550, 100)
        self.pButton = QPushButton('Искать', self)
        self.pButton.move(550, 450)
        self.pButton.resize(100, 100)
        self.pButton.clicked.connect(self.search_obj)
        self.pts = []
        self.load_map()

    def closeEvent(self, event):
        os.remove('map.png')

    def search_obj(self):
        centre = size(self.lineEdit.text())
        self.x_cor = float(centre[0])
        self.y_cor = float(centre[1])
        self.pts.append(f'{",".join([centre[0], centre[1]])},pm2dol1')
        self.load_map()

    def mousePressEvent(self, event):
        if event.pos().x() in range(0, 551) and event.pos().y() in range(450, 551):
            self.lineEdit.setFocus()
        else:
            self.lineEdit.clearFocus()

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
            old = self.y_cor
            self.y_cor += 1 / ((self.z + 0.000000001) ** 2) * (17.3 - self.z)
            try:
                self.load_map()
            except Exception:
                self.y_cor = old
        elif event.key() == Qt.Key_Down:
            old = self.y_cor
            self.y_cor -= 1 / ((self.z + 0.000000001) ** 2) * (17.3 - self.z)
            try:
                self.load_map()
            except Exception:
                self.y_cor = old
        elif event.key() == Qt.Key_Left:
            old = self.x_cor
            self.x_cor -= 1 / ((self.z + 0.000000001) ** 2) * (17.3 - self.z)
            try:
                self.load_map()
            except Exception:
                self.x_cor = old
        elif event.key() == Qt.Key_Right:
            old = self.x_cor
            self.x_cor += 1 / ((self.z + 0.000000001) ** 2) * (17.3 - self.z)
            try:
                self.load_map()
            except Exception:
                self.x_cor = old
        if event.key() == Qt.Key_1:
            self.l = 0
            self.load_map()
        elif event.key() == Qt.Key_2:
            self.l = 1
            self.load_map()
        elif event.key() == Qt.Key_3:
            self.l = 2
            self.load_map()

    def load_map(self):
        map_params = {
            "ll": f'{self.x_cor},{self.y_cor}',
            "l": self.mods[self.l],
            'size': '650,450',
            'z': self.z,
            "pt": self.pts
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
        if not response:
            print("Ошибка выполнения запроса:")
            print(response.url)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            raise Exception('все пошло не так')
        with open('map.png', 'wb') as file:
            file.write(response.content)
        self.pixmap = QPixmap('map.png')
        self.label.setPixmap(self.pixmap)

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Map()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
