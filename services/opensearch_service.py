# sc-siem-corvette/services/opensearch_service.py
import os
from opensearchpy import OpenSearch, NotFoundError
from fastapi import HTTPException, status
from schemas.discover import DiscoverRequest, DiscoverResponse, Hit

# --- OpenSearch Connection ---
OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST", "localhost")
OPENSEARCH_PORT = int(os.getenv("OPENSEARCH_PORT", 9200))
OPENSEARCH_USER = os.getenv("OPENSEARCH_USER", "admin")
OPENSEARCH_PASSWORD = os.getenv("OPENSEARCH_PASSWORD", "T-3:^otm!")

try:
    client = OpenSearch(
        hosts=[{'host': OPENSEARCH_HOST, 'port': OPENSEARCH_PORT}],
        http_auth=(OPENSEARCH_USER, OPENSEARCH_PASSWORD),
        use_ssl=False,
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False,
    )
    if not client.ping():
        raise ConnectionError("Could not connect to OpenSearch")
except Exception as e:
    print(f"ERROR: Could not initialize OpenSearch client: {e}")
    client = None

def build_opensearch_query(request: DiscoverRequest) -> dict:
    """Builds a flexible OpenSearch query DSL from the discover request."""
    query_filters = []

    if request.time_range:
        query_filters.append({
            "range": {
                "@timestamp": {
                    "gte": request.time_range.from_,
                    "lte": request.time_range.to,
                    "format": "strict_date_optional_time||epoch_millis"
                }
            }
        })

    if request.client_id:
        query_filters.append({"term": {"client_id.keyword": request.client_id}})

    if request.filters:
        for f in request.filters:
            if f.type == "term":
                query_filters.append({"term": {f"{f.field}.keyword": f.value}})
            elif f.type == "match":
                query_filters.append({"match": {f.field: f.value}})
            elif f.type == "range" and f.operator:
                query_filters.append({"range": {f.field: {f.operator: f.value}}})

    query_body = {
        "query": {
            "bool": {
                "must": request.query,
                "filter": query_filters
            }
        },
        "size": request.size,
        "from": request.from_
    }

    if request.sort:
        query_body["sort"] = [{opt.field: {"order": opt.order}} for opt in request.sort]
    else:
        query_body["sort"] = [{"@timestamp": {"order": "desc"}}]

    if request.fields:
        query_body["_source"] = request.fields

    if request.aggregations:
        query_body["aggs"] = request.aggregations

    if request.highlight:
        query_body["highlight"] = request.highlight

    return query_body

async def fetch_logs(request: DiscoverRequest) -> DiscoverResponse:
    """Executes the search query against OpenSearch and returns the results."""
    if not client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OpenSearch service is not available"
        )

    query = build_opensearch_query(request)

    try:
        response = client.search(
            index=request.index_pattern,
            body=query
        )
        
        # ** THE FIX **
        # Populate the Hit model using the new field names (index, source)
        # from the OpenSearch response keys (_index, _source).
        hits = [Hit(index=hit['_index'], source=hit['_source'], highlight=hit.get('highlight', {}))
                for hit in response['hits']['hits']]
        total = response['hits']['total']['value']
        aggregations = response.get('aggregations', {})

        return DiscoverResponse(hits=hits, total=total, aggregations=aggregations)

    except NotFoundError:
        return DiscoverResponse(hits=[], total=0, aggregations={})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"An error occurred while querying OpenSearch: {e}"
        )

# --- Template Management ---

async def create_index_template(name: str, template: dict):
    """Creates or updates an index template."""
    if not client:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="OpenSearch not available")
    try:
        return client.indices.put_template(name=name, body=template)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

async def get_index_template(name: str):
    """Gets an index template."""
    if not client:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="OpenSearch not available")
    try:
        return client.indices.get_template(name=name)
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

async def delete_index_template(name: str):
    """Deletes an index template."""
    if not client:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="OpenSearch not available")
    try:
        return client.indices.delete_template(name=name)
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

async def index_template_exists(name: str):
    """Checks if an index template exists."""
    if not client:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="OpenSearch not available")
    try:
        return client.indices.exists_template(name=name)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
