
# QED recruitment task

## Basic configuration

### Launch the application using Docker.
In the root directory, call the command 
```bash
docker compose up
```
By default, the application launches under port 8081

In the docker configuration, the application consists of three containers:

 - qed - the container containing the main application, based on FastAPI
 - qed_worker - the container responsible for the functioning of the Celery worker, needed for effective synchronization management in the application
 - redis - the broker

### Developer cycle

The application is based on Python 3.12.3 (recommends using a Python virtual environment). For a correct development cycle, the needed resource packages have been separated from the base ones. To install, wkon from the `app/` directory the command:
```bash
pip install -r requirements/dev.txt
```
Tools used:

**pre-commit**.
The applications used for pre-commit include:
 - black 
 - isort
 - mypy
 - ruff
 
The pre-commit configuration is located in the `.pre-commit-config.yaml` file in the main directory. In the same directory is the configuration file for the applied applications themselves: `pyproject.toml`.

## Endpoints
Documentation available at `<address:8081>/docs`.
 - [POST] /api/train/run - Training model
 - [GET] /api/train/check/<task_id> - Checking the training status of a particular model
 - [POST] /api/predict/use - Use of the last trained model
## Tests & coverage
1 From the `app/` directory, call the command:
```bash
coverage run -m pytest .
```
2. to generate a report call the command.
```bash
coverage report -m
```
