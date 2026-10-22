from datetime import datetime

import pandas as pd
import sqlalchemy
from airflow.providers.google.cloud.operators.gcs import GCSListObjectsOperator
from airflow.providers.google.cloud.transfers.gcs_to_local import GCSToLocalFilesystemOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import DAG, BaseHook


def load_to_sql(file_path):
    conn = BaseHook.get_connection("postgres_default")
    url = sqlalchemy.engine.URL.create(
        drivername="postgresql+psycopg2",
        username=conn.login,
        password=conn.password,
        host=conn.host,
        port=conn.port,
        database=conn.schema,
    )
    engine = sqlalchemy.create_engine(url)
    df = pd.read_csv(file_path)
    df.to_sql(name="titanic", con=engine, if_exists="replace", index=False)


with DAG(
    dag_id="extract_titanic_data",
    schedule=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    list_files = GCSListObjectsOperator(
        task_id="list_files",
        bucket="my_bucket0101",
    )

    download_file = GCSToLocalFilesystemOperator(
        task_id="download_file",
        bucket="my_bucket0101",
        object_name="Titanic-Dataset.csv",
        filename="/tmp/Titanic-Dataset.csv",
    )

    load_data = PythonOperator(
        task_id="load_to_sql",
        python_callable=load_to_sql,
        op_kwargs={"file_path": "/tmp/Titanic-Dataset.csv"},
    )

    list_files >> download_file >> load_data
