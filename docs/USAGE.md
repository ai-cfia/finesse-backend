# Running and testing the API locally

## With your local environment

Create and set the environment variables based on `.env.template`. You will need
to create a `.env` file.

### Running

```bash
flask run -h 0.0.0.0 --debug
```

Alternatively, set the `FINESSE_BACKEND_DEBUG_MODE` environment variable to
`True` and run:

```bash
python run.py
```

## With docker

Create and set the environment variables based on `.env.template`. You will need
to create a `.env` file.

Build the container:

```bash
docker build -t finesse-backend .
```

Deploy the container locally:

```bash
docker run -p 5000:5000 -e PORT=5000 --env-file .env finesse-backend
```

## Check if the API is working properly

### Test the path: `/search/static`

```bash
curl -X POST http://localhost:5000/search/static --data '{"query": "is e.coli a virus or bacteria?"}' -H "Content-Type: application/json"
```

### Test the path: `/search/azure`

```bash
curl -X POST "http://localhost:5000/search/azure?top=10&skip=0" --data '{"query": "is e.coli a virus or bacteria?"}' -H "Content-Type: application/json"
```

- `top` (optional): Number of search results to return.
- `skip` (optional): Number of search results to skip from the start.

### Test the path: `/search/llamaindex`

```bash
curl -X POST "http://localhost:5000/search/llamaindex?top=10" --data '{"query": "is e.coli a virus or bacteria?"}' -H "Content-Type: application/json"
```

- `top` (optional): Number of search results to return.

### JSON structure explanation

- id: The unique identifier for each document.
- url: The URL of the document, which should point to inspection.canada.ca.
- score: Represents the search score, indicating the relevance of the document
  to the query.
- title: The title of the document.
- content: The main content or body of the document.
- subtitle: The title or titles extracted from the snippet.
- last_updated: The last modified date of the document.
