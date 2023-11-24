# Deployment

## Azure
Create and set the environment variables based on `.env.template`. Make sure `FINESSE_BACKEND_DEBUG_MODE` is not set to `True`.

Build (do this from your WSL Ubuntu where Docker is already installed):

```
docker build -t finesse-backend .
```

test locally:

```
docker run -p 5000:5000 -e PORT=5000 finesse-backend
```
