## Running and testing the API

Running:

```
flask run -h 0.0.0.0 --debug
```

Query from the command-line:

```
curl -X POST http://localhost:5000/search --data '{"query": "is e.coli a virus or bacteria?"}' -H "Content-Type: application/json"
```

JSON structure explanation:

- id: The unique identifier for each document.
- url: The URL of the document, which should point to inspection.canada.ca.
- score: Represents the search score, indicating the relevance of the document to the query.
- title: The title of the document.
- content: The main content or body of the document.
- subtitle: The title or titles extracted from the snippet.
- last_updated: The last modified date of the document.
