import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtCore import QProcess, Qt
from PyQt5.QtGui import QFont

print("Python executable being used (PrincCode):", sys.executable)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Configurar la ventana principal
        self.setWindowTitle("Gestor de Tiempos")
        self.setGeometry(100, 100, 300, 250)

        # Crear un layout vertical principal
        main_layout = QVBoxLayout()

        # Crear y configurar el título
        title_label = QLabel("Gestor de Tiempos")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(25)
        title_font.setBold(True)
        title_label.setFont(title_font)

        # Crear y configurar la fuente de los botones
        button_font = QFont()
        button_font.setPointSize(15)

        # Crear botones
        btn_timer = QPushButton("Temporizador")
        btn_alarm = QPushButton("Alarma")
        btn_pomodoro = QPushButton("Pomodoro")

        # Ajustar tamaño y fuente de los botones
        button_size = 200
        btn_timer.setFixedSize(button_size, 50)
        btn_timer.setFont(button_font)
        btn_alarm.setFixedSize(button_size, 50)
        btn_alarm.setFont(button_font)
        btn_pomodoro.setFixedSize(button_size, 50)
        btn_pomodoro.setFont(button_font)

        # Conectar los botones con las funciones
        btn_timer.clicked.connect(self.open_timer)
        btn_alarm.clicked.connect(self.open_alarm)
        btn_pomodoro.clicked.connect(self.open_pomodoro)

        # Añadir título al layout principal
        main_layout.addWidget(title_label)

        # Crear un layout horizontal para centrar los botones
        button_layout = QVBoxLayout()
        button_layout.addWidget(btn_timer)
        button_layout.addWidget(btn_alarm)
        button_layout.addWidget(btn_pomodoro)
        button_layout.setAlignment(Qt.AlignCenter)

        button_layout_container = QHBoxLayout()
        button_layout_container.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))
        button_layout_container.addLayout(button_layout)
        button_layout_container.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Añadir layout horizontal con botones al layout principal
        main_layout.addLayout(button_layout_container)

        # Añadir espacios en el layout principal para centrar los botones verticalmente
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        main_layout.addLayout(button_layout_container)
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Establecer el layout en la ventana
        self.setLayout(main_layout)

    def open_timer(self):
        script_path = os.path.join(os.path.dirname(__file__), 'TempoCode.py')
        python_executable = sys.executable  # Asegura que usa el mismo intérprete que ejecuta este script
        QProcess.startDetached(python_executable, [script_path])

    def open_alarm(self):
        script_path = os.path.join(os.path.dirname(__file__),  'AlarmCode.py')
        python_executable = sys.executable
        QProcess.startDetached(python_executable, [script_path])

    def open_pomodoro(self):
        script_path = os.path.join(os.path.dirname(__file__), 'PomodoroCode.py')
        python_executable = sys.executable
        QProcess.startDetached(python_executable, [script_path])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
