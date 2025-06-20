import requests
import time
from pprint import pprint

OPENSEARCH_URL = "http://localhost:9200"
INDEX_NAME = "works"

def load_json(filename):
    import json
    with open(filename, "r") as f:
        return json.load(f)

def wait_for_opensearch():
    for _ in range(30):
        try:
            if requests.get(OPENSEARCH_URL).status_code == 200:
                print("OpenSearch is up!")
                return
        except Exception:
            pass
        time.sleep(2)
    raise Exception("OpenSearch did not start in time")

def main():
    wait_for_opensearch()
    mapping = load_json("works-index-mapping.json")
    sample_data = load_json("works-sample-data.json")
    search_dsl = load_json("jungle-hoodie-search-dsl.json")

    # Delete index if exists
    requests.delete(f"{OPENSEARCH_URL}/{INDEX_NAME}")

    # Create index
    r = requests.put(f"{OPENSEARCH_URL}/{INDEX_NAME}", json=mapping)
    print("Index creation:", r.status_code, r.text)

    # Index sample data
    for doc in sample_data:
        doc_id = doc["work_id"]
        r = requests.put(f"{OPENSEARCH_URL}/{INDEX_NAME}/_doc/{doc_id}", json=doc)
        print(f"Indexed work_id={doc_id}: {r.status_code}")

    time.sleep(2)  # Wait for indexing

    # Search for "jungle hoodie"
    r = requests.get(f"{OPENSEARCH_URL}/{INDEX_NAME}/_search", json=search_dsl)
    print("\n--- Search Results for 'jungle hoodie' ---")
    pprint(r.json())

if __name__ == "__main__":
    main()