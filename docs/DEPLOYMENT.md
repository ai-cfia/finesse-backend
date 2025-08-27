# Deployment

**Note on the container**: Create and set the environment variables based on
`.env.template`. Make sure `FINESSE_BACKEND_DEBUG_MODE` is NOT set to `True` in
PRODUCTION builds.

Refer to the [infrastructure repository](https://github.com/ai-cfia/infra) for a
Kubernetes deployment. The secrets (in this case environment variables) are
managed with **Hashicorp Vault**.

---

## Déploiement

**Remarque sur le conteneur**: Créez et définissez les variables d’environnement
en vous basant sur `.env.template`. Assurez-vous que
`FINESSE_BACKEND_DEBUG_MODE` **n'est PAS défini à `True`** dans les builds de
**PRODUCTION**.

Consultez le [dépôt d’infrastructure](https://github.com/ai-cfia/infra) pour un
déploiement Kubernetes. Les secrets (dans ce cas, les variables d’environnement)
sont gérés avec **HashiCorp Vault**.
