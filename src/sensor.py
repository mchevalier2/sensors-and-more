import sys
from datetime import date, datetime
import numpy as np
import pandas as pd


class Sensor:
    """
    """
    def __init__(self, id: int, avg_visit: int = 1000, std_visit: int = 100, start_time: datetime = datetime.now()) -> None:
        """
        """
        self.id=id
        self.start_time=start_time
        self.avg_visit=avg_visit
        self.std_visit=std_visit
        #

    def get_visit_counts(self, dt: datetime = datetime.now()) -> int:
        """
        """
        # Setting the seed of the random data generator based on the provided
        # datetime multiply by the sensor ID to have unique numbers for each
        # sensor.
        np.random.seed(seed=dt.toordinal() * (self.id+1))
        print(dt)
        print(dt.weekday(), dt.hour)
        if dt.weekday() == 6:
            return 0
        if dt.hour < 8 or dt.hour >= 18:
            return 0

        visits = np.random.normal(self.avg_visit, self.std_visit)
        visits = np.random.normal(self.avg_visit, self.std_visit)
        return int(visits)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        year, month, day = [int(v) for v in sys.argv[1].split("-")]
    else:
        year, month, day = 2023, 10, 25
    queried_date = date(year, month, day)

    capteur = Sensor(0, 500, 150)
    print(capteur.get_visit_counts(dt=pd.Timestamp('2021-09-15 10:03:30')))
    print(capteur.get_visit_counts(dt=pd.Timestamp('2022-09-15 11:03:30')))
    print(capteur.get_visit_counts(dt=pd.Timestamp('2023-09-15 12:03:30')))
    print(capteur.get_visit_counts(dt=pd.Timestamp('2024-09-15 19:03:30')))
    print(capteur.get_visit_counts(dt=pd.Timestamp('2024-08-04 19:03:30')))
    print(capteur.get_visit_counts(dt=datetime.now()))
