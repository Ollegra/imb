from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStatusBar,
                             QLineEdit, QPushButton, QFrame, QLabel, QSizePolicy, QMessageBox)
from PyQt6.QtGui import QPainter, QConicalGradient, QPen, QColor, QFont, QLinearGradient, QBrush, QPalette, QIcon
from PyQt6.QtCore import Qt, QPointF
import math

class GradientTorusProgressBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0  # Значение прогресса
        self._maxValue = 75  # Максимальное значение
        self._thickness = 50  # Толщина тора

    def setValue(self, value):
        if 0 <= value <= self._maxValue:
            self._value = value
            self.update()
        else:
            QMessageBox.information(self, 'Ошибка', f"Значение {value} выходит за пределы диапазона.")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Размеры и центр
        rect = self.rect()
        center = QPointF(rect.center())
        radius = int(min(rect.width(), rect.height()) // 2 - self._thickness)

        # Создание фиксированного градиента
        gradient = QConicalGradient(center, 90)
        #gradient.setColorAt(0.0, QColor(169, 169, 169))  # Серый (старт)
        #gradient.setColorAt(0.3, QColor(0, 255, 0))      # Зелёный
        #gradient.setColorAt(0.6, QColor(255, 255, 0))    # Жёлтый
        #gradient.setColorAt(1.0, QColor(255, 0, 0))      # Красный (конец)
        gradient.setColorAt(0.0, QColor(255, 0, 0))  # Красный (конец)
        gradient.setColorAt(0.6, QColor(255, 255, 0))  # Жёлтый
        gradient.setColorAt(0.7, QColor(0, 255, 0))  # Зелёный
        gradient.setColorAt(1.0, QColor(65, 105, 255))  # Серый (старт)
        # Отрисовка тора
        pen = QPen(gradient, self._thickness, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawArc(int(center.x() - radius), int(center.y() - radius),
                        int(2 * radius), int(2 * radius), 0, 360 * 16)

        # Отрисовка стрелки
        angle = 360 * self._value / self._maxValue  # Угол для значения
        angle_rad = math.radians(angle - 90)  # Начало стрелки сверху
        arrow_length = radius - self._thickness // 2 + 45

        end_x = center.x() + arrow_length * math.cos(angle_rad)
        end_y = center.y() + arrow_length * math.sin(angle_rad)

        # Стрелка только на торе
        painter.setPen(QPen(QColor(255, 0, 0), 2))  # Чёрный цвет стрелки
        painter.drawLine(
            QPointF(center.x() + radius * 0.4 * math.cos(angle_rad),
                    center.y() + radius * 0.4 * math.sin(angle_rad)),
            QPointF(end_x, end_y)
        )

        # Текст значения в центре
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, f"ИМТ-{self._value}")

        # Отрисовка надписей около значений
        self.drawLabel(painter, center, radius, 14, " дефицит")
        self.drawLabel(painter, center, radius, 22, " норма")
        self.drawLabel(painter, center, radius, 30, " избыток")
        self.drawLabel(painter, center, radius, 45, " ожирение")

    def drawLabel(self, painter, center, radius, value, text):
        """Рисует текст около заданного значения на торе."""
        angle = 360 * value / self._maxValue
        angle_rad = math.radians(angle - 90)
        label_x = center.x() + (radius + self._thickness // 2) * math.cos(angle_rad)
        label_y = center.y() + (radius + self._thickness // 2) * math.sin(angle_rad)

        painter.setPen(QColor(0, 0, 255))
        painter.setFont(QFont("Arial", 8))
        painter.drawText(QPointF(label_x, label_y), text)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        gradient = QLinearGradient(0, 0, 1, 1)
        #gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setCoordinateMode(QLinearGradient.CoordinateMode.ObjectBoundingMode)
        gradient.setColorAt(0.0, QColor("lightblue"))
        gradient.setColorAt(1.0, QColor("grey"))

        # Применяем градиент в качестве кисти
        brush = QBrush(gradient)

        # Настраиваем палитру для фона
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, brush)
        self.setPalette(palette)
        self.setWindowTitle("Индекс массы тела")
        self.setWindowIcon(QIcon("risk.png"))
        self.setStyleSheet("""
                            QLineEdit {
                                border: 1px solid gray;
                                border-radius: 10px;
                                font-size: 14px;
                            }
                            QLineEdit:focus {
                                border: 2px solid gray;
                                background-color: #F2F2F2;
                            }
                            QLabel {
                                font-size: 14px;
                                padding: 5px 5px;
                            }
                            QPushButton {
                                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                                            stop: 0 lightblue, stop: 1 #FAFBFE); 
                                border-radius: 7px;
                                border: none;
                                padding: 5px 5px;
                            }
                            QPushButton:hover {
                                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                                            stop: 0 #FAFBFE, stop: 1 lightblue); 
                                color: #FF0000;
                            }
                        """)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)

        # Основной макет
        main_layout = QVBoxLayout(self)

        data_layout = QHBoxLayout(self)

        self.inputWeight = QLineEdit(self)
        self.inputWeight.setPlaceholderText("Введите вес, кг")
        data_layout.addWidget(self.inputWeight)

        self.inputHeight = QLineEdit(self)
        self.inputHeight.setPlaceholderText("Введите рост, м")
        data_layout.addWidget(self.inputHeight)

        self.updateButton = QPushButton("Определить ИМТ", self)
        self.updateButton.clicked.connect(self.updateValue)
        data_layout.addWidget(self.updateButton)

        main_layout.addLayout(data_layout)
        main_layout.addWidget(line)

        # Круговой индикатор
        self.torus = GradientTorusProgressBar(self)
        self.torus.resize(100, 100)
        #self.torus.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        main_layout.addWidget(self.torus)

        self.diagnose = QLabel("")
        self.diagnose.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.diagnose.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        main_layout.addWidget(self.diagnose)

        self.setLayout(main_layout)


    def updateValue(self):
        try:
            bmi = float(self.inputWeight.text()) / (float(self.inputHeight.text()) ** 2) # Получение значения из поля ввода
            match bmi:
                case bmi if bmi < 16:
                    diagnos_text = ["Очень большой дефицит массы тела", "color: white;"]
                case bmi if bmi >= 16 and bmi < 17:
                    diagnos_text = ["Выраженный дефицит массы тела", "color: lightblue;"]
                case bmi if bmi >= 17 and bmi < 18.5:
                    diagnos_text = ["Недостаточная масса тела", "color: lightblue;"]
                case bmi if bmi >= 18.5 and bmi < 25:
                    diagnos_text = ["Нормальная масса тела", "color: lightgreen;"]
                case bmi if bmi >= 25 and bmi < 30:
                    diagnos_text = ['Избыточная масса тела', 'color: gold;']
                case bmi if bmi >= 30 and bmi < 35:
                    diagnos_text = ["Ожирение 1-й степени", "color: red;"]
                case bmi if bmi >= 35 and bmi < 40:
                    diagnos_text = ["Ожирение 2-й степени", "color: red;"]
                case bmi if bmi >= 40:
                    diagnos_text = ["Ожирение 3-й степени", "color: red;"]
                case _:
                    diagnos_text = "Индекс массы тела не определен"

            self.torus.setValue(round(bmi, 1))  # Обновление значения индикатора
            self.diagnose.setText(diagnos_text[0])
            self.diagnose.setStyleSheet(f"{diagnos_text[1]}")
        except ValueError:
            QMessageBox.information(self, 'Ошибка', "Hе корректное числовое значение.")


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.resize(350, 350)
    window.show()

    app.exec()
