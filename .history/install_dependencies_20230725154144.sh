#!/bin/bash
/Users/ant/miniconda3/envs/ml_recap/bin/python3.10 install --upgrade pip
/Users/ant/miniconda3/envs/ml_recap/bin/python3.10 install --no-binary :all: pyodbc
 install -r requirements.txt