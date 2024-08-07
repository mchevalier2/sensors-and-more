from __future__ import annotations

import datetime

import pendulum

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

main_dir = '/Users/palaeosaurus/Data-Projects/2024/sensors-and-more/'

with DAG(
    dag_id="sensors_and_more",
    schedule="30 * * * *",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
    tags=["example", "example2"],
    params={"example_key": "example_value"},
) as dag:

    pull_daily_data = BashOperator(
        task_id='pull_daily_data',
        bash_command=f"source {main_dir}venv/bin/activate && python {main_dir}download_data_from_client.py 2024-08-07 ",
    )

    merging_datasets = BashOperator(
        task_id = 'bash-commands-to-merge-datasets',
        bash_command = f'tail -n +2 {main_dir}data/latest_dat.csv > {main_dir}data/tmp.csv'+\
                       f' && cat {main_dir}data/dat.csv {main_dir}data/tmp.csv > {main_dir}data/new_dat.csv '+ \
                       f' && mv {main_dir}data/new_dat.csv {main_dir}data/dat.csv'+\
                       f' && rm {main_dir}data/tmp.csv {main_dir}data/latest_dat.csv',
    )
    pull_daily_data >> merging_datasets

    process_data = BashOperator(
        task_id='process_data',
        bash_command=f"source {main_dir}venv/bin/activate && python {main_dir}process_data.py",
    )
    merging_datasets >> process_data


if __name__ == "__main__":
    dag.test()
