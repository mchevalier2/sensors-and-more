""" Creation of the data necessary for the API. """

from datetime import datetime

try:
    from src_data_client.store import Store
except ModuleNotFoundError:
    from store import Store


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


if __name__ == "__main__":
    stores = create_app()
    # print(store_dict)
