# pg-isready-web

[![GitHub release](https://img.shields.io/github/v/release/wlad031/pg-isready-web)](https://github.com/wlad031/pg-isready-web/releases)
[![Docker Pulls](https://img.shields.io/docker/pulls/wlad031/pg-isready-web)](https://hub.docker.com/r/wlad031/pg-isready-web)
[![License](https://img.shields.io/github/license/wlad031/pg-isready-web)](https://github.com/wlad031/pg-isready-web/blob/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/wlad031/pg-isready-web)](https://github.com/wlad031/pg-isready-web/issues)

A Flask-based web API to check PostgreSQL readiness inside a running Docker container using `pg_isready`.

[Docker Hub](https://hub.docker.com/r/wlad031/pg-isready-web) | [Changelog](CHANGELOG.md) | [Contributing](CONTRIBUTING.md)

## Motivation

This service provides a simple HTTP API to check if a PostgreSQL database is ready using the `pg_isready` command inside a Docker container. It is useful for monitoring and health checks in containerized environments.

## Installation

### Prerequisites

- Python 3.x
- Docker installed on the host

### Environment Variables

- `POSTGRES_CONTAINER`: Name of the running PostgreSQL container (default: `postgres`)
- `DOCKER_HOST`: Docker socket URL (default: `unix://var/run/docker.sock`)
- `PORT`: Port for the Flask API (default: `80`)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/wlad031/pg-isready-web.git
   cd pg-isready-web
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python pg-isready-web.py
   ```

## Usage

### Docker Compose

You can run pg-isready-web using Docker Compose:

```yaml
version: '3'
services:
  pg-isready-web:
    image: ghcr.io/wlad031/pg-isready-web:latest
    environment:
      - POSTGRES_CONTAINER=postgres
      - DOCKER_HOST=unix://var/run/docker.sock
      - PORT=8080
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    ports:
      - "8080:8080"
```

### API Endpoints

#### Health Check
```bash
curl http://localhost:8080/health
```
Returns `200 OK` with `{"status": "healthy"}` when the service is running properly.

#### Check PostgreSQL Readiness
```bash
curl -X GET "http://localhost:8080/pg_isready/my_database?username=my_user"
```
**Response:**
```json
{
  "database": "my_database",
  "username": "my_user",
  "container": "postgres",
  "status": "ready",
  "output": "my_database:5432 - accepting connections"
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.


