""" In this script, I extract and save sensor data from the API. """

import os
import sys
import time
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import requests

from src_data_client.__init__ import create_app as create_store

os.chdir(__file__.split("download_data_from_client.py", maxsplit=1)[0])


def hourly_it(start: datetime, finish: datetime) -> None:
    """an iterator function to make an hourly loop between two dates"""
    while finish > start:
        start = start + timedelta(hours=1)
        yield start


if __name__ == "__main__":
    if len(sys.argv) > 1:
        date = sys.argv[1].split(" ")[0]
        try:
            date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("Incorrect date format. Please use 'YYYY-MM-DD'.")
            sys.exit()
    else:
        print("You did not provide any date. Will use exec time as default")
        date = datetime.now()
        date = datetime(date.year, date.month, date.day)

    if not os.path.exists("./data/"):
        os.makedirs("./data")

    start_date = date
    finish_date = datetime.now() - timedelta(hours=1)
    sensor_data = []

    store_dict = create_store()

    for shop_name in store_dict.keys():
        for sensor_id in range(store_dict[shop_name].n_sensors):
            print(shop_name, sensor_id)
            for hour in hourly_it(start_date, finish_date):
                dict1 = {}
                dict1.update({"date": str(datetime.date(hour))})
                dict1.update({"hour": hour.hour})
                dict1.update({"shop": shop_name})
                dict1.update({"sensor_id": int(sensor_id)})

                URL = (
                    "http://127.0.0.1:8000/"
                    + f"?store_name={shop_name}"
                    + f"&year={hour.year}&month={hour.month}&day={hour.day}&hour={hour.hour}"
                    + f"&sensor_id={sensor_id}"
                )
                try:
                    response = requests.get(URL, timeout=60)
                except OSError:
                    print("Let's sleep on", URL)
                    passing = False
                    while not passing:
                        time.sleep(5)
                        try:
                            response = requests.get(URL, timeout=60)
                            passing = True
                        except OSError:
                            print("Let's keep sleeping on", URL)
                            passing = False

                if response.status_code == 200:
                    dict1.update({"count": response.text})
                    if int(response.text) >= 0:
                        dict1.update({"units": "visits"})
                    else:
                        dict1.update({"units": ""})
                else:
                    print(URL)
                    raise Exception(f"Non-success status code: {response.status_code}")

                if np.random.rand() < 0.01:
                    dict1.update(
                        {list(dict1)[np.random.randint(0, len(dict1) - 1)]: "NULL"}
                    )

                sensor_data.append(dict1)
    df = pd.DataFrame(sensor_data).reindex(
        columns=["date", "hour", "shop", "sensor_id", "count", "units"]
    )

    df.to_csv("./data/latest_dat.csv", sep=",", index=False, encoding="utf-8")
