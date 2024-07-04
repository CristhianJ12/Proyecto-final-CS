import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QDialog, QSpinBox, QDialogButtonBox, QMessageBox, QSizePolicy, QSpacerItem
from PyQt5.QtCore import Qt, QTimer
import pygame  # Importar pygame para la reproducción de audio

# Inicializar pygame mixer
pygame.mixer.init()

# Conexión a la base de datos SQLite en un archivo
connection = sqlite3.connect('timers.db')
cursor = connection.cursor()

# Crear tabla para los temporizadores si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS timers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hours INTEGER,
                    minutes INTEGER,
                    seconds INTEGER,
                    is_running INTEGER DEFAULT 0
                )''')

class EditTimerDialog(QDialog):
    def __init__(self, timer_id, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Editar Cuenta Regresiva")
        self.timer_id = timer_id
        self.is_timer_running = False
        self.timer_seconds = 0

        layout = QVBoxLayout()

        self.hours_spinbox = QSpinBox()
        self.hours_spinbox.setRange(0, 23)
        self.minutes_spinbox = QSpinBox()
        self.minutes_spinbox.setRange(0, 59)
        self.seconds_spinbox = QSpinBox()
        self.seconds_spinbox.setRange(0, 59)

        self.start_button = QPushButton("Iniciar")
        self.pause_button = QPushButton("Pausar")
        self.stop_button = QPushButton("Detener")
        self.reset_button = QPushButton("Reiniciar")

        self.timer_label = QLabel("00:00:00")
        self.timer_label.setAlignment(Qt.AlignCenter)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        layout.addWidget(QLabel("Horas:"))
        layout.addWidget(self.hours_spinbox)
        layout.addWidget(QLabel("Minutos:"))
        layout.addWidget(self.minutes_spinbox)
        layout.addWidget(QLabel("Segundos:"))
        layout.addWidget(self.seconds_spinbox)

        layout.addWidget(self.timer_label)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.reset_button)

        layout.addLayout(button_layout)

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        button_box = QDialogButtonBox(buttons)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)
        self.setLayout(layout)

        # Cargar valores actuales del temporizador desde la base de datos
        self.load_timer_values()

        # Configurar estado inicial de los botones
        self.update_button_state()

        # Conectar acciones de botones
        self.start_button.clicked.connect(self.start_timer)
        self.pause_button.clicked.connect(self.pause_timer)
        self.stop_button.clicked.connect(self.stop_timer)
        self.reset_button.clicked.connect(self.reset_timer)

    def load_timer_values(self):
        cursor.execute("SELECT hours, minutes, seconds FROM timers WHERE id=?", (self.timer_id,))
        timer_values = cursor.fetchone()
        if timer_values:
            self.hours_spinbox.setValue(timer_values[0])
            self.minutes_spinbox.setValue(timer_values[1])
            self.seconds_spinbox.setValue(timer_values[2])

    def update_timer(self):
        self.timer_seconds -= 1
        if self.timer_seconds <= 0:
            self.timer.stop()
            self.timer_seconds = 0
            self.timer_label.setText("00:00:00")
            self.play_sound()  # Reproducir sonido
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Temporizador")
            msg_box.setText("¡Tiempo terminado!")
            msg_box.buttonClicked.connect(self.stop_sound)  # Conectar la señal de clic del botón al método stop_sound
            msg_box.exec_()
        else:
            hours = self.timer_seconds // 3600
            minutes = (self.timer_seconds % 3600) // 60
            seconds = self.timer_seconds % 60
            self.timer_label.setText(f"{hours:02}:{minutes:02}:{seconds:02}")

    def start_timer(self):
        self.timer_seconds = self.hours_spinbox.value() * 3600 + \
                             self.minutes_spinbox.value() * 60 + \
                             self.seconds_spinbox.value()
        self.timer.start(1000)
        self.is_timer_running = True
        self.update_button_state()

    def pause_timer(self):
        self.timer.stop()
        self.is_timer_running = False
        self.update_button_state()

    def stop_timer(self):
        self.timer.stop()
        self.is_timer_running = False
        self.timer_seconds = 0
        self.timer_label.setText("00:00:00")
        self.update_button_state()

    def reset_timer(self):
        self.hours_spinbox.setValue(0)
        self.minutes_spinbox.setValue(0)
        self.seconds_spinbox.setValue(0)
        self.timer_seconds = 0
        self.timer_label.setText("00:00:00")
        self.update_button_state()

    def update_button_state(self):
        self.start_button.setEnabled(not self.is_timer_running)
        self.pause_button.setEnabled(self.is_timer_running)
        self.stop_button.setEnabled(self.is_timer_running)
        self.reset_button.setEnabled(not self.is_timer_running)

    def play_sound(self):
        # Reproducir el archivo de sonido
        pygame.mixer.music.load('sound.mp3')
        pygame.mixer.music.play()

    def stop_sound(self):
        # Detener el archivo de sonido
        pygame.mixer.music.stop()

    def accept(self):
        # Guardar los cambios en la base de datos
        hours = self.hours_spinbox.value()
        minutes = self.minutes_spinbox.value()
        seconds = self.seconds_spinbox.value()

        if self.timer_id is None:
            # Crear nuevo temporizador en la base de datos
            cursor.execute("INSERT INTO timers (hours, minutes, seconds) VALUES (?, ?, ?)",
                           (hours, minutes, seconds))
        else:
            # Actualizar temporizador existente en la base de datos
            cursor.execute("UPDATE timers SET hours=?, minutes=?, seconds=? WHERE id=?",
                           (hours, minutes, seconds, self.timer_id))

        connection.commit()
        super().accept()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cuentas Regresivas")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.new_timer_button = QPushButton("Crear Nueva Cuenta Regresiva")
        self.new_timer_button.clicked.connect(self.create_new_timer)

        self.timer_table = QTableWidget()
        self.timer_table.setColumnCount(5)
        self.timer_table.setHorizontalHeaderLabels(["ID", "Horas", "Minutos", "Segundos", "Acciones"])

        layout.addWidget(self.new_timer_button)
        layout.addWidget(self.timer_table)

        self.setLayout(layout)

        self.load_timers()

    def load_timers(self):
        # Limpiar tabla
        self.timer_table.setRowCount(0)

        # Consultar temporizadores desde la base de datos
        cursor.execute("SELECT id, hours, minutes, seconds FROM timers")
        timers = cursor.fetchall()

        # Mostrar temporizadores en la tabla
        for row, timer in enumerate(timers):
            self.timer_table.insertRow(row)
            for col, value in enumerate(timer):
                item = QTableWidgetItem(str(value))
                if col < 4:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Hacer celdas no editables
                self.timer_table.setItem(row, col, item)

            # Botones de acciones para cada fila
            edit_button = QPushButton("Editar")
            edit_button.setFixedSize(40, 20)  # Ajustar tamaño del botón
            edit_button.setStyleSheet("font-size: 12px;")  # Ajustar el estilo del botón
            edit_button.clicked.connect(lambda _, row=row: self.edit_timer(row))

            delete_button = QPushButton("Eliminar")
            delete_button.setFixedSize(50, 20)  # Ajustar tamaño del botón
            delete_button.setStyleSheet("font-size: 12px;")  # Ajustar el estilo del botón
            delete_button.clicked.connect(lambda _, row=row: self.confirm_delete_timer(row))

            buttons_layout = QHBoxLayout()
            buttons_layout.addWidget(edit_button)
            buttons_layout.addSpacerItem(QSpacerItem(1, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))  # Añadir separador
            buttons_layout.addWidget(delete_button)
            buttons_layout.setAlignment(Qt.AlignCenter)  # Centrar los botones en la celda

            buttons_widget = QWidget()
            buttons_widget.setLayout(buttons_layout)

            self.timer_table.setCellWidget(row, 4, buttons_widget)

    def create_new_timer(self):
        dialog = EditTimerDialog(None, parent=self)
        if dialog.exec_() == QDialog.Accepted:
            # Recargar la tabla después de agregar el nuevo temporizador
            self.load_timers()

    def edit_timer(self, row):
        # Obtener el ID del temporizador seleccionado
        timer_id = int(self.timer_table.item(row, 0).text())

        # Abrir ventana de edición
        dialog = EditTimerDialog(timer_id, parent=self)
        if dialog.exec_() == QDialog.Accepted:
            # Recargar la tabla después de editar el temporizador
            self.load_timers()

    def confirm_delete_timer(self, row):
        # Mostrar mensaje de confirmación
        reply = QMessageBox.question(self, "Confirmar Eliminación",
                                     "¿Estás seguro de que deseas eliminar este temporizador?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.delete_timer(row)

    def delete_timer(self, row):
        # Obtener el ID del temporizador seleccionado
        timer_id = int(self.timer_table.item(row, 0).text())

        # Eliminar temporizador de la base de datos
        cursor.execute("DELETE FROM timers WHERE id=?", (timer_id,))
        connection.commit()

        # Recargar la tabla después de eliminar el temporizador
        self.load_timers()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    # Guardar cambios en la base de datos al cerrar la aplicación
    app.aboutToQuit.connect(connection.commit)

    sys.exit(app.exec_())
