""" My API to access to the store visit counts. """

from datetime import datetime
from typing import Optional

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src_data_client import create_app

store_dict = create_app()
app = FastAPI()


@app.get("/")
def visit(
    store_name: str,
    year: int,
    month: int,
    day: int,
    hour: int,
    sensor_id: Optional[int] = None,
) -> JSONResponse:
    """
        Dealing with all possible combinations of parameters.
        Returning the visit counts.
    """

    # If the store is not in the dictionary
    if not store_name in store_dict:
        s = f"Store '{store_name}' not found. It should one of the following " +\
            f"names: {", ".join(store_dict.keys())}."
        return JSONResponse(status_code=404, content=s)

    # Check the value of sensor_id
    if sensor_id and (sensor_id > store_dict[store_name].n_sensors or sensor_id < 0):
        return JSONResponse(
            status_code=404,
            content="Sensor_id for this shop should be between 0 and " +\
                    str(store_dict[store_name].n_sensors-1),
        )

    # Check the date
    try:
        datetime(year, month, day, hour)
    except TypeError:
        return JSONResponse(status_code=404, content="Enter a valid date")

    # Check the date is after the opening of the shop
    if datetime(year, month, day, hour) < store_dict[store_name].opening_date:
        return JSONResponse(
            status_code=404,
            content=f"No data before {store_dict[store_name].opening_date}",
        )

    # Check the date is in the past
    if datetime.now() < datetime(year, month, day, hour):
        return JSONResponse(status_code=404, content="Choose a date in the past")

    # If no sensor choose return the visit for the whole store
    if sensor_id is None:
        visit_counts = store_dict[store_name].get_visits_store_sensors(
            datetime(year, month, day, hour)
        )
    else:
        visit_counts = (
            store_dict[store_name]
            .sensors[sensor_id]
            .get_visit_counts(datetime(year, month, day, hour))
        )

    if visit_counts < 0:
        return JSONResponse(
            status_code=204, content="The sensor did not work on that date and time"
        )

    return JSONResponse(status_code=200, content=visit_counts)


"""
uvicorn app:app --reload
"""


"""
http://127.0.0.1:8000/?store_name=Paris&year=2022&month=7&day=30&hour=15
http://127.0.0.1:8000/?store_name=Paris&year=2022&month=7&day=30&hour=12&sensor_id=12


http://127.0.0.1:8000/?store_name=Toulouse&year=2022&month=7&day=30&hour=12&sensor_id=0
106
http://127.0.0.1:8000/?store_name=Toulouse&year=2022&month=7&day=30&hour=12&sensor_id=1
1080
http://127.0.0.1:8000/?store_name=Toulouse&year=2022&month=7&day=30&hour=12&sensor_id=2
-1
http://127.0.0.1:8000/?store_name=Toulouse&year=2022&month=7&day=30&hour=12&sensor_id=3
1117
http://127.0.0.1:8000/?store_name=Toulouse&year=2022&month=7&day=30&hour=12
2303

"""
