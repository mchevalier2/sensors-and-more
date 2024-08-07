import unittest
from datetime import datetime

from src_data_client.store import Store


class TestStore(unittest.TestCase):

    def test_visits_store_sensors(self):
        store = Store("REWE", 8, opening_date=datetime(2023, 8, 4, 8))
        visit_count = store.get_visits_store_sensors(dt=datetime(2024, 1, 22, 9))
        self.assertEqual(visit_count, 4632)

    def test_visits_store_day_sensor(self):
        store = Store("REWE", 8, opening_date=datetime(2023, 8, 4, 8))
        visit_count = store.get_visits_store_day_sensor(0, dt=datetime(2024, 1, 22))
        self.assertEqual(visit_count, 5878)

    def test_visits_store_day(self):
        store = Store("REWE", 8, opening_date=datetime(2023, 8, 4, 8))
        visit_count = store.get_visits_day_store(dt=datetime(2024, 1, 22))
        self.assertEqual(visit_count, 51946)


if __name__ == "__main__":
    unittest.main()
