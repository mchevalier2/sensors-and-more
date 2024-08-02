import sys
from datetime import datetime

try:
    from src.sensor import Sensor
except ModuleNotFoundError:
    from sensor import Sensor


class Store:
    """ """

    def __init__(
        self, name: str, n_sensors: int = 1, start_time: datetime = datetime.now()
    ) -> None:
        """ """
        if n_sensors < 0:
            n_sensors = 0
        self.name = name
        self.n_sensors = n_sensors
        self.sensors = {}
        for i in range(n_sensors):
            self.sensors[i] = Sensor(
                i, 1000, 150, start_time=start_time, p_fail=0.05, p_anom=0.2
            )
        self.start_time = start_time
        #

    def __repr__(self):
        return f"The shop {self.name} has {self.n_sensors} sensors."

    def get_visits_store_sensors(self, dt: datetime):
        visits = 0
        for sensor_id in range(self.n_sensors):
            v = self.sensors[sensor_id].get_visit_counts(
                datetime(dt.year, dt.month, dt.day, dt.hour)
            )
            visits += v if v >= 0 else 0
        return visits

    def get_visits_store_day_sensor(self, sensor_id: int, dt: datetime):
        visits = 0
        for hour in range(24):
            v = self.sensors[sensor_id].get_visit_counts(
                datetime(dt.year, dt.month, dt.day, hour)
            )
            visits += v if v >= 0 else 0
        return visits

    def get_visits_day_store(self, dt: datetime):
        visits = 0
        for sensor_id in range(self.n_sensors):
            visits += self.get_visits_store_day_sensor(
                sensor_id, datetime(dt.year, dt.month, dt.day, dt.hour)
            )
        return visits


if __name__ == "__main__":
    store = Store("REWE", 8, start_time=datetime(2023, 8, 4, 8))
    print(store)

    print(store.get_visits_store_sensors(dt=datetime(2024, 1, 22, 9)))
    s = 0
    for i in range(store.n_sensors):
        v = store.sensors[i].get_visit_counts(datetime(2024, 1, 22, 9))
        s += v if v >= 0 else 0
        print(i, s, v)

    print(store.get_visits_store_day_sensor(0, dt=datetime(2024, 1, 22)))
    s = 0
    for i in range(24):
        v = store.sensors[0].get_visit_counts(datetime(2024, 1, 22, i))
        s += v if v >= 0 else 0
        print(i, s, v)

    print(store.get_visits_day_store(dt=datetime(2024, 1, 22, 8)))
    s = 0
    for i in range(store.n_sensors):
        v = store.get_visits_store_day_sensor(i, datetime(2024, 1, 22, 8))
        s += v if v >= 0 else 0
        print(i, s, v)
