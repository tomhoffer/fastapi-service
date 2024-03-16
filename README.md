# powerful-medical-assignment

This repository hosts my implementation of the assignment.

# How to run locally

## Install dependencies

`pip install -r requirements.txt`

## Initialize the pre-commit hook

The git hook automatically formats the code using the black formatter on every commit so you don't have to wait for the
CI pipeline just to realize you forgot to format the code :) Install the git hook using:
`pre-commit install `

## Run your PostgreSQL database server

For this purpose you can run your own server locally or run `make run-postgres-background` to deploy a postgresql
container using docker-compose.

# Initialize your environment variables

Create a file `.env` inside the `/src` directory and set the following env variables. Do not push this file into the
repository!

- POSTGRES_DB_HOST
- POSTGRES_DB_NAME 
- POSTGRES_DB_USER
- POSTGRES_DB_PASSWORD

## Run the server

To run the server locally, use: `run-server-local`

To run the server inside a docker container, use: `run-server-docker`

By default, server will run on 127.0.0.1:80/

# Testing

Tests in this repository are spit into 3 directories:

- `test/unit`: Unit tests containing mocked dependencies, covering the edge cases.
- `test/integration`: Integration tests which use a real dependency instead of the mocked one. Example: Method should
  actually insert a row into the PostgreSQL DB.
- `test/api`: Contains API tests using the HTTPX TestClient. No dependencies are mocked in this case as well.

I'll be happy to adopt your naming conventions and definitions for API/E2E/Integration type of tests as from my
experience, test naming conventions and understanding of what API/E2E/Integration tests are, usually differ from
company to company.

## Running the tests

To run unit tests, use `make run-unit-tests`.

To run integration and API tests, use `make run-integration-tests` and ``make run-api-tests``. These tests deploy their
own PostgreSQL container using docker compose against which the tests will be executed.

# Folder structure

- `.github`: Contains Github workflows definitions.
- `src`: Contains the source code for the server
- `src/scripts`: Contains useful scripts for easier development and testing, as well as database DDL file.
- `src/static`: Contains the static html files for serving.
- `test`: Contains unit, integration and api tests.

## Potential improvements for future

I have indentified the following potential improvements for future. I'd be happy to implement them, but I wanted to
avoid over-engineering without confirming these improvements are needed.

- The current implementation does not make use of asynchronous capabilities of the psycopg library. If higher
  performance is required, it might be worth rewriting the server part to use asyncio as the main purpose of the
  database part of the server is to make I/O calls to the database. The XML<->JSON conversion part would be extracted to
  a separate server so that it doesn't block the event loop when processing large inputs.

- Read performance of the DB Selects could be improved by creating an index over the email column. Enabling it however
  introduces a penalty when it comes to `INSERT`, `UPDATE` and `DELETE` queries.

- Deletion performance could be improved by implementing soft_deletes and deleting the records in bulk during a
  low-usage period. But again, it introduces trade-offs in terms of memory, foreign key management and more complex
  queries.

- Security issue: Solution does not limit the user input size submitted to the `/json2xml` and `/json2xml` endpoints,
  nor does it sanitize the xml input to protect
  against [common XML vulnerabilities](https://cheatsheetseries.owasp.org/cheatsheets/XML_Security_Cheat_Sheet.html). I
  would use a well-established library for XML parsing if this was a production service.

- Circuit breaking, Caching, Rate-limiting and server replication (Load balancing) could help increase performance.
