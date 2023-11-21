# Deployment

## Azure
Edit configurations

* .env.prod: your .env for your container

Build (do this from your WSL Ubuntu where Docker is already installed):

```
docker build -t finesse-backend .
```

test locally:

```
docker run -p 5000:5000 -e PORT=5000 finesse-backend
```
