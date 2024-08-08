# sensors-and-more

## Context

This data analysis and visualition project was triggered by a [data-upskilling](https://benjamin-dubreu.systeme.io/programme-data-upskilling) training course I recently followed to acquaint myself with tools commonly used by data scientists. This project combines all the different concepts I learned in the class. The work was divided in four distinct yet integrated objectives:

1. Creating an API that generates data(*).
2. Querying that interface to extract the data required by the project.
3. Processing the data to address the client's needs.
4. Visualising the data in an online dynamic environment.

(*) In a real life situation, this step would be skipped as the client would provide the data.

**Skills involved**: `Python`, `SQL`, `Bash`, `Git`, `Airflow`, `Object-oriented programming`, `Unit testing`, `API development`, `Data extraction`, `Data analysis`, `Data visualisation`, `streamlit cloud`

**Languages and packages used**: `fastapi`, `pandas`, `datetime`, `numpy.random`, `unittest`, `uvicorn`, `requests`, `duckdb`, `streamlit`, `venv`, `black`, `isort`, `pylint`



## How to use

To safely use the different scripts available in this repo, you'll need to type the following commands:

```
    cd /path/to/folder
    git clone https://github.com/mchevalier2/sensors-and-more.git
    cd sensors-and-more
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

    ## <your-time-to-shine>
```

**Note**: The use of `venv` (i.e. _virtual environments_) is key to guarantee that this program does not interfere with your local system. Everything you install and delete from a venv does not impact your machine.



## The project: What the client wants

The client owns several stores in major European cities that she opened over the last decade. She wants to know how many people frequent the different stores to detect long-term trends. The data available are sensor data that count how many people enter a store per hour. A store can have several doors, and thefore, several streams of sensor data. With her initial request, [the client wants an interface where she can easily navigate between sensor data from the different stores](https://sensors-and-more.streamlit.app). In particular, she wants to see the data at four different temporal and organisational resolutions:

- Hourly data at the sensor level.
- Daily data at the sensor level.
- Hourly data at the store level.
- Daily data at the store level.


**Note**: This project is primarily about showcasing a robust infrasture and data processing pipeline, and not so much about the randomly-generated sensor data illustrated in the final app.



## The pipeline

![The data analysis pipeline of this project](jungle/pipeline_diagram.png?raw=true "The data analysis pipeline of this project")


### Creating the data

_This part involved using `python`, `bash`, `git`, `venv`, `pandas`, `datetime`, `numpy`, `unittest`, `black`, `isort`, `pylint`, and `Object oriented programming`._

In this dummy project, I need to create the data stream source. To do so, I created two Python classes, one for sensor data and a second for stores. Stores contain sensors.

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
A sensor generates a randomised number of visits per hour based on several parameters. Since stores are only opened between 8am and 6pm, sensors return 0 visits outside opening hours. In between, a number of visits is drawn from a normal distribution that is constant throughout the day. Sensors are imperfect and can fail with a predefined probability. Anomalous values, defined as 10% of the 'expected' traffic, are also randomly generated to reflect the impact of external events on store visits. The seed of the random generator is defined as a combination of the `init_time` (i.e. when the sensor was first used), the sensor `id` and the queried date and time to ensure that every sensor records a unique traffic time series but that this traffic is reproducible across runs.

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
In practice, a store is a bundle of sensors. All sensors within a store are assumed to be identical, i.e. they have the same rate of failure and they record the same traffic on average (i.e. all the doors are used homogeneously).


Our client opened five of these stores in western European capitals. Each store has a different size, reflected by the number of entry points / sensors. The opening date of the store is assumed 1) to positively impact the capacity of the store (how many people visit the store), and 2) to increase the risks of failed detections. A more refined model would be to automatically adjust the probability of failure to the age of the sensor as a proxy of the need of replacement. This feature may be added in future development.

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

The client's data can be accessed remotely with an API.



### Accessing the data remotely

_This part involved using `python`, `API development`, `Data extraction`, `bash`, `git`, `pandas`, `datetime`, `fastapi`, `black`, `isort`, and `pylint`._


To simulate how real-time data could be accessed from our client, I created the API available in this repo. This API is run locally and generates and accesses the sensor data. It can be started as follow:
```
    uvicorn app:app --reload
```

Once active, the API can be directly queried from a web browser with requests such as the following:
```
    http://localhost:8000/?store_name=Paris&year=2022&month=7&day=30&hour=12&sensor_id=12
```
This request will return a single integer representing the traffic in the Parisian store on July 30th 2022 between noon and 1PM (hour=12) from door number 12.

However, I need to collect data from every sensor of every store over a long period of time to meet the objective of the project. To do so, I developed a python script `download_data_from_client.py` to pull the data from the API. This script takes a date as argument to indicate the period the data must cover. Hourly data will be pulled from every sensor of every store between that date and the time at which the script was executed. The data will be exported as a CSV file. If no date is provided, the script will extract data for the last hour only.

```
    python download_data_from_client.py YYYY-MM-DD
```



### Processing the data

_This part involved using `SQL`, `python`, `git`, `duckdb`, `pandas`, `datetime`, `black`, `isort`, and `pylint`._







### Analysing and visualising

<!---
_This part involved using `python`, `bash`, `git`, `venv`, `pandas`, `datetime`, `numpy`, `unittest`, and `Object oriented programming`._
-->


Because the API is not live online (yet!), the [streamlit cloud app](https://sensors-and-more.streamlit.app) is built with data collected between July 1st to August 7th 2024. These data are part of the GitHub repo and are saved in the streamlit_data folder. In a real-life situation, I would not include the data with the interface. If possible, I would try to access the data live, and if not possible, I would create a dataset that I would save on a cloud service to be dynamically downloaded on loading by the programme.


## Next steps

The project's data are built on simplistic assumptions that limit the type and diversity of analyses I can perform. However, the following items highlight how they could be complexified to produce more interesting analyses.

- Sensors of different age, with age that impacts the rate of failures. And at some point the sensor needs to be changed.
- Adding long-term trends to the data
- Account for the failed detection rates
- Send warning emails when issues are detected.
- API live online to directly query data.
