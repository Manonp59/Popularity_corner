#!/bin/bash
/Users/ant/miniconda3/envs/app_cinema/binpip install --upgrade pip
pip install --no-binary :all: pyodbc
pip install -r requirements.txt