import sys
from datetime import datetime

import numpy as np
import pandas as pd


class Sensor:
    """ """

    def __init__(
        self,
        id: int,
        avg_visit: int = 1000,
        std_visit: int = 100,
        start_time: datetime = datetime.now(),
        p_fail: float = 0.01,
        p_anom: float = 0.05,
    ) -> None:
        """ """
        self.id = id
        self.start_time = start_time
        self.avg_visit = avg_visit
        self.std_visit = std_visit
        self.p_fail = p_fail
        self.p_anom = p_anom
        #

    def get_visit_counts(self, dt: datetime = datetime.now()) -> int:
        """ """
        # Setting the seed of the random data generator based on the provided
        # datetime multiply by the sensor ID to have unique numbers for each
        # sensor.

        np.random.seed(
            seed=self.start_time.toordinal() + dt.toordinal() + dt.hour + self.id
        )

        if np.random.random() > self.p_fail:
            if dt.weekday() == 6:
                return 0
            if dt.hour < 8 or dt.hour >= 18:
                return 0

            visits = np.random.normal(self.avg_visit, self.std_visit)
            visits = np.random.normal(self.avg_visit, self.std_visit)
            if np.random.random() < self.p_anom:
                visits = visits * 0.1
            return int(visits)
        else:
            return -1

    def __repr__(self, n: int = 1):
        """ """
        return f"This is sensor {self.id}. In the last {n} hour(s), I recorded {self.get_visit_counts()} entries."


if __name__ == "__main__":
    if len(sys.argv) > 1:
        year, month, day = [int(v) for v in sys.argv[1].split("-")]
    else:
        year, month, day = 2023, 10, 25
    queried_date = datetime(year, month, day)

    capteur = Sensor(0, 500, 150, start_time=queried_date)
    print(capteur)
    print(capteur.get_visit_counts(dt=pd.Timestamp("2021-09-15 10:03:30")))
    print(capteur.get_visit_counts(dt=pd.Timestamp("2021-09-15 11:03:30")))
    print(capteur.get_visit_counts(dt=pd.Timestamp("2022-09-15 11:03:30")))
    print(capteur.get_visit_counts(dt=pd.Timestamp("2023-09-15 12:03:30")))
    print(capteur.get_visit_counts(dt=pd.Timestamp("2024-09-15 19:03:30")))
    print(capteur.get_visit_counts(dt=pd.Timestamp("2024-08-04 19:03:30")))
    print(capteur.get_visit_counts(dt=datetime.now()))

    visit_sensor = Sensor(
        0,
        1000,
        150,
        start_time=pd.Timestamp("2021-09-15 10:03:30"),
        p_fail=0.05,
        p_anom=0.2,
    )
    for test in range(100):
        dt = datetime(2024, test % 12 + 1, test % 30 + 1, test % 24, 0, 0)
        score = visit_sensor.get_visit_counts(dt)
        if score == -1:
            print(dt, score)
        if score < 100 and score > 0:
            print(dt, score)
