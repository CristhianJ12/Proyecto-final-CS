import sys
import sqlite3
import pygame
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, \
    QTableWidgetItem, QHeaderView, QDialog, QTimeEdit, QLineEdit, QRadioButton, QMessageBox
from PyQt5.QtCore import QTimer, QTime, Qt

# Inicializar pygame
pygame.mixer.init()


class AlarmCreator(QDialog):
    def __init__(self, alarm_id=None):
        super().__init__()
        self.setWindowTitle("Editar Alarma" if alarm_id else "Crear Alarma")
        self.setGeometry(100, 100, 400, 200)
        self.alarm_id = alarm_id
        self.initUI()
        if alarm_id:
            self.load_alarm(alarm_id)

    def initUI(self):
        layout = QVBoxLayout()

        # Widgets para configurar la alarma
        self.timeEdit = QTimeEdit(self)
        self.timeEdit.setDisplayFormat("HH:mm:ss")
        layout.addWidget(self.timeEdit)

        self.description = QLineEdit(self)
        self.description.setPlaceholderText("Descripción de la alarma")
        layout.addWidget(self.description)

        self.repeat = QLineEdit(self)
        self.repeat.setPlaceholderText("Repetir cada X minutos (0 para no repetir)")
        layout.addWidget(self.repeat)

        # Botones de guardar y cancelar
        button_layout = QHBoxLayout()

        self.saveButton = QPushButton("Guardar", self)
        self.saveButton.clicked.connect(self.save_alarm)
        button_layout.addWidget(self.saveButton)

        self.cancelButton = QPushButton("Cancelar", self)
        self.cancelButton.clicked.connect(self.reject)
        button_layout.addWidget(self.cancelButton)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def load_alarm(self, alarm_id):
        conn = sqlite3.connect("alarms.db")
        cursor = conn.cursor()
        cursor.execute("SELECT time, description, repeat FROM alarms WHERE id = ?", (alarm_id,))
        alarm = cursor.fetchone()
        conn.close()

        if alarm:
            time, description, repeat = alarm
            self.timeEdit.setTime(QTime.fromString(time, "HH:mm:ss"))
            self.description.setText(description)
            self.repeat.setText(str(repeat))

    def save_alarm(self):
        time = self.timeEdit.time().toString()
        description = self.description.text()
        repeat = self.repeat.text()

        if not repeat.isdigit():
            QMessageBox.warning(self, "Error", "El campo 'Repetir' debe ser un número entero.")
            return

        conn = sqlite3.connect("alarms.db")
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS alarms (id INTEGER PRIMARY KEY, time TEXT, description TEXT, repeat INTEGER, active INTEGER)")

        if self.alarm_id:
            cursor.execute("UPDATE alarms SET time = ?, description = ?, repeat = ?, active = 1 WHERE id = ?",
                           (time, description, repeat, self.alarm_id))
        else:
            cursor.execute("INSERT INTO alarms (time, description, repeat, active) VALUES (?, ?, ?, ?)",
                           (time, description, repeat, 1))

        conn.commit()
        conn.close()
        self.accept()


class AlarmApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Creador de Alarmas")
        self.setGeometry(100, 100, 600, 400)
        self.initUI()
        self.load_alarms()

    def initUI(self):
        layout = QVBoxLayout()

        # Título
        self.title = QLabel("Creador de Alarmas", self)
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        # Hora actual
        self.currentTimeLabel = QLabel(self)
        self.currentTimeLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.currentTimeLabel)
        self.update_time()

        # Botón para crear alarma
        self.createAlarmButton = QPushButton("Crear Alarma", self)
        self.createAlarmButton.clicked.connect(self.open_alarm_creator)
        layout.addWidget(self.createAlarmButton)

        # Tabla de alarmas
        self.alarmTable = QTableWidget(self)
        self.alarmTable.setColumnCount(5)
        self.alarmTable.setHorizontalHeaderLabels(["Hora", "Descripción", "Repetir", "Activo", "Acciones"])
        self.alarmTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.alarmTable)

        self.setLayout(layout)

        # Timer para actualizar la hora cada segundo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def update_time(self):
        current_time = QTime.currentTime().toString("HH:mm:ss")
        self.currentTimeLabel.setText(current_time)

        # Revisa las alarmas y reproduce el sonido si es necesario
        self.check_alarms(current_time)

    def load_alarms(self):
        self.alarmTable.setRowCount(0)
        conn = sqlite3.connect("alarms.db")
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS alarms (id INTEGER PRIMARY KEY, time TEXT, description TEXT, repeat INTEGER, active INTEGER)")
        cursor.execute("SELECT * FROM alarms")
        alarms = cursor.fetchall()
        conn.close()

        for alarm in alarms:
            self.add_alarm_to_table(alarm)

    def add_alarm_to_table(self, alarm):
        row_position = self.alarmTable.rowCount()
        self.alarmTable.insertRow(row_position)

        for i, value in enumerate(alarm[1:]):
            self.alarmTable.setItem(row_position, i, QTableWidgetItem(str(value)))

        # Radio button para activar/desactivar alarma
        radio_button = QRadioButton()
        radio_button.setChecked(alarm[4] == 1)
        radio_button.toggled.connect(lambda state, alarm_id=alarm[0]: self.toggle_alarm(alarm_id, state))
        self.alarmTable.setCellWidget(row_position, 3, radio_button)

        # Botones de editar y eliminar
        button_layout = QHBoxLayout()

        edit_button = QPushButton("Editar")
        edit_button.setFixedSize(40, 20)  # Ajustar tamaño del botón
        edit_button.setStyleSheet("font-size: 12px;")  # Ajustar el estilo del botón
        edit_button.clicked.connect(lambda _, alarm_id=alarm[0]: self.open_alarm_editor(alarm_id))
        button_layout.addWidget(edit_button)

        delete_button = QPushButton("Eliminar")
        delete_button.setFixedSize(50, 20)  # Ajustar tamaño del botón
        delete_button.setStyleSheet("font-size: 12px;")  # Ajustar el estilo del botón
        delete_button.clicked.connect(lambda _, alarm_id=alarm[0]: self.delete_alarm(alarm_id))
        button_layout.addWidget(delete_button)

        widget = QWidget()
        widget.setLayout(button_layout)
        self.alarmTable.setCellWidget(row_position, 4, widget)

    def open_alarm_creator(self):
        dialog = AlarmCreator()
        if dialog.exec_():
            self.load_alarms()

    def open_alarm_editor(self, alarm_id):
        dialog = AlarmCreator(alarm_id)
        if dialog.exec_():
            self.load_alarms()

    def delete_alarm(self, alarm_id):
        conn = sqlite3.connect("alarms.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alarms WHERE id = ?", (alarm_id,))
        conn.commit()
        conn.close()
        self.load_alarms()

    def toggle_alarm(self, alarm_id, state):
        conn = sqlite3.connect("alarms.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE alarms SET active = ? WHERE id = ?", (1 if state else 0, alarm_id))
        conn.commit()
        conn.close()

    def check_alarms(self, current_time):
        try:
            conn = sqlite3.connect("alarms.db")
            cursor = conn.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS alarms (id INTEGER PRIMARY KEY, time TEXT, description TEXT, repeat INTEGER, active INTEGER)")
            cursor.execute("SELECT * FROM alarms WHERE active = 1")
            alarms = cursor.fetchall()
            for alarm in alarms:
                alarm_time = alarm[1]
                if alarm_time == current_time:
                    pygame.mixer.music.load("Sound.mp3")
                    pygame.mixer.music.play(-1)  # Reproduce en bucle
                    self.show_alarm_popup(alarm[2])  # Muestra la ventana emergente con la descripción de la alarma
                    if alarm[3] == 0:  # Si no se repite, desactivar la alarma
                        cursor.execute("UPDATE alarms SET active = 0 WHERE id = ?", (alarm[0],))
                    conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error checking alarms: {e}")

    def show_alarm_popup(self, description):
        try:
            popup = QMessageBox(self)
            popup.setWindowTitle("Alarma")
            popup.setText(f"¡Alarma! {description}")
            popup.setStandardButtons(QMessageBox.Ok)
            popup.buttonClicked.connect(self.stop_alarm)
            popup.exec_()
        except Exception as e:
            print(f"Error showing alarm popup: {e}")

    def stop_alarm(self):
        try:
            pygame.mixer.music.stop()
        except Exception as e:
            print(f"Error stopping alarm: {e}")


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = AlarmApp()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error running the application: {e}")
