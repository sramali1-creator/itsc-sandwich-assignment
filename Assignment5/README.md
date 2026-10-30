# Assignment 5 – CRUD Operations in FastAPI (Sandwich Maker Machine)

A modular FastAPI + SQLAlchemy (MySQL) API with full CRUD for **sandwiches, resources, recipes, orders and order details**.

## Structure
```
api/
  main.py              # app setup, CORS, table creation, route loading
  dependencies/        # DB config + session (config.py, database.py)
  models/              # SQLAlchemy tables (one file per table) + model_loader
  schemas/             # Pydantic request/response models with validation
  controllers/         # CRUD logic + error handling
  routers/             # APIRouter endpoints, wired up in routers/index.py
  tests/               # pytest suite (runs against SQLite)
```

## Tables
| Table | Fields |
|---|---|
| sandwiches | id, sandwich_name (unique), price |
| resources | id, item (unique), amount |
| recipes | id, sandwich_id → sandwiches, resource_id → resources, amount |
| orders | id, customer_name, order_date (defaults to now), description |
| order_details | id, order_id → orders, sandwich_id → sandwiches, amount |

## Endpoints
Each resource has `POST /`, `GET /`, `GET /{id}`, `PUT /{id}` (partial updates), `DELETE /{id}` under:
`/sandwiches`, `/resources`, `/recipes`, `/orders`, `/order-details`

## Error handling
- **404** when an id (or a referenced sandwich/resource/order) doesn't exist
- **400** on DB constraint errors: duplicate sandwich name/resource item, or deleting a row still referenced by another table
- **422** on invalid input (missing fields, negative price/amount, zero order quantity, names too long)
- DB errors roll back the session

## Setup
```bash
pip install -r requirements.txt
```
Create the MySQL database and set credentials in `api/dependencies/config.py`:
```sql
CREATE DATABASE sandwich_maker_api;
```
Run the server (from this folder):
```bash
uvicorn api.main:app --reload
```
Docs: http://127.0.0.1:8000/docs

## Tests
```bash
pytest
```
The tests set `DATABASE_URL` to a local SQLite file, so MySQL isn't needed to run them.
