## Purpose

Provide a local HTTP API that persists todos in SQLite and exposes CRUD operations plus a completion-status filter, for a single-process client to manage a todo list over JSON/HTTP.

## ADDED Requirements

### Requirement: Create a todo
The system SHALL accept `POST /todos` with a JSON body `{ "title": string, "completed"?: boolean }` and create a new todo with a server-generated UUID `id`, server-set `created_at`/`updated_at` RFC 3339 UTC timestamps, and `completed` defaulting to `false` when omitted.

#### Scenario: Successful creation
- **WHEN** a client POSTs `{ "title": "Buy milk" }` to `/todos`
- **THEN** the server responds `201` with the full Todo JSON, including a generated `id`, `completed: false`, and `created_at`/`updated_at` set

#### Scenario: Empty or whitespace-only title rejected
- **WHEN** a client POSTs a title that is empty or whitespace-only
- **THEN** the server responds `400` with the standard error shape and code `validation_error`

#### Scenario: Overlong title rejected
- **WHEN** a client POSTs a title longer than 200 characters
- **THEN** the server responds `400` with the standard error shape and code `validation_error`

### Requirement: List todos with optional completion filter
The system SHALL accept `GET /todos` with an optional `completed` query parameter (`true` or `false`) and return a JSON array of todos, filtered by completion status when the parameter is present.

#### Scenario: List all todos
- **WHEN** a client GETs `/todos` with no query parameters
- **THEN** the server responds `200` with a JSON array of all todos (an empty array is a valid response)

#### Scenario: List filtered by completion status
- **WHEN** a client GETs `/todos?completed=true`
- **THEN** the server responds `200` with a JSON array containing only todos where `completed` is `true`

#### Scenario: Invalid completed value rejected
- **WHEN** a client GETs `/todos?completed=notabool`
- **THEN** the server responds `400` with the standard error shape and code `validation_error`

### Requirement: Get a single todo
The system SHALL accept `GET /todos/:id` and return the matching todo, or a `404` if no todo exists with that id.

#### Scenario: Successful get
- **WHEN** a client GETs `/todos/:id` for an existing todo
- **THEN** the server responds `200` with the Todo JSON

#### Scenario: Todo not found
- **WHEN** a client GETs `/todos/:id` for an id that does not exist
- **THEN** the server responds `404` with the standard error shape and code `not_found`

### Requirement: Update a todo
The system SHALL accept `PATCH /todos/:id` with a JSON body containing any subset of `{ "title"?: string, "completed"?: boolean }`, requiring at least one field, applying the same title validation rules as creation, and updating `updated_at` on every successful update.

#### Scenario: Successful partial update
- **WHEN** a client PATCHes `/todos/:id` with `{ "completed": true }` for an existing todo
- **THEN** the server responds `200` with the updated Todo JSON, with `updated_at` refreshed and other fields unchanged

#### Scenario: Empty PATCH body rejected
- **WHEN** a client PATCHes `/todos/:id` with an empty JSON body `{}`
- **THEN** the server responds `400` with the standard error shape and code `validation_error`

#### Scenario: Invalid title on update rejected
- **WHEN** a client PATCHes `/todos/:id` with an empty, whitespace-only, or overlong `title`
- **THEN** the server responds `400` with the standard error shape and code `validation_error`

#### Scenario: Todo not found on update
- **WHEN** a client PATCHes `/todos/:id` for an id that does not exist
- **THEN** the server responds `404` with the standard error shape and code `not_found`

### Requirement: Delete a todo
The system SHALL accept `DELETE /todos/:id`, removing the todo and responding with an empty `204` body, or a `404` if no todo exists with that id.

#### Scenario: Successful delete
- **WHEN** a client DELETEs `/todos/:id` for an existing todo
- **THEN** the server responds `204` with an empty body and the todo no longer appears in subsequent list/get calls

#### Scenario: Todo not found on delete
- **WHEN** a client DELETEs `/todos/:id` for an id that does not exist
- **THEN** the server responds `404` with the standard error shape and code `not_found`

### Requirement: Standard error shape
The system SHALL return all 4xx/5xx responses as JSON in the shape `{ "error": { "code": "string_snake_case", "message": "human readable" } }`, using at minimum the codes `validation_error`, `not_found`, and `internal_error`.

#### Scenario: Error response shape
- **WHEN** any request fails validation, lookup, or processing
- **THEN** the response body matches `{ "error": { "code": <snake_case string>, "message": <string> } }` with an appropriate HTTP status

### Requirement: SQLite persistence
The system SHALL persist todos in SQLite, applying schema migrations automatically on startup, with the database location configurable via the `DATABASE_URL` environment variable (default `sqlite:todos.db`), sufficient for concurrent-safe single-process local use.

#### Scenario: Startup applies migrations
- **WHEN** the server starts against a fresh SQLite file
- **THEN** the required schema is created automatically before the server accepts requests

#### Scenario: Configurable database location
- **WHEN** `DATABASE_URL` is set to a custom SQLite path
- **THEN** the server persists and reads todos from that path instead of the default

### Requirement: Server configuration and health check
The system SHALL bind to a configurable `HOST` (default `127.0.0.1`) and `PORT` (default `8080`), and SHALL expose `GET /health` returning `200` with `{ "status": "ok" }`.

#### Scenario: Health check
- **WHEN** a client GETs `/health`
- **THEN** the server responds `200` with `{ "status": "ok" }`

#### Scenario: Default bind address
- **WHEN** the server starts without `HOST`/`PORT` set
- **THEN** it binds to `127.0.0.1:8080`
