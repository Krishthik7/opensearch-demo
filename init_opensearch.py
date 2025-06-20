import requests
import time
from pprint import pprint

OPENSEARCH_URL = "http://localhost:9200"
INDEX_NAME = "works"

# --- 1. Mapping with analyzer and synonym filter
mapping = {
  "settings": {
    "analysis": {
      "filter": {
        "product_synonyms": {
          "type": "synonym",
          "synonyms": [
            "sticker,sticker pack",
            "t-shirt,tee,classic t-shirt",
            "coaster,coasters",
            "clock,timepiece",
            "hoodie,pullover,sweatshirt,Pullover Hoodie"
          ]
        }
      },
      "analyzer": {
        "product_name_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "product_synonyms"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "work_id": { "type": "long" },
      "title": { "type": "text", "analyzer": "standard" },
      "tags": { "type": "text", "analyzer": "standard" },
      "products": {
        "type": "nested",
        "properties": {
          "product_id": { "type": "keyword" },
          "name": { "type": "text", "analyzer": "product_name_analyzer" },
          "stage": { "type": "keyword" },
          "enabled": { "type": "boolean" }
        }
      }
    }
  }
}

# --- 2. Sample data
sample_data = [
  {
    "work_id": 274839,
    "title": "Retro Sticker Collection",
    "tags": ["stickers", "vintage", "fun"],
    "products": [
      { "product_id": "sticker", "name": "sticker", "stage": "Active", "enabled": True },
      { "product_id": "coaster", "name": "coasters", "stage": "Active", "enabled": True }
    ]
  },
  {
    "work_id": 593210,
    "title": "Clockwork Jungle",
    "tags": ["clock", "jungle", "time"],
    "products": [
      { "product_id": "clock", "name": "clock", "stage": "Active", "enabled": True },
      { "product_id": "tshirt", "name": "classic t-shirt", "stage": "Active", "enabled": True },
      { "product_id": "hoodie", "name": "Pullover Hoodie", "stage": "Active", "enabled": True }
    ]
  },
  {
    "work_id": 862147,
    "title": "Monochrome Tee Drop",
    "tags": ["fashion", "shirt", "minimal"],
    "products": [
      { "product_id": "tshirt", "name": "classic t-shirt", "stage": "Active", "enabled": True },
      { "product_id": "sticker", "name": "sticker", "stage": "Active", "enabled": True },
      { "product_id": "hoodie", "name": "Pullover Hoodie", "stage": "Active", "enabled": True }
    ]
  }
]

# --- 3. Query DSL for "jungle hoodie"
def build_query(tokens):
    # Each token must match at least one of (enabled product name with synonyms, title, tags)
    must = []
    for token in tokens:
        should = [
            {
                "nested": {
                    "path": "products",
                    "query": {
                        "bool": {
                            "must": [
                                { "term": { "products.enabled": True } },
                                { "match": { "products.name": token } }
                            ]
                        }
                    }
                }
            },
            { "match": { "title": token } },
            { "match": { "tags": token } }
        ]
        must.append({
            "bool": {
                "should": should,
                "minimum_should_match": 1
            }
        })
    return {
        "query": {
            "bool": {
                "must": must
            }
        }
    }

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
    tokens = ["jungle", "hoodie"]
    query = build_query(tokens)
    r = requests.get(f"{OPENSEARCH_URL}/{INDEX_NAME}/_search", json=query)
    print("\n--- Search Results for 'jungle hoodie' ---")
    pprint(r.json())

if __name__ == "__main__":
    main()