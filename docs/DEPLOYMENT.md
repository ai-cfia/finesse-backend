# Deployment

## Azure
Create and set the environment variables based on `.env.template`. Make sure 
`FINESSE_BACKEND_DEBUG_MODE` is not set to `True`.

Build (do this from your WSL Ubuntu where Docker is already installed):

```
docker build -t finesse-backend .
```

test locally:

```
export PORT=<your_port_here>
docker run -p $PORT:$PORT -e PORT=$PORT --env-file .env finesse-backend
```
