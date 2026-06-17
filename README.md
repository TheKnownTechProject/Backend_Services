# TheTechProjectBackendServices

Admin backend bootstrap for The Tech Project.

## Stack

- `FastAPI`
- `Pydantic v2`
- development adapters for `DynamoDB` repositories and `S3` asset storage

## Current scope

Implemented admin modules:

- auth
- categories
- tags
- assets
- blogs
- preview
- dashboard
- analytics
- master data

The repository layer currently uses an in-memory development store and local file storage under `storage/assets` so the API is usable before AWS integration is finished. The route, controller, service, and repository separation follows the supplied design documents, so replacing the development adapters with real DynamoDB/S3 implementations is straightforward.

## Run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

Default seeded admin user:

- email: `admin@thetechproject.local`
- password: `Admin@123`
