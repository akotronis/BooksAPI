# Flask BooksAPI

A CRUD rest api app for books fetched from [Openlibrary](https://openlibrary.org/developers/api)

# Implementation

## Models

Database models were created according to the logic indicated in the below diagram

[Database diagram](https://drawsql.app/teams/akotronis-team/diagrams/books)

(Folder **models**)

- `book`
- `author`
- `work`
- `book_author`
- `book_work`
- `user`

As indicated from openlibrary data,

- A **book** [may have](https://openlibrary.org/books/OL1017798M.json) multiple **authors** and belong to multiple **works**
- A **work** [may contain](https://openlibrary.org/works/OL45804W/Fantastic_Mr_Fox) multiple **books** and
- An **author** may have written multiple **books**

Implementation with [`flask-sqlalchemy`](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)

## Authentication

User authentication implemented with [`flask-jwt-extended`](https://flask-jwt-extended.readthedocs.io/en/stable/)

(Currently protected endpoint: `/books` &rarr; **GET**. Uncomment decorator `@jwt_required()` to protect others)

## Data transfer validation/(de)serialization

Implemented with [`marshmallow`](https://marshmallow.readthedocs.io/en/stable/)

(Folder **schemas**)

- `book`
- `author`
- `work`
- `book_author`
- `book_work`
- `user`

## Endpoints

(Folder **resources**)

- `olib_book`
- `book`
- `author`
- `work`
- `user`

In openlib there are books without registered _authors_, which suggests that _authors_ should be handled by separate endpoints, decoupled from _book_ endpoints implementation.

So the endpoints are the below:

### Books

- `/olib-books` &rarr; **GET**
  - Fetch book codes defined in `book_codes.py` from open-library, extracts info, clean tables and populate database
  - Accepts query `asynchronously=<bool>` based on which the get requests to open library are performed _sequentially_ (`asynchronously=False`) or _concurrently_ (`asynchronously=False`) using `requests` module in combination with `asyncio`. Second option is **significantly faster**.
- `/books/<book_id>` &rarr; **GET, PUT, DELETE** a book with a specific `book_id`
- `/books` &rarr; **POST**
  - Create a book with `{'code': <book_code_str>, 'title': <book_title_str>}`
- `/books` &rarr; **GET**
  - Get list of all books in database. May filter results by adding query `contains=<string>` (Filters by `<string>` in `title`, case insensitive)
- `/books/<book_id>/authors/<author_id>` &rarr; **POST**
  - Link a book to an author. Add a row to `books_authors` table
- `/books/<book_id>/works/<work_id>` &rarr; **POST**
  - Link a book to a work. Add a row to `books_works` table

### Authors

- `/authors/<author_id>` &rarr; **GET, PUT, DELETE** an author with a specific `author_id`
- `/authors` &rarr; **POST**
  - Create an author with `{'code': <author_code_str>}`
- `/authors` &rarr; **GET**
  - Get list of all authors in database

### Works

- `/works/<work_id>` &rarr; **GET, PUT, DELETE** a work with a specific `work_id`
- `/works` &rarr; **POST**
  - Create a work with `{'code': <work_code_str>}`
- `/works` &rarr; **GET**
  - Get list of all works in database

### Users

- `/users/register` &rarr; **POST** register a user with with `{'username': <username>, 'password': <password>}`
- `/works` &rarr; **POST**
  - Create a work with `{'code': <work_code_str>}`
- `/works` &rarr; **GET**
  - Get list of all works in database

# Instructions

Make `.env` file as in `.env.example`

`WORK_ENV=prod/dev/test`. If empty, defaults to `dev`. See `config.py/run.py` for details.

## Run app outside Docker

`>>> python run.py`

## Build-Run the Dockerfile locally

With Docker (Desktop) installed, on the folder where `Dockerfile` is:

- `>>> docker build -t books-api-image .`
- `>>> docker run --rm -it --name books-api-container -p 5000:5000 -w /app -v ${PWD}:/app books-api-image` (Powershell) OR
- `>>> docker run --rm -it --name books-api-container -p 5000:5000 -w /app -v "%cd%":/app books-api-image` (Terminal)

# TODO

- Implement versioning with Blueprints
- Documentation with `flask-smorest/swagger`
- Use `flask-migrate` for migrations
- Use `gunicorn` as a server
- Unit testing
