# CodeScript Backend

This repository contains the backend code for CodeScript.

- [codescript-frontend](https://github.com/jjpark987/codescript-frontend)
- [codescript-problems](https://github.com/jjpark987/codescript-problems)

Please read this [Dev article](https://dev.to/jjpark987/building-a-code-problem-solving-assistant-4b71) for more details.

## Getting Started

### Prerequisites

- Python 3.10+
- MySQL server

### Installation

1. Clone the repository

```zsh
git clone git@github.com:jjpark987/codescript-backend.git
```

2. Download [Ollama](https://ollama.com/) and run server

```zsh
ollama serve
```

3. Download DeepSeek model (for more models click [here](https://ollama.com/library/deepseek-r1:7b))

```zsh
ollama run deepseek-r1:7b
```

4. Create a virtual environment if there isn't one already

```zsh
python -m venv .venv
```

5. Activate virtual environment

```zsh
source .venv/bin/activate
```

6. Install dependencies

```zsh
pip install -r requirements.txt
```

7. Run API server

```zsh
uvicorn app.main:app --host 0.0.0.0
```

The API should now be running at http://0.0.0.0:8000.

## Alebmic Version Control

This project uses Alembic for managing database migrations and version control. Whenever there are updates to the database models, we must create and apply a migration to ensure that the database schema remains in sync with the application’s data structures.

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

- Make sure MySQL database server is up and migrated with the latest migration

- Seed database

```zsh
python -m app.seed
```

## Docker

- Build image and create container in the foreground

```zsh
docker compose up --build
```
