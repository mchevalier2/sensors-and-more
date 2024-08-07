from datetime import datetime

try:
    from src_data_client.store import Store
except ModuleNotFoundError:
    from store import Store


def create_app() -> dict:
    """ """

    store_name = ["Madrid", "Paris", "Berlin", "Roma", "London"]
    store_n_sensors = [1, 20, 6, 4, 8]
    store_year_start = [2024, 2018, 2022, 2019, 2014]

    store_dict = dict()

    for i in range(len(store_name)):
        store_dict[store_name[i]] = Store(
            name=store_name[i],
            n_sensors=store_n_sensors[i],
            opening_date=datetime(store_year_start[i], 1, 1, 0),
            capacity=[(2024 - store_year_start[i] + 1) * x for x in [1000 , 150]],
            probs=[(2024 - store_year_start[i] + 1) * x for x in [0.01, 0.001]],
        )
    return store_dict


if __name__ == "__main__":
    store_dict = create_app()
    # print(store_dict)
