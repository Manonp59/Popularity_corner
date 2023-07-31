#!/bin/bash
/Users/ant/miniconda3/bin/python3.10 install --upgrade pip
pip install --no-binary :all: pyodbc
pip install -r requirements.txt