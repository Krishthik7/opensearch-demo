---

## 1. Improvements for the Next Iteration

- **Field Boosting:** Adjust scoring so title or exact product name matches are weighted higher than tag or synonym matches for better relevance.
- **Multi-match Queries:** Use `multi_match` to search across multiple fields more flexibly.
- **Autocomplete & Suggestions:** Add edge n-gram analyzers for fast autocomplete and user search suggestions.
- **Partial/Fuzzy Matching:** Support typo tolerance via fuzzy matching or phonetic analyzers.
- **Product Filtering:** Allow filtering and faceting on product attributes (e.g., stage, type).
- **Index Templates & Aliases:** Use index templates for easier updates and rollovers for zero-downtime migrations.
- **Data Enrichment:** Store derived fields like product counts or popularity to enhance search and ranking.
- **Security:** Re-enable security plugins and use proper authentication for production.
- **Monitoring & Alerting:** Integrate with OpenSearch Dashboards for cluster and query monitoring.

---

## 2. Tools and Utilities Used

- **OpenSearch:** Search engine and analytics backend.
- **Docker & Docker Compose:** For isolated environment and repeatable setup.
- **Python (requests):** For scripting indexing and querying as code.
- **OpenSearch Dashboards:** For visualizing data and managing the cluster.
- **VS Code / Text Editor:** For authoring code and configurations.
- **curl:** For testing HTTP endpoints quickly.

---

## 3. Supported Scale and What to Monitor

**Supported Scale:**  
- With this mapping and setup, you can comfortably support 100K–1M works on a single-node cluster (assuming moderate document size and low QPS).

**What to Monitor:**  
- **Cluster health:** (green/yellow/red), node status.
- **JVM heap usage:** Memory pressure, garbage collection overhead.
- **CPU and disk I/O:** For indexing/search spikes or resource bottlenecks.
- **Query latency and throughput:** In Dashboards or via metrics.
- **Index size and storage utilization.**
- **Slow logs:** For identifying slow queries or index operations.
- **Error logs:** For mapping/index errors or node failures.

**When to Rework:**  
- When JVM heap consistently >80% or GC pauses increase.
- When query latency or error rates rise.
- When disk usage approaches node limits.
- When cluster health degrades or data nodes are regularly overloaded.

---

## 4. Scaling for 1 Million Times More Documents

- **Cluster Sharding:** Increase the number of primary shards and nodes for horizontal scaling.
- **Multiple Data Nodes:** Distribute data across more nodes for parallel indexing and search.
- **Index Rollover:** Use time-based or size-based index patterns (e.g., monthly indices).
- **Query Optimization:** Use filters, avoid deep pagination, and leverage search_after/scroll APIs.
- **Resource Allocation:** Increase RAM, CPU, and disk for each node.

---

## 5. Scaling for 10x Larger Documents

- **Increase Node Resources:** More RAM and disk per node to accommodate bigger documents.
- **Tune JVM Heap:** Set heap to 50% of system RAM (up to 32GB for JVM).
- **Document Modeling:** Consider splitting very large documents or storing large blobs outside OpenSearch (e.g., in object storage).
- **Compression:** Use best-compression codec for indices.
- **Monitor Merge and Refresh Rates:** Large docs can slow segment merges; tune accordingly.

---

## 6. Scaling for Request Spikes

- **Add Coordinator Nodes:** Separate query and indexing traffic from data nodes.
- **Load Balancers:** Use HAProxy, NGINX, or OpenSearch's built-in round-robin for query distribution.
- **Replica Shards:** Increase the number of replicas for higher read throughput and redundancy.
- **Caching:** Tune query and field data caches for hot queries.
- **Autoscaling (Cloud):** Use managed OpenSearch services with autoscaling for bursty workloads.
- **Queueing:** Buffer incoming requests with a message queue or service layer during high spikes.

---

## Evaluation Criteria Summary

- **Great:** Mapping and query ensure every search token is matched as described, with analyzers and synonym support. Explanations are clear and tie back to requirements.
- **Good:** Mapping and query are mostly correct, but may not match on all required fields or tokens. Explanations show strong understanding.
- **Poor:** Key requirements missed—e.g., tokens are not all matched, or mapping/query lacks synonym or nested product support.

---
