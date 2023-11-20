import logging

from app.config import AzureSearchConfig


class AzureSearchQueryError(Exception):
    """Raised when the search operation fails."""


class EmptyQueryError(Exception):
    """Raised when the search query is empty."""


def transform_result(result):
    return {
        "id": result.get("id"),
        "url": result.get("url"),
        "score": result.get("@search.score"),
        "title": result.get("title"),
        "content": result.get("content"),
        "subtitle": result.get("subtitle"),
        "last_updated": result.get("metadata_last_modified"),
    }


def azure_search_documents(query, config: AzureSearchConfig):
    if not query:
        logging.error("Empty search query received")
        raise EmptyQueryError("Search query cannot be empty")
    try:
        search_results = config.client.search(search_text=query)
        transformed_results = [transform_result(result) for result in search_results]
        return transformed_results
    except Exception as e:
        logging.error(f"Search operation failed: {e}", exc_info=True)
        raise AzureSearchQueryError from e
