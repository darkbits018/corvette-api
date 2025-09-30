# SC-SIEM-Corvette API

---

# API Documentation

This document provides details on the available API endpoints for the SIEM application.

## Authentication

Endpoints that require authentication and specific permissions are marked with a "shield" icon (🛡️). Requests to these endpoints must include a valid JWT in the `Authorization` header:

`Authorization: Bearer <your_jwt_token>`

---

# Development & Testing

## Swagger UI

FastAPI provides automatic interactive API documentation. Once the server is running, you can access it at:

-   [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Postman Collection

A Postman collection is available for testing the API endpoints. You can import it using the following link:

-   [Import Postman Collection](https://documenter.getpostman.com/view/39324004/2sB3QDvCWm)

---

## Authentication API

Base Path: `/api/v1/auth`

### 1. User Login

Authenticates a user via username and password and returns an access and refresh token pair.

-   **Endpoint:** `POST /login`
-   **Request Body:** `application/x-www-form-urlencoded`
    -   `username`: The user's username.
    -   `password`: The user's password.

#### Response Body

```json
{
  "access_token": "string",
  "refresh_token": "string",
  "token_type": "bearer"
}
```

### 2. Refresh Access Token 🛡️

Takes a valid refresh token and returns a new access and refresh token pair. The refresh token must be sent as a Bearer token in the `Authorization` header.

-   **Endpoint:** `POST /refresh`
-   **Permission:** Requires a valid refresh token.

#### Response Body

```json
{
  "access_token": "string",
  "refresh_token": "string",
  "token_type": "bearer"
}
```

---

## Users API

Base Path: `/api/v1/users`

### 1. Create User 🛡️

Creates a new user in the database.

-   **Endpoint:** `POST /`
-   **Permission:** `can_manage_users`

#### Request Body

| Field       | Type   | Description                                |
| :---------- | :----- | :----------------------------------------- |
| `username`  | string | **Required.** A unique username.           |
| `email`     | string | **Required.** A unique email address.      |
| `password`  | string | **Required.** The user's password.         |
| `role`      | string | **Required.** The name of an existing role. |
| `client_id` | string | An optional client identifier.             |

#### Responses

-   **`201 Created`**: The user was successfully created.
-   **`409 Conflict`**: The username or email already exists.
-   **`404 Not Found`**: The specified role does not exist.

### 2. Get All Users 🛡️

Retrieves a list of all users.

-   **Endpoint:** `GET /`
-   **Permission:** `can_manage_users`

#### Response Body

Returns a JSON array of user objects.

```json
[
  {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "is_active": true,
    "role": {
      "id": 1,
      "name": "Administrator",
      "description": "Full access to all features.",
      "permissions": { "can_manage_users": true, "can_view_logs": true }
    },
    "client_id": null
  }
]
```

---

## Roles API

Base Path: `/api/v1/roles`

### 1. Create Role 🛡️

Creates a new role.

-   **Endpoint:** `POST /`
-   **Permission:** `can_manage_roles`

#### Request Body

| Field         | Type    | Description                                      |
| :------------ | :------ | :----------------------------------------------- |
| `name`        | string  | **Required.** A unique name for the role.        |
| `description` | string  | A description of the role.                       |
| `permissions` | object  | A dictionary of permission names and boolean values. |

##### Example Request

```json
{
  "name": "Analyst",
  "description": "Can view logs and dashboards.",
  "permissions": {
    "can_view_logs": true,
    "can_manage_indices": false
  }
}
```

#### Responses

-   **`201 Created`**: The role was successfully created.
-   **`409 Conflict`**: A role with that name already exists.

### 2. Get All Roles

Retrieves a list of all roles.

-   **Endpoint:** `GET /`

#### Response Body

Returns a JSON array of role objects.

```json
[
  {
    "id": 1,
    "name": "Administrator",
    "description": "Full access to all features.",
    "permissions": { "can_manage_users": true, "can_view_logs": true }
  }
]
```

### 3. Get All Permissions

Returns a list of all available permission strings in the system.

-   **Endpoint:** `GET /permissions`

#### Response Body

```json
[
  "can_manage_users",
  "can_manage_roles",
  "can_view_logs",
  "can_manage_indices"
]
```

---

## Discover API

Base Path: `/api/v1/discover`

### 1. Flexible Log Search 🛡️

Performs a flexible and powerful search query against OpenSearch to retrieve logs.

-   **Endpoint:** `POST /`
-   **Permission:** `can_view_logs`

#### Request Body

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

#### Response Body

-   `hits`: An array of log objects.
-   `total`: The total number of documents matching the query.
-   `aggregations`: The results of any requested aggregations.

---

## Templates API

Base Path: `/api/v1`

Provides endpoints for managing OpenSearch index templates.

### 1. Create or Update an Index Template 🛡️

-   **Endpoint:** `POST /templates/{name}`
-   **Permission:** `can_manage_indices`

### 2. Get an Index Template 🛡️

-   **Endpoint:** `GET /templates/{name}`
-   **Permission:** `can_manage_indices`

### 3. Delete an Index Template 🛡️

-   **Endpoint:** `DELETE /templates/{name}`
-   **Permission:** `can_manage_indices`

### 4. Check if an Index Template Exists 🛡️

-   **Endpoint:** `HEAD /templates/{name}`
-   **Permission:** `can_manage_indices`

---

## Indices API

Base Path: `/api/v1/indices`

Provides endpoints for managing OpenSearch indices.

### 1. Create Index 🛡️

Creates a new OpenSearch index. Can be created with specific settings and mappings, or can be based on an existing index template.

-   **Endpoint:** `POST /`
-   **Permission:** `can_manage_indices`

#### Request Body

| Field           | Type   | Description                                                                                              |
| :-------------- | :----- | :------------------------------------------------------------------------------------------------------- |
| `index_name`    | string | **Required.** The name of the index to create.                                                           |
| `template_name` | string | *Optional.* The name of an index template to use. If provided, `settings` and `mappings` will be ignored. |
| `settings`      | object | *Optional.* A standard OpenSearch index settings object.                                                 |
| `mappings`      | object | *Optional.* A standard OpenSearch index mappings object.                                                 |

##### Example 1: Create with specific settings

```json
{
  "index_name": "my_custom_index",
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "message": { "type": "text" }
    }
  }
}
```

##### Example 2: Create using a template

```json
{
  "index_name": "my_templated_index",
  "template_name": "my_log_template"
}
```

#### Responses

-   **`201 Created`**: The index was successfully created.
-   **`400 Bad Request`**: An error occurred (e.g., index already exists).

### 2. Get All Indices 🛡️

Retrieves a list and details of all indices in the cluster.

-   **Endpoint:** `GET /`
-   **Permission:** `can_manage_indices`

#### Response Body

Returns a dictionary where keys are index names and values are their corresponding settings and mappings.

### 3. Get Specific Index 🛡️

Retrieves details for a specific index.

-   **Endpoint:** `GET /{index_name}`
-   **Permission:** `can_manage_indices`

#### Response Body

Returns a dictionary containing the settings and mappings for the requested index.

### 4. Delete Index 🛡️

Deletes a specific index.

-   **Endpoint:** `DELETE /{index_name}`
-   **Permission:** `can_manage_indices`

#### Responses

-   **`200 OK`**: The index was successfully deleted.
-   **`400 Bad Request`**: An error occurred (e.g., index not found).
