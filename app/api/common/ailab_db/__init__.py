import logging

from ailab.db import DBError, connect_db
from ailab.db.api import match_documents_from_text_query


class AilabDbSearchException(DBError):
    """Custom exception for errors in searching from ailab-db."""


class EmptyQueryError(DBError):
    "Raised when the search query is empty."


def ailab_db_search(query):
    if not query:
        logging.error("Empty search query received")
        raise EmptyQueryError("Search query cannot be empty")

    try:
        with connect_db().cursor() as cursor:
            return match_documents_from_text_query(cursor, query)
    # TODO: handle specific exceptions
    except Exception as e:
        logging.error(f"finesse-data fetch failed: {e}", exc_info=True)
        raise AilabDbSearchException(f"finesse-data fetch failed: {e}") from e
