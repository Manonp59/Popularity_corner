#!/bin/bash
/Users/ant/miniconda3/envs/ml_recap/bin/python3.10 install --upgrade pip
 install --no-binary :all: pyodbc
pip install -r requirements.txt