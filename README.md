# backend

    - Python version: 3.11.3
    - pip verison: 22.3

## Project structure

```
ITA-APP-SERVER
└───src
|   │   └───app
|   │   |   ├───crud         # crud services
|   │   |   ├───db           # database connection and config
|   │   |   ├───models       # db models
|   │   |   ├───routers
|   │   |   ├───schemas      # pydantic models
|   │   |   ├───constants    # local configs
|   │   |   ├───utils        # local utils such as logging module
|   │   |   ├───api.py
|   │   |   ├───Dockerfile
|   │   |   ├───poetry.lock
|   │   |   ├───pyproject.toml
|   |   |___logs             # include log files
```

### Development

If you are about to add new dependencies during the development, please follow **all** the steps below. If there is no need to add a new dependency, please follow from **Step 5** to **Step 6**.

1. Follow steps in this [website](https://docs.conda.io/en/latest/miniconda.html#installing) to install MiniConda.
2. Run the following commands

```shell
# Create a virtual environment
conda create -n voiads-app-server python=3.11
# Activate the virtual environment
conda activate voiads-app-server
```

3. Follow steps in this [website](https://python-poetry.org/docs/#installation) to install Poetry.
4. Install all dependencies

```
poetry lock
poetry install
```

6. (Optional) Add a new dependency

Navigate to the directory of the service where you want to add a new dependency.

```shell
# If the dependency for both development and production
poetry add [dependency-name]
# If the dependency only for development
poetry add -D [dependency-name]
```

7. Run docker

```
docker compose --profile dev up
```
