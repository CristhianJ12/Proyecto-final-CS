import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox,
    QTableWidget, QTableWidgetItem, QDialog, QLabel, QLineEdit, QHBoxLayout
)
from PyQt5.QtCore import Qt, QTimer
from pygame import mixer

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('pomodoro_timers.db')
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS timers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            work_time INTEGER NOT NULL,
            break_time INTEGER NOT NULL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_timer(self, work_time, break_time):
        query = "INSERT INTO timers (work_time, break_time) VALUES (?, ?)"
        self.conn.execute(query, (work_time, break_time))
        self.conn.commit()

    def get_timers(self):
        query = "SELECT * FROM timers"
        cursor = self.conn.execute(query)
        return cursor.fetchall()

    def delete_timer(self, timer_id):
        query = "DELETE FROM timers WHERE id = ?"
        self.conn.execute(query, (timer_id,))
        self.conn.commit()

    def update_timer(self, timer_id, work_time, break_time):
        query = "UPDATE timers SET work_time = ?, break_time = ? WHERE id = ?"
        self.conn.execute(query, (work_time, break_time, timer_id))
        self.conn.commit()

class TimerWindow(QDialog):
    def __init__(self, parent=None, timer_id=None, work_time=25, break_time=5):
        super().__init__(parent)
        self.setWindowTitle("Configurar Temporizador Pomodoro")
        self.setGeometry(100, 100, 300, 200)
        self.layout = QVBoxLayout()

        self.timer_id = timer_id
        self.work_time_label = QLabel("Tiempo de Trabajo (min):")
        self.layout.addWidget(self.work_time_label)
        self.work_time_input = QLineEdit(str(work_time))
        self.layout.addWidget(self.work_time_input)

        self.break_time_label = QLabel("Tiempo de Descanso (min):")
        self.layout.addWidget(self.break_time_label)
        self.break_time_input = QLineEdit(str(break_time))
        self.layout.addWidget(self.break_time_input)

        self.start_button = QPushButton("Iniciar")
        self.start_button.clicked.connect(self.start_timer)
        self.layout.addWidget(self.start_button)

        self.pause_button = QPushButton("Pausar")
        self.pause_button.clicked.connect(self.pause_timer)
        self.layout.addWidget(self.pause_button)

        self.stop_button = QPushButton("Detener")
        self.stop_button.clicked.connect(self.stop_timer)
        self.layout.addWidget(self.stop_button)

        self.save_button = QPushButton("Guardar")
        self.save_button.clicked.connect(self.save_timer)
        self.layout.addWidget(self.save_button)

        self.exit_button = QPushButton("Salir")
        self.exit_button.clicked.connect(self.close)
        self.layout.addWidget(self.exit_button)

        self.timer_label = QLabel("00:00", self)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.timer_label)

        self.setLayout(self.layout)
        self.is_paused = False
        self.is_stopped = False
        self.is_work_time = True  # Para rastrear si es tiempo de trabajo o de descanso
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.current_seconds = 0

    def start_timer(self):
        try:
            work_time = int(self.work_time_input.text())
            break_time = int(self.break_time_input.text())
            if work_time > 60 or break_time > 30:
                raise ValueError
            self.is_paused = False
            self.is_stopped = False
            self.is_work_time = True
            self.current_seconds = work_time * 60
            self.update_timer_label()
            self.timer.start(1000)
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor, ingrese tiempos válidos (Trabajo: máx 60 min, Descanso: máx 30 min).")

    def update_timer(self):
        if not self.is_paused and not self.is_stopped:
            if self.current_seconds > 0:
                self.current_seconds -= 1
                self.update_timer_label()
            else:
                self.timer.stop()
                mixer.init()
                mixer.music.load("Sound.mp3")
                mixer.music.play()
                if self.is_work_time:
                    QMessageBox.information(self, "Alerta", "Tiempo de trabajo cumplido")
                    self.is_work_time = False
                    self.current_seconds = int(self.break_time_input.text()) * 60
                else:
                    QMessageBox.information(self, "Alerta", "Tiempo de descanso cumplido")
                    self.is_work_time = True
                    self.current_seconds = int(self.work_time_input.text()) * 60
                mixer.music.stop()
                self.update_timer_label()
                self.timer.start(1000)

    def update_timer_label(self):
        mins, secs = divmod(self.current_seconds, 60)
        self.timer_label.setText(f"{mins:02}:{secs:02}")

    def pause_timer(self):
        self.is_paused = True

    def stop_timer(self):
        self.is_stopped = True
        self.timer.stop()
        self.update_timer_label()

    def save_timer(self):
        work_time = int(self.work_time_input.text())
        break_time = int(self.break_time_input.text())
        if self.timer_id:
            self.parent().db.update_timer(self.timer_id, work_time, break_time)
        else:
            self.parent().db.add_timer(work_time, break_time)
        self.parent().load_timers()
        self.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Temporizador Pomodoro")
        self.setGeometry(100, 100, 600, 400)
        self.db = Database()

        self.layout = QVBoxLayout()

        self.create_timer_button = QPushButton("Crear Temporizador Pomodoro")
        self.create_timer_button.clicked.connect(self.open_create_timer_window)
        self.layout.addWidget(self.create_timer_button)

        self.timer_table = QTableWidget()
        self.timer_table.setColumnCount(5)
        self.timer_table.setHorizontalHeaderLabels(["ID", "Trabajo (min)", "Descanso (min)", "Editar", "Eliminar"])
        self.layout.addWidget(self.timer_table)

        self.load_timers()

        self.exit_button = QPushButton("Salir")
        self.exit_button.clicked.connect(self.close)
        self.layout.addWidget(self.exit_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def load_timers(self):
        self.timer_table.setRowCount(0)
        timers = self.db.get_timers()
        for timer in timers:
            row_position = self.timer_table.rowCount()
            self.timer_table.insertRow(row_position)
            self.timer_table.setItem(row_position, 0, QTableWidgetItem(str(timer[0])))
            self.timer_table.setItem(row_position, 1, QTableWidgetItem(str(timer[1])))
            self.timer_table.setItem(row_position, 2, QTableWidgetItem(str(timer[2])))

            edit_button = QPushButton("Editar")
            edit_button.clicked.connect(lambda ch, timer_id=timer[0]: self.open_edit_timer_window(timer_id))
            self.timer_table.setCellWidget(row_position, 3, edit_button)

            delete_button = QPushButton("Eliminar")
            delete_button.clicked.connect(lambda ch, timer_id=timer[0]: self.confirm_delete_timer(timer_id))
            self.timer_table.setCellWidget(row_position, 4, delete_button)

    def open_create_timer_window(self):
        self.timer_window = TimerWindow(self)
        self.timer_window.show()

    def open_edit_timer_window(self, timer_id):
        timer = self.db.get_timers()
        for t in timer:
            if t[0] == timer_id:
                self.timer_window = TimerWindow(self, timer_id, t[1], t[2])
                self.timer_window.show()
                break

    def confirm_delete_timer(self, timer_id):
        reply = QMessageBox.question(self, 'Confirmar Eliminación', '¿Estás seguro de que deseas eliminar este temporizador?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.db.delete_timer(timer_id)
            self.load_timers()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
