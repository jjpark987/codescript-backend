# CodeScript

This repository contains the backend code for CodeScript.

## Getting Started

### Prerequisites

- Python 3.10+
- MySQL server

### Installation

1. Clone the repository

```zsh
git clone git@github.com:jjpark987/codescript-backend.git
```

2. Create a virtual environment if there isn't one already

```zsh
python -m venv .venv
```

3. Activate virtual environment

```zsh
source .venv/bin/activate
```

4. Install dependencies

```zsh
pip install -r requirements.txt
```

5. Run API server

```zsh
uvicorn app.api.main:app --host 0.0.0.0 --port 80
```

The API should now be running at http://0.0.0.0:80.

## Alebmic Version Control

This project uses Alembic for managing database migrations and version control. Whenever there are updates to the database models, it is essential to create and apply a migration to ensure that the database schema remains in sync with the application’s data structures.

1. Create migration

```zsh
alembic revision --autogenerate -m "Migration message"
```

2. Migrate

```zsh
alembic upgrade head
```

## Seeding Database

To seed the database with:
- 3 categories (data manipulations, combinatorics, optimizations)
- subcategories for each category

1. Make sure MySQL database is set up and migrated with the latest migration

2. Seed database

```zsh
python -m app.database.seed
```

## Docker

- Force build and run containers in the foreground

```zsh
docker compose up --build
```

- Build and run containers in the foreground

```zsh
docker compose up
```

- Build and run containers in background

```zsh
docker compose up -d
```

- Start previously stopped containers

```zsh
docker compose start
```

- Stop and remove containers

```zsh
docker compose down
```

- Stop containers without removing

```zsh
docker compose stop
```

- Restart containers in the background (compose down and up)

```zsh
docker compose restart
```

- Check container status

```zsh
docker ps
```

- Open a shell inside an already running container

```zsh
docker exec -it codescript-fastapi bash
```
