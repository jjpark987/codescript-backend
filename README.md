# CodeScript Backend

This repository contains the Rails version of the backend code for CodeScript.

- [codescript-demo](https://github.com/jjpark987/codescript-demo)
- [codescript-frontend](https://github.com/jjpark987/codescript-frontend)
- [codescript-problems](https://github.com/jjpark987/codescript-problems)

Please read this [Dev article](https://dev.to/jjpark987/building-a-code-problem-solving-assistant-4b71) for more details.

## Getting Started

### Prerequisites

- Ruby 3.4.3
- Rails 8.0.2
- PostgreSQL server

### Installation

1. Clone the rails branch of the repository.

```zsh
git clone --branch rails git@github.com:jjpark987/codescript-backend.git
```

2. Download [Ollama](https://ollama.com/) and run server

```zsh
ollama serve
```

3. Download DeepSeek model (for more models click [here](https://ollama.com/library/deepseek-r1:7b))

```zsh
ollama run deepseek-r1:7b
```

4. Install dependencies

```zsh
bundle install
```

5. Create PostgreSQL database

```zsh
rails db:create
```

6. Migrate

```zsh
rails db:migrate
```

7. Run API server

```zsh
rails server
```

The API should now be running at http://localhost:3000.

## Seeding Database

### Local MySQL

To seed the database with:
- 3 categories (data manipulations, combinatorics, optimizations)
- subcategories for each category

- Make sure PostgreSQL database server is up and migrated with the latest migration

- Seed database

```zsh
rails db:seed
```

## Docker

- Build image and create container in the foreground

```zsh
docker compose up --build
```
