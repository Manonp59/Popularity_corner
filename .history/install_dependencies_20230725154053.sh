#!/bin/bash
p install --upgrade pip
pip install --no-binary :all: pyodbc
pip install -r requirements.txt