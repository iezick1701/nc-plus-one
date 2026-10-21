# NC Plus One

NC Plus One is an events management project I'm building as part of the Northcoders Data Engineering Bootcamp.

The project uses Python and PostgreSQL to manage data relating to events, users, venues and RSVPs.

I'm currently working on the database side of the project, including setting up the connection, creating tables and preparing the database for seeding.

## Tech Stack

- Python
- PostgreSQL
- Psycopg 3
- Python-dotenv

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd nc-plus-one
```

### 2. Set Up a Virtual Environment

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL

Make sure PostgreSQL is installed and running locally.

Run the database setup script from the project root:

```bash
psql -d postgres -f db/setup.sql
```

This creates the `nc_plus_one` database.

Note: Check the setup script before running it, as it may recreate an existing database.

### 5. Configure Environment Variables

Database credentials are stored in a `.env` file rather than being hardcoded into the Python code.

Create your own `.env` file using the provided example:

```bash
cp .env.example .env
```

Add your local PostgreSQL credentials:

```dotenv
DB_NAME=nc_plus_one
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

The `.env` file is ignored by Git to prevent credentials from being committed.

### 6. Test the Database Connection

The database connection is handled by `get_connection()` in `db/connection.py`.

To check that everything is working, run:

```bash
python -c 'from db.connection import get_connection; conn = get_connection(); print(conn.info.dbname); conn.close()'
```

You should see:

```text
nc_plus_one
```

## Project Structure

```text
nc-plus-one/
├── db/
│   ├── data/
│   │   ├── events.json
│   │   ├── rsvps.json
│   │   ├── users.json
│   │   └── venues.json
│   ├── connection.py
│   ├── seed.py
│   └── setup.sql
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Current Progress

- [x] Set up PostgreSQL database
- [x] Configure environment variables
- [x] Create reusable database connection
- [x] Test database connection
- [ ] Create database tables
- [ ] Implement database seeding
- [ ] Build API endpoints
- [ ] Add automated tests

I'll update this README as I work through the remaining features.