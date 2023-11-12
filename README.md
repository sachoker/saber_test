# Python Build System

This is a simple microservice written in Python using FastAPI. It loads tasks and builds from yaml files and provides a POST `/get_tasks` endpoint that accepts a JSON request with a build name and returns a list of tasks sorted according to their dependencies.

## Installation

1. Install Python 3.11 or higher.
2. Clone this repository.
3. Install the dependencies using pip:

```bash
pip install -r requirements.txt
```

## Running the Application

You can run the application locally using the command:

```bash
uvicorn main:app --reload
```

## Docker

You can also run the application in Docker using Docker Compose:

```bash
docker.exe compose -f ./docker-compose.yml -p saber_test up -d
```

## Testing

To run the tests, use the command:

```bash
pytest test.py
```

## API

The POST `/get_tasks` endpoint accepts a JSON request with a build name and returns a list of tasks sorted according to their dependencies.

Example request:

```json
{
    "build": "test_build"
}
```

Example response:

```json
["pack_game_files", "pack_docker", "pack_server_files", "build_exe", "pack_in_zip"]
```
