""" In this module, I create the Store() class. """

from datetime import datetime

try:
    from src_data_client.sensor import Sensor
except ModuleNotFoundError:
    from sensor import Sensor


class Store:
    """
    Initiate a Store(). A store has
        - A name (str)
        - A number of sensors (int)
        - An opening date (datetime)

        From these parameters, n_sensors are created within the store.
    """

    def __init__(
        self, name: str, n_sensors: int = 1, opening_date: datetime = datetime.now()
    ) -> None:
        # If the number provided is negative
        # n_sensors = max(n_sensors, 0)
        self.name = name
        self.n_sensors = n_sensors
        self.sensors = {}
        for i in range(n_sensors):
            self.sensors[i] = Sensor(
                i, 1000, 150, init_time=opening_date, p_fail=0.05, p_anom=0.2
            )
        self.opening_date = opening_date
        #

    def __repr__(self):
        """
        A simple function to print() a sensor.
        """
        return f"The shop {self.name} has {self.n_sensors} sensors."

    def get_visits_store_sensors(self, dt: datetime):
        """
        A method to get the sum of visits across all sensors at a given time.
        """
        visits = 0
        for sensor_id in range(self.n_sensors):
            v = self.sensors[sensor_id].get_visit_counts(
                datetime(dt.year, dt.month, dt.day, dt.hour)
            )
            visits += v if v >= 0 else 0
        return visits

    def get_visits_store_day_sensor(self, sensor_id: int, dt: datetime):
        """
        A method to get the sum of visits for a specific sensor on a given day.
        """
        visits = 0
        for hour in range(24):
            v = self.sensors[sensor_id].get_visit_counts(
                datetime(dt.year, dt.month, dt.day, hour)
            )
            visits += v if v >= 0 else 0
        return visits

    def get_visits_day_store(self, dt: datetime):
        """
        A method to get the sum of visits across all sensors on a given day.
        """
        visits = 0
        for sensor_id in range(self.n_sensors):
            visits += self.get_visits_store_day_sensor(
                sensor_id, datetime(dt.year, dt.month, dt.day, dt.hour)
            )
        return visits


if __name__ == "__main__":
    store = Store("REWE", 8, opening_date=datetime(2023, 8, 4, 8))
    print(store)

    print(store.get_visits_store_sensors(dt=datetime(2024, 1, 22, 9)))
    s = 0
    for ii in range(store.n_sensors):
        val = store.sensors[ii].get_visit_counts(datetime(2024, 1, 22, 9))
        s += val if val >= 0 else 0
        print(ii, s, val)

    print(store.get_visits_store_day_sensor(0, dt=datetime(2024, 1, 22)))
    s = 0
    for ii in range(24):
        val = store.sensors[0].get_visit_counts(datetime(2024, 1, 22, ii))
        s += val if val >= 0 else 0
        print(ii, s, val)

    print(store.get_visits_day_store(dt=datetime(2024, 1, 22, 8)))
    s = 0
    for ii in range(store.n_sensors):
        val = store.get_visits_store_day_sensor(ii, datetime(2024, 1, 22, 8))
        s += val if val >= 0 else 0
        print(ii, s, val)
