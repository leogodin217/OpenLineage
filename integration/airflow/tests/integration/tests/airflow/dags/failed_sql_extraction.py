# Copyright 2018-2025 contributors to the OpenLineage project
# SPDX-License-Identifier: Apache-2.0
from openlineage.client import set_producer_v2 as set_producer
from packaging.version import Version

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago
from airflow.version import version as AIRFLOW_VERSION

set_producer("https://github.com/OpenLineage/OpenLineage/tree/0.0.1/integration/airflow")


default_args = {
    "owner": "datascience",
    "depends_on_past": False,
    "start_date": days_ago(7),
    "email_on_failure": False,
    "email_on_retry": False,
    "email": ["datascience@example.com"],
}


dag = DAG(
    "failed_sql_extraction",
    schedule_interval="@once",
    default_args=default_args,
    description="Determines the popular day of week orders are placed.",
)


# Some sql-parser unsupported syntax
sql = "DROP POLICY IF EXISTS name ON table_name"


if Version(AIRFLOW_VERSION) < Version("2.5.0"):
    t1 = PostgresOperator(task_id="fail", postgres_conn_id="food_delivery_db", sql=sql, dag=dag)
else:
    from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

    t1 = SQLExecuteQueryOperator(task_id="fail", conn_id="food_delivery_db", sql=sql, dag=dag)
