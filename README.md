# Path of Exile Currency Tracker

A data engineering project to collect, store, and analyze Path of Exile currency data over the course of a league. This project leverages Apache Airflow for orchestration, PostgreSQL for storage, and Docker Compose for containerization. Data is sourced from [poe.ninja](https://poe.ninja).

---

## Features

- Scheduled DAGs using Airflow to fetch currency data
- Data persistence using PostgreSQL
- Containerized environment using Docker Compose
- Healthchecks to monitor the state of critical services
- Environment variables for secrets and configuration
- Ready for local development and experimentation

---

## Technologies

- Python 3.11
- Apache Airflow 2.9.0
- PostgreSQL 13
- Docker / Docker Compose
- Bash
- REST APIs

---

## Prerequisites

Make sure the following are installed:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/)
- (Optional) [DBeaver](https://dbeaver.io/) or another SQL client

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/PoE_Ninja_Currency.git
cd PoE_Ninja_Currency
```

### 2. Create the `.env` File

```bash
cp .env.example .env
```

Generate a Fernet key:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Paste it into your `.env` file under `FERNET_KEY`.

### 3. Start the Containers

```bash
docker compose up -d
```

This launches:

- PostgreSQL (`poe_postgres`)
- Airflow Webserver (`poe_airflow`)
- Airflow Scheduler (`poe_scheduler`)

### 4. Access the Airflow UI

Navigate to: [http://localhost:8080](http://localhost:8080)  
Use the login credentials from your `.env` file.

---

## Environment Variables

Create your `.env` file using the template below:

```env
DB_USER=airflow
DB_PASSWORD=airflow
DB_NAME=airflow

AIRFLOW_ADMIN_USERNAME=admin
AIRFLOW_ADMIN_PASSWORD=supersecret
AIRFLOW_ADMIN_EMAIL=admin@example.com

FERNET_KEY=your_32_byte_base64_fernet_key
```

**Do not commit `.env` to version control.** Use `.env.example` instead.

---

## DAGs

- Located in the `./dags/` directory
- Logs saved in `./logs/`
- Trigger or monitor DAGs through the Airflow UI

---

## Database Persistence

PostgreSQL uses a named volume:

```yaml
volumes:
  - postgres-db-volume:/var/lib/postgresql/data
```

To reset everything:

```bash
docker compose down -v
```

To inspect volumes:

```bash
docker volume ls
```

---

## Healthchecks

Containers uses a healthcheck:

- **PostgreSQL**: `pg_isready -U $DB_USER`
- **Airflow Webserver**: `curl -f http://localhost:8080/health`

Check status using:

```bash
docker ps
```

Look for container status: `healthy` / `unhealthy`.

---

## Troubleshooting

### Database won't start

- Verify `.env` values
- View logs: `docker logs poe_postgres`

### Scheduler not executing DAGs

- Ensure `poe_scheduler` is running
- View logs: `docker logs poe_scheduler`

### Environment changes not reflected

Restart containers:

```bash
docker compose down
docker compose up -d
```
