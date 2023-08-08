#!/bin/bash
airflow scheduler &
airflow webserver -p 8080