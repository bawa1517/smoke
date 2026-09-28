# RESUME — FastAPI contract design (parked demo)

## What this work is

This was a demo interview about designing an HTTP contract for the Taskwell browser app. The user asked to leave the demo task parked. The decisions below are retained as a record; they are not an instruction to implement the API.

## Settled so far

- The proposed API serves the Taskwell browser UI for one local user without authentication, from the same origin and bound to loopback only.
- The proposed `Task` has `id`, `text`, and `completed`. Clients provide positive integer IDs; IDs are immutable. Text is trimmed and limited to 1–100 Unicode code points. Unknown fields, null values, and empty PATCH bodies are rejected.
- The proposed routes are `GET /tasks`, `POST /tasks`, and `GET`, `PATCH`, and `DELETE /tasks/{task_id}`. Listing returns all tasks newest first by server-recorded creation time, without pagination or filters. PATCH accepts either or both `text` and `completed`. Create accepts optional `completed`, defaulting to `false`.
- Duplicate existing IDs return `409` without changing the existing task; deleted IDs may be reused. Missing tasks return `404`; invalid input uses FastAPI’s `422`. Successful CRUD operations return `200` with Task objects, including the deleted Task. Domain error messages are stable human-readable details.
- The proposed storage is local SQLite with persistence across restarts. A clean install starts empty; existing browser `localStorage` data remains unused. The requested deliverable was OpenAPI YAML version `1.0.0`.

## Next action

None. The user said this was a demo task and asked to leave it. No OpenAPI YAML or FastAPI code was created. Resume only if the user explicitly asks to continue this contract as project work.

## Cost estimate

The interview and context updates took approximately 24 tool calls; token count unavailable. No tests or app commands were run, and no contract artifact was produced.
