
# 📦 Rack Management Service

Rack and device management service built with **FastAPI** and **PostgreSQL**, following a Domain-Driven Design (DDD) architecture.

---

## 🚀 Tech Stack

* **Backend:** FastAPI
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Migrations:** Alembic
* **Containerization:** Docker & Docker Compose
* **Testing:** Pytest

---

## 🐳 Running the Project

### ✅ Initial Setup

After cloning the repository, simply run:

```bash
make all
```

That’s it.

This command will:

1. Stop existing containers
2. Build Docker images
3. Start services
4. Run database migrations
5. Execute tests

---

## 🌐 Application Access

Once running, the API is available at:

```
http://localhost:8000
```

Swagger documentation:

```
http://localhost:8000/docs
```

---

## 🛠 Makefile Commands

You can run individual commands if needed:

| Command                      | Description                            |
| ---------------------------- | -------------------------------------- |
| `make build`                 | Build Docker containers                |
| `make up`                    | Start services                         |
| `make down`                  | Stop and remove containers and volumes |
| `make test`                  | Run tests inside Docker                |
| `make logs`                  | Show last 25 logs from API container   |
| `make migration m="message"` | Create new Alembic migration           |
| `make upgrade-head`          | Apply latest database migrations       |

---

## 🗂 Project Structure

```
app/
├── api/            # FastAPI routes
├── domain/         # Domain entities (DDD core)
├── services/       # Application services
├── infrastructure/ # Repositories & DB models
├── main.py         # FastAPI entrypoint
```

---

## 🐳 Docker Configuration

The application runs inside a Docker container based on:

```dockerfile
python:3.12-slim
```

It installs:

* gcc
* libpq-dev

The service is started with:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Port exposed:

```
8000
```

---

## 🧪 Running Tests

To run tests manually:

```bash
make test
```

Tests are executed inside Docker to ensure consistency.

---

## 🗄 Database Migrations

Create a new migration:

```bash
make migration m="your_message"
```

Apply migrations:

```bash
make upgrade-head
```

---

## 🧱 Architecture

This project follows a layered DDD approach:

* **Domain Layer** → Entities & business logic
* **Application Layer** → Services
* **Infrastructure Layer** → Repositories & DB
* **API Layer** → FastAPI endpoints

Unit tests mock repositories.
Integration tests use real PostgreSQL.

---

## 📌 Requirements

* Docker
* Docker Compose
* Make

---

## 👨‍💻 Author

Aleksandar Perovic


