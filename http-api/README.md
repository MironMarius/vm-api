### HTTP API

This is a small Flask app that communicates with multiple services.

#### Setup

1. Check out the repo
2. Copy `.env.sample` to `.env`
3. Install Python 3.12.0
4. Install Poetry with `python3 -m pip install poetry`
5. Install dependencies with `poetry install`
6. You can install Postgres locally or run it from the `docker-compose.yaml` of the parent directory

#### Setup the database

With Postgres running, create the database with

```bash
psql postgresql://postgres:postgres@127.0.0.1:5432 -c 'CREATE DATABASE api_development';
```
Then apply migrations with
```bash
poetry run alembic upgrade head
```

#### Running the app

```bash
poetry run python app.py

```
Open http://127.0.0.1:9000 in a browser or ping it with `curl` to see

```json
{"message":"Hello, World!"}
```
being returned.


#### Migrations

You can add new migrations with
```bash
poetry run alembic  revision --autogenerate -m "Migration name"
```

after you've modified your models. Apply them with
```bash
poetry run alembic upgrade head
