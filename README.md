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



## The general idea

The client owns several stores in major European cities that he/she opened in the last decade. The client needs to know how many people frequent the different stores and detect long-term trends. The data available are sensor data that count how many people enter a store per hour. A store can have several doors, and thefore, several streams of sensor data. With his/her initial request, the client wants an interface where he/she can easily navigate the sensor data from the different stores. In particular, he/she wants the data at four different resolutions:

- Hourly data at the sensor level.
- Hourly data at the store level.
- Daily data at the sensor level.
- Daily data at the store level.



**Note**: This project is primarily about showcasing my capacity at creating a robust infrasture and data processing pipeline, and not so much about the data illustrated in the final app.



## The details


### Creating the data


### Accessing the data remotely


### Processing the data


### Analysing and visualising


## Next steps
