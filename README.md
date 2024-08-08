# sensors-and-more

## Context

This data analysis and visualition project was triggered by a [data-upskilling](https://benjamin-dubreu.systeme.io/programme-data-upskilling) training course I recently followed to acquaint myself with tools commonly used by data scientists. With this project, I used and combined all the different concepts I learned in the class. The work was divided in four different routes:

1. Creating an API that generates data(*).
2. Querying that interface to extract the data required by the project.
3. Processing the data to address the client's needs.
4. Visualising the data in an online dynamic environment.

(*) In a real life situation, this step would be skipped as the client would provide the data.

**Skills involved**: Python, SQL, Bash, Git, Airflow, Object-oriented programming, Unit testing, API development, Data extraction, Data analysis, Data visualisation, streamlit cloud

**Languages and packages used**: fastapi, pandas, datetime, numpy.random, unittest, uvicorn, requests, duckdb, streamlit, venv



## The project: what the client needs

The client owns several stores in major European cities that he/she opened over the last decade. The client needs to know how many people frequent the different stores to detect long-term trends. The data available are sensor data that count how many people enter a store per hour. A store can have several doors, and thefore, several streams of sensor data. With his/her initial request, [the client wants an interface where he/she can easily navigate the sensor data from the different stores](https://sensors-and-more.streamlit.app). In particular, he/she asks to see the data at four different resolutions:

- Hourly data at the sensor level.
- Hourly data at the store level.
- Daily data at the sensor level.
- Daily data at the store level.


**Note**: This project is primarily about showcasing my capacity at creating a robust infrasture and data processing pipeline, and not so much about the data illustrated in the final app.



## The pipeline

![The data analysis pipeline of this project](jungle/pipeline_diagram.png?raw=true "The data analysis pipeline of this project")


### Creating the data

In this dummy project, I need to create the data source. To do so, I created two Python classes, one for sensor data and a second for stores. Stores contain sensors.

- The class `sensor`:
```
def __init__(
    self,
    id: int,
    avg_visit: int = 1000,
    std_visit: int = 100,
    init_time: datetime = datetime.now(),
    p_fail: float = 0.01,
    p_anom: float = 0.05,
) -> None:
```
A sensor generates a randomised number of visits based on several parameters. Since stores are only opened between 8am and 6pm, sensors return 0 visits outside opening hours. In between, a number of visits is drawn from a normal distribution that is constant throughout the day. Sensors are imperfect and can fail with a predefined probability. Anomalous values, defined as 10% of the 'expected' traffic, are also randomly generated to reflect that external events can impact store visits. The seed of the random generator is defined as a combination of the `init_time`, the sensor `id` and the date and time of the visit to ensure that no two sensors record the same traffic, but this traffic is constant across runs.

- The class `store`:
```
def __init__(
    self,
    name: str,
    n_sensors: int = 1,
    opening_date: datetime = datetime.now(),
    capacity: [] = [1000, 150],
    probs: [] = [0.2, 0.05],
) -> None:
```
A store is essentially a bundle of sensors. All sensors within a store are assumed to be identical, i.e. they have the same rate of failure and the same amount of people use every door on average (even if this is likely wrong).


Our client has five of these stores in western European capitals. Each store has a different size, reflected by the number of entry points / sensors. The opening date of the store is assumed to positively impact the capacity of the store (how many people visit the store) but also on the risks of failed detections. A more refined model would be to automatically adjust the probability of failure to the age of the sensor as a proxy of the need of replacement.

```
def create_app() -> dict:
    """Create the data for the API"""

    store_name = ["Madrid", "Paris", "Berlin", "Roma", "London"]
    store_n_sensors = [1, 20, 6, 4, 8]
    store_year_start = [2024, 2018, 2022, 2019, 2014]
    store_dict = {}

    for i, store in enumerate(store_name):
        store_dict[store] = Store(
            name=store,
            n_sensors=store_n_sensors[i],
            opening_date=datetime(store_year_start[i], 1, 1, 0),
            capacity=[(2024 - store_year_start[i] + 1) * x for x in [1000, 150]],
            probs=[(2024 - store_year_start[i] + 1) * x for x in [0.01, 0.001]],
        )
    return store_dict
```

Data can be generated and downloaded using the python script in this repo: ```python download_data_from_client.py YYYY-MM-DD```. If no date is provided, the script will extract data for the last hour. The [streamlit cloud app](https://sensors-and-more.streamlit.app) is built with data collected between July 1st to August 7th 2024.




### Accessing the data remotely


### Processing the data


### Analysing and visualising


## Next steps

The project's data are built on simplistic assumptions that limit the type and diversity of analyses I can perform. However, the following items highlight how they could be complexified to produce more interesting analyses.

- Sensors of different age
- Adding long-term trends to the data
- Account for the failed detection rates
- Send warning emails when issues are detected.
