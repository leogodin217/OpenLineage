# Copyright 2018-2025 contributors to the OpenLineage project
# SPDX-License-Identifier: Apache-2.0

import os
from typing import Any

from openlineage.client import set_producer

from airflow import DAG
from airflow.models import BaseOperator
from airflow.utils.dates import days_ago

set_producer("https://github.com/OpenLineage/OpenLineage/tree/0.0.1/integration/airflow")


# This is to test the thread handling in the Airflow listener.
# The thread should be shutdown after 2 seconds, even if the extractor is hanging
os.environ["OPENLINEAGE_EXTRACTOR_CustomOperator"] = "hanging_extractor.HangingExtractor"

default_args = {
    "owner": "datascience",
    "depends_on_past": False,
    "start_date": days_ago(7),
    "email_on_failure": False,
    "email_on_retry": False,
    "email": ["datascience@example.com"],
}


dag = DAG(
    "hanging_extractor_dag",
    schedule_interval="@once",
    default_args=default_args,
    description="Test dag.",
)


class CustomOperator(BaseOperator):
    def execute(self, context: Any):
        for i in range(10):
            print(i)


t1 = CustomOperator(task_id="hanging_extractor", dag=dag)
