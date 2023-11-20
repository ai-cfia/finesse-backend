import logging

from app.config import AzureSearchConfig


class AzureSearchQueryError(Exception):
    """Raised when the search operation fails."""


class EmptyQueryError(Exception):
    """Raised when the search query is empty."""


def azure_search_documents(query, config: AzureSearchConfig):
    if not query:
        logging.error("Empty search query received")
        raise EmptyQueryError("Search query cannot be empty")
    try:
        results = config.client.search(search_text=query)
        return [dict(result) for result in results]
    except Exception as e:
        logging.error(f"Search operation failed: {e}", exc_info=True)
        raise AzureSearchQueryError from e
