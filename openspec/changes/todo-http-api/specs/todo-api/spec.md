## ADDED Requirements

### Requirement: Todo resource model
The system SHALL persist todos with fields `id` (UUID string), `title`, `completed`, `created_at`, and `updated_at` (RFC 3339 UTC).

#### Scenario: Create assigns server fields
- **WHEN** a client creates a todo with a valid title
- **THEN** the response includes generated `id`, timestamps, and `completed` defaulting to false unless provided

### Requirement: Create todo
The system SHALL expose `POST /todos` returning `201` with the Todo JSON, rejecting empty/whitespace or >200 char titles with `400` `validation_error`.

#### Scenario: Empty title rejected
- **WHEN** title is empty or whitespace
- **THEN** response is `400` with error code `validation_error`

### Requirement: List and filter todos
The system SHALL expose `GET /todos` returning `200` with a JSON array, supporting `?completed=true|false`, and `400` for invalid filter values.

#### Scenario: Filter completed
- **WHEN** client requests `GET /todos?completed=true`
- **THEN** only completed todos are returned

### Requirement: Get patch delete by id
The system SHALL expose `GET|PATCH|DELETE /todos/:id` with `404` `not_found` when missing; PATCH requires at least one field; DELETE returns `204`.

#### Scenario: Missing id
- **WHEN** id does not exist
- **THEN** response is `404` with code `not_found`

### Requirement: Health and config
The system SHALL expose `GET /health` → `200` `{ "status": "ok" }`, bind via `HOST`/`PORT`, and use `DATABASE_URL` (default `sqlite:todos.db`) with sqlx migrations on startup.

#### Scenario: Health check
- **WHEN** client calls `GET /health`
- **THEN** response is `200` with status ok

### Requirement: Error shape
All 4xx/5xx JSON errors SHALL use `{ "error": { "code": "...", "message": "..." } }` with codes including `validation_error`, `not_found`, `internal_error`.

#### Scenario: Error envelope
- **WHEN** a validation failure occurs
- **THEN** body matches the error envelope with `validation_error`
