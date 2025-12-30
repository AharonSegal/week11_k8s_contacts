# Contact Manager API

app for managing contacts (first name, last name, phone number) using **FastAPI** and **MySQL**, packaged with **Docker Compose**.

---

## What it does

- Stores contacts in a MySQL database (`contacts` table).
- Exposes CRUD endpoints:
  - `GET /contacts` – list all contacts
  - `POST /contacts` – create a new contact
  - `PUT /contacts/{id}` – update an existing contact
  - `DELETE /contacts/{id}` – delete a contact
- Includes a simple DB health check:
  - `GET /test/health`
  - `GET /test/db`

---

## How to run

1. **Set environment variables**

   At the project root, create a `.env` file 

   ```env
   DB_USER=root
   ROOT_PASS=pass
   DB_NAME=contacts_db
   API_PORT=8000