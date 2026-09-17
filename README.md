# Stocks Data Pipeline with Airflow
## Contents
1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [prerequisites](#prerequisites)
4. [Project Structure](#project-structure)
4. [Project Architecture](#project-architecture)
6. [Project environment setup](#environment-setup)
7. [Triggering the DAG](#triggering-the-dag)

## Project Overview
This project provides an Airflow DAG that triggers a data pipeline to asynchronously extract stock data from the [MASSIVE REST API](https://massive.com), transform the data into a logical structure, and load the cleaned data into a PostgreSQL database.
## Tech Stack
- Python
- SQLAlchemy
- psycopg2
- pandas
- asyncio
- MASSIVE API
- Airflow
- PostgreSQL

## Prerequisites
1. A running PostgreSQL database
2. [A MASSIVE API key](https://massive.com/dashboard/signup?redirect=%2Fdashboard%2Fkeys)
3. [Airflow installation](https://airflow.apache.org/docs/apache-airflow/stable/start.html)

## Project Structure
```text
stock_data_pipeline
├── README.md                   #project documentation
├── config.py                   #Environment settings
├── dags
│   └── stocks_pipeline.py      #Orchestration logic
├── etl
│   ├── __init__.py             #package initialization
│   ├── extract.py              #data extraction logic
│   ├── load.py                 #database upload logic
│   └── transform.py            #transformation logic
└── requirements.txt            #list of dependencies
```

## Project Architecture
The project architecture can be divided into 2 sections
1. The ETL pipeline
2. The Airflow DAG
### ETL pipeline
This section contains 3 subsections:
#### Extract
This is defined by the logic inside the [extract.py](etl/extract.py) module. `asyncio`, `aiohttp`, and `aiolimiter` libraries are implemented in this module to asynchronously extract data from the MASSIVE REST API while considering the API's rate limiting constraints.
#### Transform
After extracting the data, it is organized into the desired structure using the `pandas` library.
#### Load
The cleaned data is now ready to be uploaded to the database. This is implemented by using `SQLAlchemy` and the `psycopg2` driver to connect to the specified database, and the Pandas `to_sql` function to upload the data to the DB.
### Airflow DAG
This is where the orchestration logic is organized as a DAG (Directed Acyclic Graph) inside the [stocks_pipeline.py](dags/stocks_pipeline.py) file. It implements Airflow's [TaskFlow API](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/taskflow.html) to facilitate the flow of data between the tasks.
### General Structure
```text
 -------
|Airflow|
 -------
    ⬇ trigger
 ---------    
|Pipeline |
|---------|     -----------
|Extract  | ⟵ |MASSIVE API|
|   ⬇     |     -----------
|Transform|
|   ⬇     |  
|  Load   |
 ---------
    ⬇
 --------
|Database|
 --------
```


## Environment Setup
### Python Virtual Environment
Create a python virtual environment to manage the project dependecies
```bash
$ python -m venv <your_venv_name>
#activate the virtual environment
$ source <your_venv_path>/bin/activate
```
### Cloning the Project
Clone the project and switch to the project directory.
```bash
$ git clone <project repository>
$ cd stock_data_pipeline
```
### Dependencies Installation
Install all the project dependencies inside the [requirements.txt](requirements.txt) file.
```bash
$ git install -r requirements.txt
```
### Airflow Metadata Database and Dag location configuration
Navigate to the installed airflow directory and locate the [airflow.cfg](dummy_airflow.cfg) file. Inside, modify the path configuration which airflow will use to automatically locate the DAG(s). Also ensure to modify the metadata database for airflow.
```text
# The folder where your airflow pipelines live, most likely a
# subfolder in a code repository. This path must be absolute.
#
# Variable: AIRFLOW__CORE__DAGS_FOLDER

dags_folder = home/stocks_data/airflow/dags

------------------------------------------------

# Variable: AIRFLOW__DATABASE__SQL_ALCHEMY_CONN
#
sql_alchemy_conn = postgresql+psycopg2://DB_username:password@host:port/db_name
```

## Triggering the DAG
1. Start airflow and open the airflow UI
```bash
$ export AIRFLOW_HOME=<your_airflow_directory>
$ airflow standalone
```
Inside a browser open airflow on port `8080` and provide you login credentials
<div>
<img src="airflow_login.png" alt="airflow login">
<i><figcaption align="center">airflow login</figcaption></i>
</div>

2. locate the name of your pipeline DAG under dags, click on it and then manually trigger the dag by clicking the trigger button on the top right corner of the UI.

<div>
<img src="airflow_landing.png" alt="airflow landing">
<i><figcaption align="center">airflow landing page</figcaption></i>
</div>

<div>
<img src="triggering_dag.png" alt="triggering the dag">
<i><figcaption align="center"> Manual trigger </figcaption></i>
</div>

<div>
<img src="successful_run.png" alt="successful run">
<i><figcaption align="center">successful dag run </figcaption></i>
</div>

When the DAG runs successfully, the database will have a table as shown below:
<div>
<img src="news_table.png" alt="news table">
<i><figcaption align="center"> News table </figcaption></i>
</div>