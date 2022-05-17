NiPAMS VCG Blood Pressure Estimation
==============================
[Work In Progress]

## Overview
Repository for all aspects of Exploratory Analysis, Processing, Modeling and Evaluation of NiPAMS Vibrational Cardiography (VCG) to Blood Pressure Estimation algoriths & system. 

Available both as a series of notebooks and/or an interactive dashboard/modeling application.

<br/>

## VCG Acquisition & Prediction Overview

![title](assets/Nipams_ML_Pipeline_Simplified.png)

<br/>


# Get Started !
## Run Analysis Engine
1. Prerequisite : Install Docker (and Docker-Compose) - https://docs.docker.com/get-docker/

1. Run the Command to Build and Deploy Interactive Application
    ```
    docker-compose up
    ```
1. Access & interact with NiPAMS Analysis Engine : 
    <!-- 1. Primary Application : http://localhost:8501/ -->
    1. Python Notebooks - Visit the following link : http://localhost:8888?token=nipams
    1. Python CLI - Run the following in terminal : `docker exec -it nipams-data-jupyterlab python`
    1. Bash (Root) - Run the following in terminal : `docker exec -it nipams-data-jupyterlab bash`

<br/>

# Development Environment Setup

## Local Machine (Docker)
Uses Docker and DockerCompose to build disk images and run containers within Docker Engine
- Prerequisites
    - Ensure Docker Engine is running
    - Build Docker Containers
        ```
        docker-compose build 
        ```
    - Start your Engine!
        ```
        docker-compose up 
        ```
- Notebooks (JupyterLab)
    - Start App (PreReq above)
    - View logs for similar URL : http://127.0.0.1:8888/lab?token=nipams

## Colab (Cloud)
### Overview :
Uses Google-provided Colab computing platform
Recommend running larger jobs with paid Colab accounts for higher-memory.

- Notebooks
    - Run Colab Notebooks as you would normally (from Google Drive).
- Dash Application
    - Open "LifeCycle" Colab Notebook & Open Terminal
    - Run the following command to start Dash App
        ```
        python3 src/dash/index.py
        ```
    - Visit the link
- VSCode Editor (Online)
    - Open "LifeCycle" Colab Notebook & Open Terminal
    - Run the following commands to setup the ngrok tunnel and start VSCode
    ```
    cd "{PROJECT_FOLDER}" && colabcode --port 10000 && rm install.sh    
    ```
- Git
    - Ensure the Git creds are in .env
    - Connect & Authenticate with Git

<br/><br/>
------------


# System Architecture

![title](assets/Nipams_ML_Pipeline_Full.png)

<br/><br/>
# Nipams Code Organization

    ├── README.md          <- The top-level README for collaborators of the nipams project.
    ├── .git               <- includes .gitignore - Everything related to changelogs and version management
    ├── data
    │   ├── raw        <- Intermediate data that has been transformed (matlab files & python dataframes)
    │   ├── interim        <- Intermediate data that has been transformed (matlab files & python dataframes)
    │   ├── processed      <- The final, canonical data sets for modeling (includes interpolation).
    │   └── raw_mat            <- Raw VCG Data from patient trials (sourced from gDrive).
    │
    ├── models             <- Trained and serialized models and model summaries
    │
    ├── notebooks          <- Colab/Jupyter notebooks. Naming convention `<date>-<initials>-<notebook title>`.
    │
    ├── reports            <- Generated analysis as HTML, PDF, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── utils          <- Scripts for platform agnostic helpers and environments
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   ├── load_data.py
    │   │   └── preprocess.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   ├── simple.py
    │   │   └── tsfel_vectorizer.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make predictions
    │   │   ├── analytical_mvd.py
    │   │   ├── baselines.py
    │   │   ├── experiments.py
    │   │   ├── nn_tsai.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    ├── env            <- Environment variables and configurations for build and runtime
    │   ├── local.yml 
    │   ├── colab.yml 
    │   └── default.yml 
    ├── docker-compose.yml <- Configuration for Docker Compose for defining and running multi-container 
    └── Dockerfile         <- Dockerfile contains all the commands a user could call on the command line to assemble an image




<br/><br/>

# Life Cycle Operations

1. Connect to bash
    ```
    docker exec -it nipams-data-jupyterlab bash
    ```
1. Display Help Information
    ```
    docker exec -it nipams-data-jupyterlab python src/scripts/load_data.py -h
    ```
1. Execute LifeCycle Script
    ```
    docker exec -it nipams-data-jupyterlab \
        python src/scripts/load_data.py \
        --input.folder=./data
        --output.folder=./data
    ```



## Loading & Preprocessing
__Description__ : The Loading & Preprocessing script will 

__Script File__ : 1_load_data.py

__Arguments__ :
- **download.source** : This is the remote folder in which to search
- **download.out_folder** : The local folder in which to download files
- **input.folder** : If download folder is not provided assumes loading from local folder
- **input.pattern** : This is the file regex pattern to use when searching for files
- **input.limit_files** : This is the limit_files variable
- **preprocess.type** : This is the preprocess type input parameter
- **output.file_path** : Output file path

<br/>

## Graphing & Analysis
__Description__ : The Graphing & Analysis script will 

__Script File__ : 2_draw_chart.py

__Arguments__ :
- **input.folder** : This is the folder in which to search
- **input.data_path** : Points to the specific file to load within the input folder
- **chart.type** : This is the chart type parameter, defaults to timeline
- **chart.configuration** : This is the additional chart configurations in JSON form
- **output.file_path** : Output Chart file path

<br/>

## Feature & TimeSeries Vectorization
__Description__ : The Feature & TimeSeries Vectorization script will 

__Script File__ : 3_build_features.py

__Arguments__ :
- **input.file_path** : This parameter points to the specific preprocessed dataset file
- **feature.type** : Overarching type of featurizing being calculated
- **feature.configuration** : Generic feature generation configuration JSON
- **output.file_path** : Output file path

<br/>

## Model Training & Prediction
__Description__ : The Model Training & Prediction script will 

__Script File__ : 4_train_model.py

__Arguments__ :
- **input.folder** : This parameter points to the specific folder in which to search
- **input.data_path** : Points to the specific file to load within the input folder
- **experiment.split_type** : Indicates which strategy to use when generating splits
- **experiment.configuration** : Additional configurations for train & test splitting configuration
- **model.type** : Overarching model type - analytical, machine learning, deep learning
- **model.configuration** : Additional details for model configuration
- **model.pipeline** : The most flexible approach to pipeline creation for modeling
- **output.model_path** : The destination folder path in which to save the model snapshot
- **output.file_path** : The output resulting predictions file path to save the results

<br/>

## Evaluation
__Description__ : The Evaluation script takes a trained model and experiment_split to output the resulting model __score.__

__Script__ File : 5_predict_and_evaluate.py

Arguments :
- **input.folder** : This parameter points to the specific folder in which to search
- **input.data_path** : Points to the specific file to load within the input folder
- **input.model_path** : The source folder path in which to load the model snapshot
- **experiment.split_type** : Indicates which strategy to use when generating splits
- **experiment.configuration** : Additional configurations for train & test splitting configuration
- **output.file_path** : The output resulting predictions file path to save the results

<br/>