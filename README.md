# Cloud Database Creation Service

This is a service that allows you to easily create and manage cloud databases. It utilizes the power of FastAPI and Docker API to provide a reliable and efficient solution for your database needs.

## Features

- **Easy Database Creation**: With this service, you can quickly create cloud databases without the hassle of manual setup. Just provide the necessary details, and the service will handle the rest.
- **FastAPI Integration**: The service is built using FastAPI, a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. FastAPI ensures quick response times and efficient handling of requests.
- **Docker API**: Docker is an open platform for developing, shipping, and running applications. This service leverages Docker API to manage the database containers, making it easy to deploy and scale your databases.

## Getting Started

To get started with the Cloud Database Creation Service, follow these steps:

1. Clone the repository:
   ```shell
    > git clone https://github.com/Tuanpluss02/DataCloud.git
   ```
2. Create a vitural environment:
    ```shell
    > python -m venv venv
    ```
3. Configure the service:
    Rename the `.env.example` to  `.env` and modify the necessary settings, such as database credentials, Docker configuration, etc.
4. Start the service:
    ```shell 
    > docker compose up -d
    > uvicorn main:app --reload
    ```
## API Documentation
The API documentation is automatically generated and available at `http://localhost:8000/docs`. Use this documentation to understand the available endpoints, request/response formats, and to test the API directly.