# Deployment

Note on the container: Create and set the environment variables based on
`.env.template`. Make sure `FINESSE_BACKEND_DEBUG_MODE` is NOT set to `True` in
PRODUCTION builds.

Refer to the [infrastructure repository](https://github.com/ai-cfia/infra) for a
Kubernetes deployment. The secrets (in this case environment variables) are
managed with Hashicorp Vault.
