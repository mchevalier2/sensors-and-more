""" In this script, I process the data. """

import os
import sys
from datetime import datetime, timedelta

import duckdb
import pandas as pd
import shutils


if 'app_streamlit' in __file:
    os.chdir(__file__.split('app_streamlit.py')[0])
else:
    os.chdir(__file__.split('process_data.py')[0])

try:
    os.system("rm -Rf ./data/dat_sensors_hours.parquet")
    os.system("rm -Rf ./data/dat_sensors.parquet")
    os.system("rm -Rf ./data/dat_shops.parquet")
    os.system("rm -Rf ./data/dat_shops_hours.parquet")
except:
    print("Nothing to delete.")


def get_status(x):
    if x == -1:
        return "Measurement failed"
    if x == -2:
        return "Shop closed"
    return "OK"


if True:
    print(">>>>> Prepping data")
    df_hourly = pd.read_csv("./data/dat.csv").drop_duplicates()
    df_hourly = df_hourly.dropna(subset=["date", "hour", "shop", "sensor_id", "count"])
    df_hourly.insert(
        6, "weekday", [pd.Timestamp(x).weekday() for x in df_hourly["date"]]
    )
    df_hourly.insert(7, "status", [get_status(x) for x in df_hourly["count"]])
    df_hourly.loc[df_hourly["status"] != "OK", "count"] = 0
    print(df_hourly.query("status != 'OK'"))
    print(df_hourly["status"].value_counts())
    ## Daily trafic per sensor
    req = """
             SELECT shop, date, weekday, sensor_id, sum(count) AS count
             FROM df_hourly
             GROUP BY shop, date, weekday, sensor_id
             ORDER BY shop, date, sensor_id
          """
    df_daily = duckdb.query(req).df()
    print(df_daily.head(10))
    ## Daily trafic per store_dict
    req = """
             SELECT shop, date, weekday, sum(count) AS count
             FROM df_hourly
             GROUP BY shop, date, weekday
             ORDER BY shop, date
          """
    df_shop = duckdb.query(req).df()
    print(df_shop.head(10))
    print("<<<<< Prepping data\n\n\n\n")


if True:
    print(">>>>> Creating data per shop, per sensor, per hour")
    req = """
             WITH df3 AS (
                 SELECT shop, date, weekday, hour, sensor_id, count, status,
                        AVG(count) OVER(
                                PARTITION BY shop, weekday, hour, sensor_id
                                ORDER BY date
                                ROWS between 3 PRECEDING AND CURRENT ROW
                                ) AS avg_count_4days
                 FROM df_hourly
                 ORDER BY shop, date, hour, sensor_id
             )

             SELECT *,
                100 * (count-avg_count_4days)/avg_count_4days AS perc_diff
             FROM df3
             ORDER BY shop, date, hour, sensor_id
          """

    df2 = duckdb.query(req).df()
    print(df2.query("hour==9").query("sensor_id==1").query("weekday==0").head(10))
    df2.to_csv("./data/dat_sensors_hours.csv")
    df2.to_parquet(
        path="./data/dat_sensors_hours.parquet",
        engine="fastparquet",
        compression=None,
        index=None,
        partition_cols=["shop", "weekday"],
    )
    print("Files saved as dat_sensors_hours (.csv, .parquet)")
    print("<<<<< Creating data per shop, per sensor, per hour\n\n\n\n")


if True:
    print(">>>>> Creating data per shop, per sensor, per day")
    req = """
             WITH df3 AS (
                 SELECT shop, date, weekday, sensor_id, count,
                        AVG(count) OVER(
                                PARTITION BY shop, weekday, sensor_id
                                ORDER BY date
                                ROWS between 3 PRECEDING AND CURRENT ROW
                                ) AS avg_count_4days
                 FROM df_daily
                 ORDER BY shop, date, sensor_id
             )

             SELECT *,
                100 * (count-avg_count_4days)/avg_count_4days AS perc_diff
             FROM df3
             ORDER BY shop, date, sensor_id
          """
    df2 = duckdb.query(req).df()
    print(df2.query("weekday==0").head(30))
    df2.to_csv("./data/dat_sensors.csv")
    df2.to_parquet(
        path="./data/dat_sensors.parquet",
        engine="fastparquet",
        compression=None,
        index=None,
        partition_cols=["shop", "weekday"],
    )
    print("Files saved as dat_sensors (.csv, .parquet)")
    print("<<<<< Creating data per shop, per sensor, per day\n\n\n\n")


if True:
    print(">>>>> Creating data per shop, per day")
    req = """
             WITH df3 AS (
                 SELECT shop, date, weekday, count,
                        AVG(count) OVER(
                                PARTITION BY shop, weekday
                                ORDER BY date
                                ROWS between 3 PRECEDING AND CURRENT ROW
                                ) AS avg_count_4days
                 FROM df_shop
                 ORDER BY shop, date
             )

             SELECT *,
                100 * (count-avg_count_4days)/avg_count_4days AS perc_diff
             FROM df3
             ORDER BY shop, date
          """
    df2 = duckdb.query(req).df()
    print(df2.head(30))
    df2.to_csv("./data/dat_shops.csv")
    df2.to_parquet(
        path="./data/dat_shops.parquet",
        engine="fastparquet",
        compression=None,
        index=None,
        partition_cols=["shop", "weekday"],
    )
    print("Files saved as dat_shops (.csv, .parquet)")
    print("<<<<< Creating data per shop, per day\n\n\n\n")


if True:
    print(">>>>> Creating data per shop, per hour")
    req = """
             WITH df4 AS (
                 SELECT shop, date, weekday, hour, sum(count) AS count
                 FROM df_hourly
                 GROUP by shop, date, weekday, hour
             ),

             df3 AS (
                 SELECT shop, date, weekday, hour, count,
                        AVG(count) OVER(
                                PARTITION BY shop, weekday, hour
                                ORDER BY date
                                ROWS between 3 PRECEDING AND CURRENT ROW
                                ) AS avg_count_4days
                 FROM df4
                 ORDER BY shop, date, hour
             )


             SELECT *,
                100 * (count-avg_count_4days)/avg_count_4days AS perc_diff
             FROM df3
             ORDER BY shop, date, hour
          """
    df2 = duckdb.query(req).df()
    print(df2.query("weekday==0").query("hour==9").head(30))
    df2.to_csv("./data/dat_shops_hours.csv")
    df2.to_parquet(
        path="./data/dat_shops_hours.parquet",
        engine="fastparquet",
        compression=None,
        index=None,
        partition_cols=["shop", "weekday"],
    )
    print("Files saved as dat_shops_hours (.csv, .parquet)")
