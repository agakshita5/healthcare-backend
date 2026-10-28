# Healthcare Backend

A REST API for a healthcare application, built with Django, Django REST Framework and PostgreSQL. Users register and log in with JWT, manage their patients and a shared list of doctors, and assign doctors to patients.

## Tech stack

- Python 3.13, Django 5.2 (LTS), Django REST Framework
- PostgreSQL
- JWT authentication with `djangorestframework-simplejwt`
- Configuration through environment variables (`python-dotenv`)

## Project structure

```
healthcare/     project settings, root urls, error helper
users/          custom user model (login with email), register / login / refresh
patients/       patient CRUD, each user sees only their own patients
doctors/        doctor CRUD, shared between all users
mappings/       assign doctors to patients
postman/        Postman collection for every endpoint
```

Each app has `models.py`, `serializers.py`, `views.py`, `urls.py`, `admin.py` and `tests.py`.

## Setup

Requires Python 3.10+ and PostgreSQL 14+.

```bash
git clone https://github.com/agakshita5/healthcare-backend.git
cd healthcare-backend

python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

createdb healthcare               # or create it in pgAdmin / psql
cp .env.example .env              # then fill in the values
```

`.env` values:

| Variable | Example | Notes |
|---|---|---|
| `SECRET_KEY` | long random string | generate one with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | `True` | `False` in production |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | comma separated |
| `DB_NAME` | `healthcare` | |
| `DB_USER` | `postgres` | |
| `DB_PASSWORD` | | empty is fine for a local install without a password |
| `DB_HOST` | `localhost` | |
| `DB_PORT` | `5432` | |

```bash
python manage.py migrate
python manage.py createsuperuser  # optional, for /admin/
python manage.py runserver        # http://127.0.0.1:8000
```

## Authentication

Register or log in to get an `access` and a `refresh` token. Send the access token on every other request:

```
Authorization: Bearer <access token>
```

Access tokens last 60 minutes. Send the refresh token to `/api/auth/refresh/` for a new one (refresh tokens last 1 day). All endpoints except register, login and refresh return `401` without a valid token.

## API endpoints

### Authentication

| Method | URL | Body | Response |
|---|---|---|---|
| POST | `/api/auth/register/` | `name`, `email`, `password` | `201` user + `access`, `refresh` |
| POST | `/api/auth/login/` | `email`, `password` | `200` `access`, `refresh` |
| POST | `/api/auth/refresh/` | `refresh` | `200` new `access` |

### Patients

Each user only sees and manages the patients they created. Another user's patient returns `404`.

| Method | URL | Description |
|---|---|---|
| POST | `/api/patients/` | Add a patient |
| GET | `/api/patients/` | List my patients |
| GET | `/api/patients/<id>/` | Get one patient |
| PUT | `/api/patients/<id>/` | Update a patient (all fields) |
| PATCH | `/api/patients/<id>/` | Update some fields |
| DELETE | `/api/patients/<id>/` | Delete a patient (its mappings are removed too) |

Fields: `name`, `age` (0-150), `gender` (`male` / `female` / `other`), `phone`, `address`, `medical_history` (last three optional).

### Doctors

Doctors are shared: every logged-in user can view and manage all doctors.

| Method | URL | Description |
|---|---|---|
| POST | `/api/doctors/` | Add a doctor |
| GET | `/api/doctors/` | List all doctors |
| GET | `/api/doctors/<id>/` | Get one doctor |
| PUT | `/api/doctors/<id>/` | Update a doctor (all fields) |
| PATCH | `/api/doctors/<id>/` | Update some fields |
| DELETE | `/api/doctors/<id>/` | Delete a doctor (its mappings are removed too) |

Fields: `name`, `specialization`, `phone` (optional), `email` (optional, unique).

### Patient-doctor mappings

Users can only assign doctors to their own patients, and only see mappings of their own patients. The same doctor can't be assigned to the same patient twice (`400`).

| Method | URL | Description |
|---|---|---|
| POST | `/api/mappings/` | Assign a doctor to a patient. Body: `{"patient": <id>, "doctor": <id>}` |
| GET | `/api/mappings/` | List all mappings of my patients |
| GET | `/api/mappings/<patient_id>/` | List doctors assigned to a patient |
| DELETE | `/api/mappings/<id>/` | Remove a mapping |

> **Note:** as specified in the assignment, `GET /api/mappings/<id>/` and `DELETE /api/mappings/<id>/` share a URL but the id means different things: a **patient id** for GET and a **mapping id** for DELETE. The mapping id is returned when the mapping is created and by `GET /api/mappings/`.

## Errors

| Status | When |
|---|---|
| `400` | Validation failed, e.g. `{"age": ["Ensure this value is less than or equal to 150."]}` |
| `401` | Missing / invalid / expired token, or wrong login (`{"error": "invalid credentials"}`) |
| `404` | Record doesn't exist or belongs to another user |

## Testing

Automated tests (Django creates and removes a separate test database):

```bash
python manage.py test
```

Postman: import `postman/healthcare-backend.postman_collection.json`, start the server, and run the requests top to bottom (or use **Run collection**). Register / Login save the token, and the create requests save the new ids, so later requests work without copy-pasting. Run **Register** once; afterwards use **Login**.