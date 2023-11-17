import logging

from app.config import AzureSearchConfig


class AzureSearchQueryError(Exception):
    """Raised when the search operation fails."""


def azure_search_documents(query, config: AzureSearchConfig):
    if not query:
        logging.warning("Empty search query received")
        return []
    try:
        results = config.client.search(search_text=query)
        return [dict(result) for result in results]
    except Exception as e:
        logging.error(f"Search operation failed: {e}", exc_info=True)
        raise AzureSearchQueryError from e
