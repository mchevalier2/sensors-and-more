from datetime import datetime

try:
    from src_data_client.store import Store
except ModuleNotFoundError:
    from store import Store

def create_app() -> dict:
    """ """

    store_name = ["Lille", "Paris", "Lyon", "Toulouse", "Marseille"]
    store_n_sensors = [8, 20, 6, 4, 1]
    store_year_start = [2014, 2018, 2022, 2019, 2019]

    store_dict = dict()

    for i in range(len(store_name)):
        store_dict[store_name[i]] = Store(
            name=store_name[i],
            n_sensors=store_n_sensors[i],
            opening_date=datetime(store_year_start[i], 1, 1, 8),
        )
    return store_dict


if __name__ == "__main__":
    store_dict = create_app()
    #print(store_dict)
