# Flask BoksAPI

## How to build-run the Dockerfile locally

On the folder where `Dockerfile` is, RUN:

- `docker build -t books-api-image .`
- `docker run --name books-api-container -p 5000:5000 -w /app -v ${PWD}:/app books-api-image`
