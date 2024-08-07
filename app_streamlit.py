import os
from datetime import datetime as dt

import duckdb
import logging
import pandas as pd
import plotly.express as px
import streamlit as st


def load_daily_data():
    req = """
             SELECT *
             FROM read_parquet('./data/dat_sensors.parquet/*/*/*.parquet', hive_partitioning = true);
    """
    df_sensors = duckdb.query(req).df()

    req = """
             SELECT *
             FROM read_parquet('./data/dat_shops.parquet/*/*/*.parquet', hive_partitioning = true);
    """
    df_shops = duckdb.query(req).df()
    return df_shops, df_sensors


def load_hourly_data():
    req = """
             SELECT *
             FROM read_parquet('./data/dat_sensors_hours.parquet/*/*/*.parquet', hive_partitioning = true);
    """
    df_sensors = duckdb.query(req).df()

    req = """
             SELECT *
             FROM read_parquet('./data/dat_shops_hours.parquet/*/*/*.parquet', hive_partitioning = true);
    """
    df_shops = duckdb.query(req).df()
    return df_shops, df_sensors


def filter_day(df, cb):
    for i in range(7):
        if not cb[i]:
            df = df.drop(df[df.weekday == i].index)
    return df


def filter_dates(df, dates, resol):
    date_end = dt(dates[1].year, dates[1].month, dates[1].day, 23)
    if resol == "Hourly":
        df["date"] = df[["date", "hour"]].apply(str_as_date_hour, axis=1)
    elif resol == "Daily":
        df["date"] = df["date"].apply(str_as_date_day)
    df = df[
        (df["date"] >= pd.to_datetime(dates[0]))
        & (df["date"] <= pd.to_datetime(date_end))
    ]
    return df


def filter_hours(df, dates):
    df = df.query(f"hour >= {dates[0]}").query(f"hour <= {dates[1]}")
    return df


def str_as_date_day(s):
    return dt.strptime(s, "%Y-%m-%d")


def str_as_date_hour(s):
    return dt.strptime(s.iloc[0] + " " + str(int(s.iloc[1])), "%Y-%m-%d %H")


def create_slider_dates(dfplot):
    values = st.slider(
        "Select a range of dates",
        str_as_date_day(dfplot.date.min()),
        str_as_date_day(dfplot.date.max()),
        (str_as_date_day(dfplot.date.min()), str_as_date_day(dfplot.date.max())),
    )
    return values


def create_slider_openinghours(dfplot):
    values = st.slider(
        "Select a range of hours",
        0,
        23,
        (0, 23),
    )
    return values


logging.error("keyword")
logging.error(os.listdir())
if 'data' not in os.listdir():
    os.mkdir("data")

if "dat_sensors_hours.parquet" not in os.listdir('./data'):
    #os.mkdir("data")
    os.system("cp ./minidata/dat.csv ./data")
    os.system("python process_data.py")
    logging.error(__file__)
    logging.error(os.listdir('./data'))
    logging.error("keyword")


logging.error(os.listdir('./data'))

with st.sidebar:
    df_shops, df_sensors = load_daily_data()

    list_shops = (
        duckdb.query("SELECT DISTINCT shop FROM df_shops").df().sort_values("shop")
    )
    shop = st.selectbox(
        "Which shop would you like to access?",
        list_shops,
        index=None,
        placeholder="Select a shop...",
    )

    if shop:
        list_sensors = duckdb.query(
            f"SELECT DISTINCT sensor_id FROM df_sensors WHERE shop='{shop}' ORDER BY sensor_id"
        ).df()

        sensor = st.selectbox(
            "Which sensor would you like to access? If none are selected, will return the sum of all sensors.",
            list_sensors,
            index=None,
            placeholder="Select a sensor...",
        )
    else:
        sensor = st.selectbox(
            "Which sensor would you like to access? If none are selected, will return the sum of all sensors.",
            "",
            index=None,
            placeholder="Select a shop first...",
            disabled=True,
        )

    st.write("For which day(s) do you want to see data?")
    cb_days = [
        st.checkbox("Monday", value=True),
        st.checkbox("Tuesday", value=True),
        st.checkbox("Wednesday", value=True),
        st.checkbox("Thursday", value=True),
        st.checkbox("Friday", value=True),
        st.checkbox("Saturday", value=True),
        st.checkbox("Sunday", value=False),
    ]

    time_resol = st.selectbox(
        "Select the temporal resolution of the data.",
        ("Daily", "Hourly"),
        index=0,
    )

    if time_resol == "Daily":
        df_shops, df_sensors = load_daily_data()
    else:
        df_shops, df_sensors = load_hourly_data()


if sensor is not None or shop is not None:

    if sensor is not None:

        dfplot = df_sensors.query(f"shop=='{shop}'").query(f"sensor_id=={sensor}")
        values_dates = create_slider_dates(dfplot)
        dfplot = filter_day(dfplot, cb_days)
        dfplot = filter_dates(dfplot, values_dates, time_resol)
        if time_resol == "Hourly":
            values_hours = create_slider_openinghours(dfplot)
            dfplot = filter_hours(dfplot, values_hours)

        tab2, tab3 = st.tabs(["Graphes", "Table"])
        dfplot = dfplot.reset_index(drop=True)

        with tab2:
            st.line_chart(data=dfplot, x="date", y="count", color="#ffaa00")
            st.line_chart(data=dfplot, x="date", y="avg_count_4days", color="#001100")

        with tab3:
            st.write(dfplot)

    else:
        dfplot = df_shops.query(f"shop=='{shop}'")
        values_dates = create_slider_dates(dfplot)
        dfplot = filter_day(dfplot, cb_days)
        dfplot = filter_dates(dfplot, values_dates, time_resol)
        if time_resol == "Hourly":
            values_hours = create_slider_openinghours(dfplot)
            dfplot = filter_hours(dfplot, values_hours)

        tab2, tab3 = st.tabs(["Graphes", "Table"])
        dfplot = dfplot.reset_index(drop=True)

        with tab2:
            st.line_chart(data=dfplot, x="date", y="count", color="#ffaa00")
            st.line_chart(data=dfplot, x="date", y="avg_count_4days", color="#001100")

        with tab3:
            st.write(dfplot)
