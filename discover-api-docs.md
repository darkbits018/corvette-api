# Discover API Documentation

This document provides detailed documentation for the `/api/v1/discover` endpoint.

---

## Flexible Log Search 🛡️

Performs a flexible and powerful search query against OpenSearch to retrieve logs.

-   **Endpoint:** `POST /api/v1/discover/`
-   **Permission:** `can_view_logs`

### Request Body

| Field           | Type          | Description                                                                                                  |
| :-------------- | :------------ | :----------------------------------------------------------------------------------------------------------- |
| `index_pattern` | string        | **Required.** The index pattern to search (e.g., `syslog_logs-*`).                                           |
| `client_id`     | string        | **Required for non-admins.** Filters logs to a specific client.                                              |
| `size`          | integer       | The maximum number of hits to return. Default: `100`.                                                        |
| `from`          | integer       | The starting offset for pagination. Default: `0`.                                                            |
| `time_range`    | object        | An object specifying the time filter with `from` and `to` keys.                                              |
| `query`         | object        | A standard OpenSearch query object (e.g., `{"match_all": {}}` or `{"match": {"message": "error"}}`).         |
| `filters`       | array[object] | A list of dynamic filters to apply. Each object has `field`, `value`, `type` (`term`, `match`), and `operator` (`gte`, `lte`). |
| `sort`          | array[object] | A list of fields to sort by. Each object has `field` and `order` (`asc`, `desc`). Default: `@timestamp` desc. |
| `aggs`          | object        | A standard OpenSearch aggregations object.                                                                   |
| `highlight`     | object        | A standard OpenSearch highlight object.                                                                      |
| `fields`        | array[string] | A list of specific `_source` fields to return. If omitted, the full source is returned.                      |

### Example Advanced Request

```json
{
    "index_pattern": "syslog_logs-*",
    "size": 50,
    "from": 0,
    "time_range": {
        "from": "2025-09-23T00:00:00.000Z",
        "to": "2025-09-23T23:59:59.999Z"
    },
    "query": {
        "match": {
            "message": "timeout"
        }
    },
    "filters": [
        {
            "field": "event_type",
            "value": "system",
            "type": "term"
        }
    ],
    "sort": [
        {
            "field": "@timestamp",
            "order": "desc"
        }
    ],
    "aggs": {
        "event_type_count": {
            "terms": {
                "field": "event_type.keyword"
            }
        }
    },
    "highlight": {
        "fields": {
            "message": {}
        }
    },
    "fields": ["@timestamp", "message", "host", "event_type"]
}
```

### Response Body

The response contains the search results, total count, and any requested aggregations.

-   `hits`: An array of log objects. Each object contains:
    -   `index`: The name of the index the log came from.
    -   `source`: The original log document.
    -   `highlight`: An object containing highlighted snippets if requested.
-   `total`: The total number of documents matching the query.
-   `aggregations`: An object containing the results of any requested aggregations.
