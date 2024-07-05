import unittest


def set_alarm(alarm_data):
    required_keys = ["alarm_type", "label", "trigger_time", "repeat", "sound", "snooze", "notes"]

    for key in required_keys:
        if key not in alarm_data:
            raise ValueError(f"Missing required key: {key}")

    if not isinstance(alarm_data["notes"], str):
        raise TypeError("Notes must be a string")

    if not isinstance(alarm_data["trigger_time"], str) or not is_valid_time_format(alarm_data["trigger_time"]):
        raise ValueError("Invalid trigger time format")

    # Further processing and setting the alarm
    print("Alarm set successfully with data:", alarm_data)
    return True


def is_valid_time_format(time_str):
    try:
        hours, minutes, seconds = map(int, time_str.split(':'))
        return 0 <= hours < 24 and 0 <= minutes < 60 and 0 <= seconds < 60
    except ValueError:
        return False


class TestAlarmDataValidation(unittest.TestCase):

    def test_set_alarm_with_valid_data(self):
        valid_alarm_data = {
            "alarm_type": "timer",
            "label": "Wake Up",
            "trigger_time": "08:00:00",
            "repeat": "daily",
            "sound": "default",
            "snooze": True,
            "notes": "Important meeting today"
        }

        result = set_alarm(valid_alarm_data)
        self.assertTrue(result)

    def test_set_alarm_with_missing_required_data(self):
        invalid_alarm_data = {
            "label": "Wake Up",
            "trigger_time": "08:00:00",
            "repeat": "daily",
            "sound": "default",
            "snooze": True,
            "notes": "Important meeting today"
        }

        with self.assertRaises(ValueError):
            set_alarm(invalid_alarm_data)

    def test_set_alarm_with_invalid_data_types(self):
        invalid_alarm_data = {
            "alarm_type": "timer",
            "label": "Wake Up",
            "trigger_time": "08:00:00",
            "repeat": "daily",
            "sound": "default",
            "snooze": True,
            "notes": 123  # Invalid data type
        }

        with self.assertRaises(TypeError):
            set_alarm(invalid_alarm_data)

    def test_set_alarm_with_invalid_trigger_time(self):
        invalid_alarm_data = {
            "alarm_type": "timer",
            "label": "Wake Up",
            "trigger_time": "invalid_time",
            "repeat": "daily",
            "sound": "default",
            "snooze": True,
            "notes": "Important meeting today"
        }

        with self.assertRaises(ValueError):
            set_alarm(invalid_alarm_data)


if __name__ == '__main__':
    unittest.main()
