import unittest
from unittest.mock import patch

from Principal.PrincCode import MainWindow  # Replace with the actual path to your MainWindow class


class TestMainWindow(unittest.TestCase):

    @patch('PyQt5.QtCore.QProcess.startDetached')
    def test_open_timer(self, mock_start_detached):
        # Create an instance of MainWindow
        main_window = MainWindow()

        # Simulate clicking the timer button
        main_window.open_timer()

        # Assert that QProcess.startDetached was called with the expected arguments
        script_path = os.path.join(os.path.dirname(main_window.__file__), 'TempoCode.py')
        expected_call = mock_start_detached.call_args[0]
        self.assertEqual(expected_call[0], sys.executable)
        self.assertEqual(expected_call[1], [script_path])

    @patch('PyQt5.QtCore.QProcess.startDetached')
    def test_open_alarm(self, mock_start_detached):
        # Similar approach as test_open_timer, but for the alarm button
        main_window = MainWindow()
        main_window.open_alarm()

        script_path = os.path.join(os.path.dirname(main_window.__file__), 'AlarmCode.py')
        expected_call = mock_start_detached.call_args[0]
        self.assertEqual(expected_call[0], sys.executable)
        self.assertEqual(expected_call[1], [script_path])

    @patch('PyQt5.QtCore.QProcess.startDetached')
    def test_open_pomodoro(self, mock_start_detached):
        # Similar approach as test_open_timer, but for the pomodoro button
        main_window = MainWindow()
        main_window.open_pomodoro()

        script_path = os.path.join(os.path.dirname(main_window.__file__), 'PomodoroCode.py')
        expected_call = mock_start_detached.call_args[0]
        self.assertEqual(expected_call[0], sys.executable)
        self.assertEqual(expected_call[1], [script_path])


if __name__ == '__main__':
    unittest.main()
