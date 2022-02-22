nipams-data-project
==============================

Work in progress.. Python repository for all aspects of exploratory analysis, processing, modeling and evaluation of Nipams VCG to Blood Pressure Prediction System. Available both as a series of notebooks and/or an interactive dashboard/modeling application.

# Simply Run The Nipams App!
- Ensure Docker and Docker-Compose are installed and DockerEngine is running
- Run the Command to Build and Deploy Interactive Application
    ```
    docker-compose up
    ```
- Visit the following link : http://localhost:8501/

# Start Coding!
## Setting /.env folder
- Overview : 
- What to include : 
    1. GIT Creds (User, Token)
    2. ngrok

## Colab
- Overview :
    - Uses Google-provided Colab computing platform
    - Recommend running larger jobs with paid Colab accounts for higher-memory.
- Notebooks
    - Run Colab Notebooks as you would normally (from Google Drive).
- Dash Application
    - Open "LifeCycle" Colab Notebook & Open Terminal
    - Run the following command to start Dash App
        ```
        python3 src/dash/index.py
        ```
    - Visit the link
- VSCode Editor
    - Open "LifeCycle" Colab Notebook & Open Terminal
    - Run the following commands to setup the ngrok tunnel and start VSCode
    ```
    
    ```
- Git
    - Ensure the Git creds are in .env
    - Connect & Authenticate with Git

## Local
Uses Docker and DockerCompose
- PreReq
    - Ensure Docker Engine is running
    - Build!
        ```
        docker-compose build 
        ```
    - Start!
        ```
        docker-compose up 
        ```
- Notebooks (JupyterLab)
    - Start App (PreReq above)
    - View logs for similar URL : http://127.0.0.1:8888/lab?token=
- Dash Application
    - Start App (PreReq above)
    - Visit URL : http://0.0.0.0:8501/


Nipams Project Organization
------------

    ├── README.md          <- The top-level README for collaborators of the nipams project.
    ├── .git               <- includes .gitignore - Everything related to changelogs and version management
    ├── data
    │   ├── interim        <- Intermediate data that has been transformed (matlab files & python dataframes)
    │   ├── processed      <- The final, canonical data sets for modeling (includes interpolation).
    │   └── raw            <- Raw VCG Data from patient trials (sourced from gDrive).
    │
    ├── docs               <- Folder for sensor collection details and data dictionaries (structures, indexes, etc)
    │
    ├── models             <- Trained and serialized models and model summaries
    │
    ├── notebooks          <- Colab/Jupyter notebooks. Naming convention `<date>-<initials>-<notebook title>`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials. (includes lifecycle operations)
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
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
    │   ├── dash           <- Scripts to create interactive dashboard application
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    ├── .env.yml           <- Environment variables and configurations for build and runtime
    ├── docker-compose.yml <- Configuration for Docker Compose for defining and running multi-container Docker applications
    └── Dockerfile         <- Dockerfile contains all the commands a user could call on the command line to assemble an image



--------

