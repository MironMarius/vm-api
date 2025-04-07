FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
  gcc \
  libpq-dev \
  curl \
  libc-dev \
  && rm -rf /var/lib/apt/lists/*

RUN pip install poetry==2.1.1

COPY pyproject.toml ./

RUN poetry config virtualenvs.create false

RUN poetry install --only main --no-interaction --no-ansi --no-root

COPY . .

CMD ["sh", "-c", "alembic upgrade head && python app.py"]

EXPOSE 9000
