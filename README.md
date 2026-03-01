# Cinema Ticket Reservation API

A Django REST Framework project for managing cinema guests, movies, and reservations.  
The repository also demonstrates multiple DRF styles side by side (FBV, CBV, mixins, generics, and viewsets).

## Stack

- Python 3
- Django 5.2.7
- Django REST Framework 3.16.1
- SQLite (default)
- DRF Token Authentication

## Features

- CRUD APIs for `Guest`, `Movie`, and `Reservation`
- Search movies by title on the viewset endpoint
- Custom reservation creation endpoint from movie + guest details
- Token issuance for users (`rest_framework.authtoken`)
- Object-level permission example on `Post` (`author` can edit/delete)

## Data Models

- `Guest`: `name`, `mobile`
- `Movie`: `hall`, `movie`
- `Reservation`: `guest` (FK), `movie` (FK)
- `Post`: `author` (FK to user), `title`, `body`

## Setup

1. Clone and enter the project directory.
2. Create and activate a virtual environment.
3. Install dependencies.
4. Apply migrations.
5. Run the server.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

API base URL:

```text
http://127.0.0.1:8000/
```

## Authentication

This project includes token auth via:

```text
POST /api-token-auth
```

Example:

```bash
curl -X POST http://127.0.0.1:8000/api-token-auth \
  -H "Content-Type: application/json" \
  -d '{"username":"your_username","password":"your_password"}'
```

If the credentials are valid, the response includes:

```json
{"token":"<your-token>"}
```

Use the token for protected endpoints:

```bash
curl http://127.0.0.1:8000/rest/generics/ \
  -H "Authorization: Token <your-token>"
```

Note: A token is auto-created when a new user is created (signal in `tickets/models.py`).

## API Endpoints

### Non-DRF JSON examples

- `GET /django/jsonresponse_no_model/`
- `GET /django/jsonresponse_from_model/`

### Function-Based Views

- `GET, POST /rest/fbvlist/`
- `GET, PUT, DELETE /rest/fbvpk/<int:pk>`
- `GET /fbv/findmovie/`
- `POST /fbv/newreservation`

### Class-Based Views

- `GET, POST /rest/cbv/`
- `GET, PUT, DELETE /rest/cbv/<int:pk>`

### Mixins + GenericAPIView

- `GET, POST /rest/mixins/`
- `GET, PUT, DELETE /rest/mixins/<int:pk>`

### Generic Views

- `GET, POST /rest/generics/` (Token auth enabled)
- `GET, PUT, PATCH, DELETE /rest/generics/<int:pk>`

### ViewSets (router)

- `/rest/viewsets/` (router root)
- `/rest/viewsets/guests/`
- `/rest/viewsets/movies/` (supports search: `?search=<movie_name>`)
- `/rest/viewsets/reservations/`

### Post endpoint with object-level permissions

- `GET, PUT, PATCH, DELETE /post/generics/<int:pk>`

Safe methods are public; write operations are allowed only for the post author.

## Sample Payloads

Create guest:

```json
{
  "name": "Ahmed",
  "mobile": "0123456789"
}
```

Create movie:

```json
{
  "hall": "A1",
  "movie": "Inception"
}
```

Create reservation (viewset endpoint):

```json
{
  "guest": 1,
  "movie": 1
}
```

Create reservation (custom endpoint `/fbv/newreservation`):

```json
{
  "movie": "Inception",
  "hall": "A1",
  "name": "Ahmed",
  "mobile": "0123456789"
}
```

## Admin

To use Django admin:

```bash
python manage.py createsuperuser
```

Then open:

```text
http://127.0.0.1:8000/admin/
```

## Tests

Test scaffolding exists, but no project tests are implemented yet.
