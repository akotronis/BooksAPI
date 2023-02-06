# Flask BooksAPI

# Implementation

## Endpoints

- `/olib-books` &rarr; **GET**
  - Fetches books codes defined in `book_codes.py` from open-library extracts info and populates database

# Instructions

Make `.env` file as in `.env.example`

`WORK_ENV=prod/dev/test`. If empty, defaults to `dev`. See `config.py/run.py` for details.

## Run app outside Docker

`>>> python run.py`

## Build-Run the Dockerfile locally

On the folder where `Dockerfile` is:

- `>>> docker build -t books-api-image .`
- `>>> docker run --name books-api-container -p 5000:5000 -w /app -v ${PWD}:/app books-api-image`
