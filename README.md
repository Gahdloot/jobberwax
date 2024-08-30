#jobberwax
This repository contains a Django application configured to run with Docker and Docker Compose. It includes a PostgreSQL database service and an API service using Gunicorn as the WSGI server.

## Features

- **Django 4.x**: A powerful web framework.
- **PostgreSQL 13**: A reliable and robust relational database.
- **Gunicorn**: A Python WSGI HTTP Server for UNIX.
- **Docker**: For containerizing the application.
- **Docker Compose**: To manage multi-container Docker applications.

## Getting Started

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Gahdloot/jobberwax.git
    cd joberwax
    ```

2. **Set up environment variables**:

   Create a `.env` file in the project root and add your environment-specific variables, like this:

    ```bash
    API_ACCESS_KEY=bwfigujsoijrgoirsjngoirsjg94r93ie039131-23kemfalk.f,.,df/fd?jrnrw3
    API_REFRESH_SECRET=...
    POSTGRES_PASSWORD=...
    POSTGRES_DB=...
    POSTGRES_USER=...
    POSTGRES_HOST=...
    POSTGRES_PORT=...
    POSTGRES_NAME=...
    SECRET_KEY=...
    ```

3. **Build and start the containers**:
    ```bash
    docker-compose up 
    ```