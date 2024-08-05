""" In this script, I process the data. """

import os
import sys
from datetime import datetime, timedelta

import pandas as pd
import duckdb


df = pd.read_csv("./data/dat_big.csv").dropna()
df.insert(6, "weekday", [pd.Timestamp(x).weekday() for x in df["date"]])
print(df)
print(df.weekday.mean())


## Daily trafic per sensor
req = """
         SELECT date, weekday, shop, sensor_id, sum(count) AS daily_count
         FROM df
         GROUP BY date, weekday, shop, sensor_id
         ORDER BY date, shop, sensor_id
      """

df2 = duckdb.query(req).df()
print(df2)

## Daily trafic per store
req = """
         SELECT date, weekday, shop, sum(count) AS daily_count
         FROM df
         GROUP BY date, weekday, shop
         ORDER BY shop, date
      """

print(duckdb.query(req).df())


print(df2.query("weekday == 1"))


## Average the last 4 same days


req = """
         SELECT date, weekday, shop, sensor_id, daily_count,
                AVG(daily_count) OVER(
                        PARTITION BY shop, weekday, sensor_id
                        ORDER BY date
                        ROWS between 3 PRECEDING AND CURRENT ROW
                        ) AS avg_counts_4days
         FROM df2
         ORDER BY shop, sensor_id, date
      """

print(duckdb.query(req).df())
print(duckdb.query(req).df().query("weekday == 6"))


## Percentage difference between each line and the 4 similar day average

req = """
         WITH df3 AS (
             SELECT date, weekday, shop, sensor_id, daily_count,
                    AVG(daily_count) OVER(
                            PARTITION BY shop, weekday, sensor_id
                            ORDER BY date
                            ROWS between 3 PRECEDING AND CURRENT ROW
                            ) AS avg_counts_4days
             FROM df2
             ORDER BY shop, sensor_id, date
         )

         SELECT *,
            100 * (daily_count-avg_counts_4days)/avg_counts_4days AS perc_diff
         FROM df3
         ORDER BY shop, sensor_id, date

      """
df3 = duckdb.query(req).df()
print(df3.query("weekday==1"))

df3.to_parquet(
    path="./data/dat6.parquet",
    engine="pyarrow",
    compression=None,
    index=None,
    partition_cols=["shop", "weekday"],
)


"""
df3.to_parquet(
    path='./data/dat2.parquet',
    engine='pyarrow',
    compression=None,
    partition_cols=['shop', 'weekday'],
    index=False
)
"""
