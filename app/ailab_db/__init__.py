from ailab.db import connect_db
from ailab.db.api import search_from_text_query


def ailab_db_search(query):
    with connect_db().cursor() as cursor:
        return search_from_text_query(cursor, query)
