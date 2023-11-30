## Running and testing the API
Create and set the environment variables based on `.env.template`.

### Running:

```
flask run -h 0.0.0.0 --debug
```

Alternatively, set the `FINESSE_BACKEND_DEBUG_MODE` environment variable to 
`True` and run:
```
python run.py
```

### Querying the API:

#### Ailab Search Query

Perform a search query using ailab search:

```
curl -X POST http://localhost:5000/search/ailab --data '{"query": "is e.coli a virus or bacteria?"}' -H "Content-Type: application/json"
```

#### Azure Search Query

Perform a search query using Azure Cognitive Search:

```
curl -X POST http://localhost:5000/search/azure --data '{"query": "search term"}' -H "Content-Type: application/json"
```

#### Static Data Search Query

Perform a search query on static data:

```
curl -X POST http://localhost:5000/search/static --data '{"query": "document name"}' -H "Content-Type: application/json"
```

#### Fetching `finesse-data` Filenames

To fetch a list of filenames from the static data source, use the following command:

```
curl http://localhost:5000/search/static/filenames
```

### JSON Structure Explanation

The JSON response structure for search queries is as follows:

- `id`: The unique identifier for each document.
- `url`: The URL of the document, which should point to inspection.canada.ca.
- `score`: Represents the search score, indicating the relevance of the document to the query.
- `title`: The title of the document.
- `content`: The main content or body of the document.
- `subtitle`: The title or titles extracted from the snippet.
- `last_updated`: The last modified date of the document.
