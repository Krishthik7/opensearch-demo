# OpenSearch Assessment – Ready-to-Run Project

## Prerequisites

- [Docker & Docker Compose](https://www.docker.com/products/docker-desktop)
- [Python 3.7+](https://www.python.org/downloads/)
- Python requests library:  
  Install with `pip install requests`

## Project Structure

```
opensearch-assessment/
│
├── docker-compose.yml               # Runs OpenSearch & Dashboards
├── works-index-mapping.json         # Index mapping with analyzers & synonyms
├── works-sample-data.json           # Sample data to index
├── jungle-hoodie-search-dsl.json    # Example search for "jungle hoodie"
├── init_opensearch.py               # Script to set up index, data, and search
└── README.md                        # This help file
```

## Quickstart

1. **Start OpenSearch and Dashboards:**
   ```sh
   docker compose up -d
   ```
   Wait 2–5 minutes until services are up.

2. **Install Python requests (if needed):**
   ```sh
   pip install requests
   ```
   *(If pip fails, try `pip3` or `python -m pip install requests`)*

3. **Run the setup and search script:**
   ```sh
   python init_opensearch.py
   ```

4. **See your results in the terminal.**

5. **(Optional) Use the Dashboard UI:**  
   Go to [http://localhost:5601](http://localhost:5601) in your browser.

## Troubleshooting

- If you see `OpenSearch Dashboards server is not ready yet`, wait a few minutes and refresh.
- If you see port or memory errors, check Docker is running and has at least 2GB RAM allocated.
- For other issues, check logs:
  ```sh
  docker compose logs opensearch
  docker compose logs opensearch-dashboards
  ```

---

# Explanation and Design Choices

## Token Matching & Synonyms

- Each query token must match at least one of: enabled product name (with synonyms), a title token, or a tag.
- Product name uses a custom analyzer with a synonym filter for flexible matching (e.g., "hoodie" matches "Pullover Hoodie", "pullover", "sweatshirt", etc.).
- Query ensures all tokens are matched somewhere via a `bool` with `must` clauses, each containing a `should` on the three fields.

## Nested Products & Filtering

- Products are modeled as a `nested` array, so enabled filtering and name matching apply to the same product object.
- Query uses a `nested` query with `products.enabled: true`.

## Relevance Scoring

- Default scoring reflects how well and where tokens match.
- Improvement: add boosts so matches in title are scored higher, or add function scoring for product popularity.

## Elasticsearch Techniques

- **Flattened:** Use for large, simple, dynamic objects (e.g., arbitrary user settings).
- **Parent/Child:** Use for independent scalability and updates (e.g., blog posts and comments).
- **Nested:** Use for arrays of objects where relationships between fields must be preserved (e.g., products in a work).

## Improvements

- Add field boosts (e.g., title > tags > products).
- Use multi_match queries for more flexible matching.
- Support fuzzy/partial matches for typos and autocomplete.
- Add popularity or recency as a scoring factor.

## Tools Used

- Docker & Docker Compose
- Python + requests
- VS Code
- OpenSearch Dashboards

## Scaling & Monitoring

- This setup supports millions of docs on decent hardware.
- Monitor: JVM heap, CPU, disk I/O, query latency, cluster health.
- For 1M× scale: increase nodes, shards, use index rollovers.
- For larger docs: increase RAM/heap, consider cold storage.
- For spikes: use load balancers, add coordinator nodes, enable caching.

---