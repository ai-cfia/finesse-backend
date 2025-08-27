# Running and testing the API locally

([*Le français est disponible au bas de la
page*](#exécuter-et-tester-lapi-localement))

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

### Docker-compose (optional)

You can also use `docker-compose` to run the API with the client. The client is
the web interface that makes use of the API and is available at
<https://github.com/ai-cfia/finesse-frontend>.

To run the API and the client together, you can use the following command:

```bash
docker-compose up --build
```

You can then access the client at `http://localhost`.

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

---

## Exécuter et tester l'API localement

## Avec votre environnement local

Créez et définissez les variables d'environnement en vous basant sur
`.env.template`. Vous devrez créer un fichier `.env`.

### Exécution

```bash
flask run -h 0.0.0.0 --debug
```

Sinon, définissez la variable d'environnement `FINESSE_BACKEND_DEBUG_MODE` à
`True` et exécutez :

```bash
python run.py
```

## Avec Docker

Créez et définissez les variables d'environnement en vous basant sur
`.env.template`. Vous devrez créer un fichier `.env`.

Construisez le conteneur :

```bash
docker build -t finesse-backend .
```

Déployez le conteneur localement :

```bash
docker run -p 5000:5000 -e PORT=5000 --env-file .env finesse-backend
```

### Docker-compose (optionnel)

Vous pouvez également utiliser docker-compose pour exécuter l'API avec le
client. Le client est l'interface web qui utilise l'API et est disponible sur
<https://github.com/ai-cfia/finesse-frontend>.

Pour exécuter l'API et le client ensemble, utilisez la commande suivante :

```bash
docker-compose up --build
```

Vous pourrez ensuite accéder au client à l'adresse `http://localhost`.

## Vérifiez si l'API fonctionne correctement

### Testez le chemin : `/search/static`

```bash
curl -X POST http://localhost:5000/search/static --data '{"query": "is e.coli a virus or bacteria?"}' -H "Content-Type: application/json"
```

### Testez le chemin : `/search/azure`

```bash
curl -X POST "http://localhost:5000/search/azure?top=10&skip=0" --data '{"query": "is e.coli a virus or bacteria?"}' -H "Content-Type: application/json"
```

- `top`  (optionnel) : Nombre de résultats de recherche à retourner.
- `skip` (optionnel) : Nombre de résultats de recherche à ignorer depuis le
  début.

### Testez le chemin : `/search/llamaindex`

```bash
curl -X POST "http://localhost:5000/search/llamaindex?top=10" --data '{"query": "is e.coli a virus or bacteria?"}' -H "Content-Type: application/json"
```

- `top` (optionnel) : Nombre de résultats de recherche à retourner.

### Explication de la structure JSON

- **id** : L'identifiant unique de chaque document.
- **url** : L'URL du document, qui doit pointer vers inspection.canada.ca.
- **score** : Représente le score de recherche, indiquant la pertinence du
  document par rapport à la requête.
- **title** : Le titre du document.
- **content** : Le contenu principal ou le corps du document.
- **subtitle** : Le ou les sous-titres extraits du snippet.
- **last_updated** : La dernière date de modification du document.
