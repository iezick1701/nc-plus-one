# NC Plus One

NC Plus One is an events management project I'm building as part of the Northcoders Data Engineering Bootcamp.

The project uses Python and PostgreSQL to manage data relating to events, users, venues and RSVPs.

I've implemented the database setup and seeding functionality, including creating tables, managing foreign key relationships and populating the database with data from JSON files.

I'm also using pytest to test the data and verify that records have been inserted correctly.

## Tech Stack

- Python
- PostgreSQL
- Psycopg 3
- Python-dotenv
- Pytest

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

**Note:** Check the setup script before running it, as it may recreate an existing database.

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

## Database Seeding

The database is populated using JSON files stored in the `db/data/` directory.

The seeding process is handled by `db/seed.py`.

It contains separate functions for creating and populating each table:

- `seed_users()` - Creates and populates the users table.
- `seed_venues()` - Creates and populates the venues table.
- `seed_events()` - Creates and populates the events table.
- `seed_rsvps()` - Creates and populates the RSVPs table.

The `read_file()` utility function reads the JSON data used during seeding.

### Running the Seed Function

From the project root, run:

```bash
python -m db.seed
```

This recreates the database tables and populates them with the JSON data.

**Warning:** Running the seed function drops and recreates the tables, removing existing records. It should only be used with disposable development data.

### Table Dependencies

The database contains four tables:

**Users**

- Stores user information, including email, password and name.
- Each user has a unique ID.
- Includes a timestamp showing when the user was created.

**Venues**

- Stores venue information, including name, address and capacity.
- Each venue has a unique ID.

**Events**

- Stores event information, including title, description, start time and end time.
- References the users table through `organiser_id`.
- References the venues table through `venue_id`.
- Includes a timestamp showing when the event was created.

**RSVPs**

- Stores information about users attending events.
- References the users table through `attendee_id`.
- References the events table through `event_id`.
- Includes a timestamp showing when the RSVP was created.

### Foreign Key Relationships

Because the tables reference one another, they must be created in the correct order.

Creation order:

1. Users
2. Venues
3. Events
4. RSVPs

When recreating the database, dependent tables must be dropped before the tables they reference.

For example, the RSVPs table must be dropped before the Events table.

The seed function handles these dependencies so that the database can be seeded repeatedly without foreign key errors.

## Pytest Configuration

The project uses a `pyproject.toml` file to configure pytest.

The file contains the following configuration:

```toml
[tool.pytest.ini_options]
pythonpath = ["."]
```

### What Does This Do?

The `pythonpath = ["."]` setting tells pytest to include the project's root directory in Python's module search path.

This allows the test files to import functions from other directories within the project.

For example:

```python
from db.seed import read_file
from db.connection import get_connection
```

Without this configuration, pytest may struggle to locate the `db` package when running tests, resulting in a `ModuleNotFoundError`.

Using `pyproject.toml` means we don't need to manually modify Python's import paths in individual test files.

It also keeps the testing configuration in one place, making the project easier to maintain.

## Testing

The project uses pytest to test the JSON data and check that records have been inserted correctly into PostgreSQL.

Tests cover:

- JSON files containing lists of records.
- Records containing the expected fields.
- Correct data types.
- Required fields containing valid values.
- Database records matching the JSON data.
- Automatically generated timestamps where applicable.

### Pytest Fixtures

The tests use pytest fixtures to load JSON data and reduce repeated setup code.

For example:

```python
import pytest
from db.seed import read_file

@pytest.fixture
def test_file():
    return read_file("users")
```

This fixture loads the user data from the JSON file and makes it available to multiple tests.

Using fixtures avoids repeatedly calling the same function in each test.

### Running All Tests

From the project root:

```bash
pytest -v
```

### Running Individual Test Files

Users:

```bash
pytest tests/test_users.py -v
```

Venues:

```bash
pytest tests/test_venues.py -v
```

Events:

```bash
pytest tests/test_events.py -v
```

RSVPs:

```bash
pytest tests/test_rsvps.py -v
```

Some tests query the database directly, so the database must be created and seeded before running them.

### Testing Database Records

Alongside checking the JSON data, the tests also query PostgreSQL to verify that records have been inserted correctly.

For example:

```python
cursor.execute("""
    SELECT name, address, capacity
    FROM venues
    ORDER BY id
""")

result = cursor.fetchall()
```

The returned records are compared against the expected values from the JSON file.

This helps confirm that the seeding process has inserted the correct information rather than simply checking the number of records.

### Repeated Seeding

The seeding process is designed to be repeatable.

Running the seed function multiple times should recreate the tables and insert the same data without producing errors.

This can be checked by running:

```bash
python -m db.seed
python -m db.seed
```

The database should contain the same seed records after each successful run.

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
├── tests/
│   ├── test_users.py
│   ├── test_venues.py
│   ├── test_events.py
│   └── test_rsvps.py
├── .env.example
├── .gitignore
├── pyproject.toml
├── README.md
└── requirements.txt
```

## Current Progress

- [x] Set up PostgreSQL database
- [x] Configure environment variables
- [x] Create reusable database connection
- [x] Test database connection
- [x] Create users table
- [x] Create venues table
- [x] Create events table
- [x] Create RSVPs table
- [x] Implement JSON file reading
- [x] Implement database seeding
- [x] Handle foreign key dependencies
- [x] Configure pytest using `pyproject.toml`
- [x] Add automated tests using pytest
- [x] Test JSON data structure and validation
- [x] Add tests to verify database records
- [ ] Build API endpoints

## Future Development

The next stage of the project will focus on building API functionality to interact with the database.

I'll continue updating this README as I implement additional features and progress through the Northcoders Data Engineering Bootcamp.