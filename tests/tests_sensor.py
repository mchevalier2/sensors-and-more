import unittest
from datetime import datetime

from src_data_client.sensor import Sensor


class TestSensor(unittest.TestCase):

    def test_weekdays_open(self):
        for test_day in range(5, 10):
            with self.subTest(i=test_day):
                visit_sensor = Sensor(id=test_day)
                visit_count = visit_sensor.get_visit_counts(
                    datetime(2024, 8, test_day, 12, 0, 0)
                )
                self.assertFalse(visit_count == 0)

    def test_closed_sundays(self):
        visit_sensor = Sensor(id=0)
        visit_count = visit_sensor.get_visit_counts(datetime(2024, 8, 4, 12, 0, 0))
        self.assertEqual(visit_count, 0)

    def test_opening_hours(self):
        for test_hour in range(8, 18):
            with self.subTest(i=test_hour):
                visit_sensor = Sensor(id=test_hour)
                visit_count = visit_sensor.get_visit_counts(
                    datetime(2024, 8, 2, test_hour, 0, 0)
                )
                self.assertFalse(visit_count == 0)

    def test_closing_hours(self):
        for test_hour in [x % 24 for x in range(18, 32)]:
            with self.subTest(i=test_hour):
                visit_sensor = Sensor(id=test_hour)
                visit_count = visit_sensor.get_visit_counts(
                    datetime(2024, 8, 2, test_hour, 0, 0)
                )
                self.assertEqual(visit_count, 0)

    def test_anomalies(self):
        visit_sensor = Sensor(
            0,
            1000,
            150,
            init_time=datetime(2021, 9, 15, 10, 3, 30),
            p_fail=0.05,
            p_anom=0.2,
        )
        visit_count = visit_sensor.get_visit_counts(datetime(2024, 9, 9, 8, 0, 0))
        self.assertEqual(visit_count, 80)

    def test_failures(self):
        visit_sensor = Sensor(
            0,
            1000,
            150,
            init_time=datetime(2021, 9, 15, 10, 3, 30),
            p_fail=0.05,
            p_anom=0.2,
        )
        visit_count = visit_sensor.get_visit_counts(datetime(2024, 8, 14, 19, 0, 0))
        self.assertEqual(visit_count, -1)


if __name__ == "__main__":
    unittest.main()
