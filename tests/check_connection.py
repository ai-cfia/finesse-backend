import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from dotenv import load_dotenv

def test_index_existence():
    load_dotenv()
    service_endpoint = os.environ["FINESSE_BACKEND_AZURE_SEARCH_ENDPOINT"]
    expected_index_name = os.environ["FINESSE_BACKEND_AZURE_SEARCH_INDEX_NAME"]
    key = os.environ["FINESSE_BACKEND_AZURE_SEARCH_API_KEY"]

    # Create a SearchIndexClient to manage indexes
    client = SearchIndexClient(service_endpoint, AzureKeyCredential(key))

    try:
        # Fetch and list all indexes
        indexes = client.list_indexes()
        index_names = [index.name for index in indexes]
        if expected_index_name in index_names:
            print(f"Index '{expected_index_name}' exists.")
        else:
            print(f"Index '{expected_index_name}' does not exist.")
    except Exception as e:
        print("Failed to connect or retrieve data:", e)

# Run the test
test_index_existence()
