## Purpose

Defines HTTP behavior for a local Todo API resolved from the ambiguous ticket: CRUD, completion filter, health check, SQLite persistence, and a shared JSON error envelope for clients and integration tests.

## ADDED Requirements

### Requirement: Todo resource model
The system SHALL represent each todo with `id` (server-generated UUID string), `title` (string), `completed` (boolean), `created_at` (RFC 3339 UTC), and `updated_at` (RFC 3339 UTC). On create, `completed` MUST default to `false` when omitted; `created_at` and `updated_at` MUST be set by the server. On every successful PATCH, `updated_at` MUST be refreshed by the server.

#### Scenario: Create assigns server fields
- **WHEN** a client creates a todo with a valid title and omits `completed`
- **THEN** the response includes a generated UUID `id`, `completed` false, and server-set `created_at` and `updated_at` in RFC 3339 UTC

### Requirement: Create todo
The system SHALL expose `POST /todos` accepting JSON `{ "title": string, "completed"?: boolean }`. Success MUST return `201` with the full Todo JSON. Empty, whitespace-only, or titles longer than 200 characters MUST return `400` with code `validation_error`. Title MUST be trimmed before length validation and persistence.

#### Scenario: Valid create
- **WHEN** a client posts a title of length 1..=200 after trim
- **THEN** the response is `201` with the full Todo JSON

#### Scenario: Empty title rejected
- **WHEN** title is empty or whitespace-only
- **THEN** the response is `400` with error code `validation_error`

#### Scenario: Overlong title rejected
- **WHEN** title length after trim exceeds 200
- **THEN** the response is `400` with error code `validation_error`

### Requirement: List and filter todos
The system SHALL expose `GET /todos` returning `200` with a JSON array of Todos (empty array allowed). Optional query `completed=true` or `completed=false` MUST filter results. Any other `completed` value MUST return `400` with code `validation_error`.

#### Scenario: List all
- **WHEN** a client calls `GET /todos` with no filter
- **THEN** the response is `200` with a JSON array of all todos

#### Scenario: Filter completed
- **WHEN** a client requests `GET /todos?completed=true`
- **THEN** only todos with `completed` true are returned

#### Scenario: Invalid completed query
- **WHEN** `completed` is present and not exactly `true` or `false`
- **THEN** the response is `400` with code `validation_error`

### Requirement: Get todo by id
The system SHALL expose `GET /todos/:id` returning `200` with the Todo JSON when found, and `404` with code `not_found` when missing.

#### Scenario: Get existing
- **WHEN** the id exists
- **THEN** the response is `200` with that Todo

#### Scenario: Get missing
- **WHEN** the id does not exist
- **THEN** the response is `404` with code `not_found`

### Requirement: Patch todo by id
The system SHALL expose `PATCH /todos/:id` accepting any non-empty subset of `{ "title"?: string, "completed"?: boolean }`. An empty body or body with no updatable fields MUST return `400` with code `validation_error`. When `title` is present, the same trim and 1..=200 rules as create MUST apply. Success MUST return `200` with the updated Todo. Missing id MUST return `404` with code `not_found`.

#### Scenario: Patch success
- **WHEN** the id exists and at least one valid field is provided
- **THEN** the response is `200` with the updated Todo and refreshed `updated_at`

#### Scenario: Empty patch body
- **WHEN** the PATCH body is empty or has no fields
- **THEN** the response is `400` with code `validation_error`

#### Scenario: Patch missing
- **WHEN** the id does not exist
- **THEN** the response is `404` with code `not_found`

### Requirement: Delete todo by id
The system SHALL expose `DELETE /todos/:id` returning `204` with an empty body when the todo is deleted, and `404` with code `not_found` when missing.

#### Scenario: Delete success
- **WHEN** the id exists
- **THEN** the response is `204` with an empty body

#### Scenario: Delete missing
- **WHEN** the id does not exist
- **THEN** the response is `404` with code `not_found`

### Requirement: Health and configuration
The system SHALL expose `GET /health` returning `200` with `{ "status": "ok" }`. The server MUST bind using `HOST` (default `127.0.0.1`) and `PORT` (default `8080`). Persistence MUST use SQLite via `DATABASE_URL` (default `sqlite:todos.db`) with schema applied through sqlx migrations on startup. Concurrency MUST be safe for local single-process use.

#### Scenario: Health check
- **WHEN** a client calls `GET /health`
- **THEN** the response is `200` with `{ "status": "ok" }`

### Requirement: Error shape
All 4xx/5xx JSON responses MUST use `{ "error": { "code": "string_snake_case", "message": "human readable" } }`. Required codes at minimum: `validation_error`, `not_found`, `internal_error`.

#### Scenario: Validation error envelope
- **WHEN** a validation failure occurs
- **THEN** the body matches the error envelope with code `validation_error`

#### Scenario: Not found envelope
- **WHEN** a resource is missing
- **THEN** the body matches the error envelope with code `not_found`

### Requirement: Integration test coverage
A complete implementation MUST include in-process HTTP integration tests covering create, list, list filter, get, patch, delete; validation for empty title, overlong title, empty PATCH body, and bad `completed` query; and 404 paths for get, patch, and delete.

#### Scenario: Required suite present
- **WHEN** `cargo test` is run after implementation
- **THEN** the suite exercises CRUD, filter, validation, and 404 behaviors above

### Requirement: Out of scope
The system SHALL NOT require authentication, multi-tenant isolation, pagination, sorting, UI, OpenAPI artifact generation, or deployment packaging beyond a local binary for v1.

#### Scenario: No auth required
- **WHEN** a client calls any todo endpoint without credentials
- **THEN** requests are processed without auth checks (local single-user use)
