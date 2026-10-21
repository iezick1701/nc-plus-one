# NC Plus One API

## Overview

NC Plus One is a RESTful API for an events management platform.

The API allows users to register, discover events, RSVP to events,
and manage their attendance.

Event organisers can create and manage events, as well as view
statistics about their attendees.

This project focuses on backend development, database management,
and building an API that can be integrated with a frontend application.

## Technologies

- Python
- PostgreSQL
- SQL
- Git & GitHub

## Database Setup

This project uses PostgreSQL to store and manage application data.

### Prerequisites

- PostgreSQL installed and running.
- Access to the PostgreSQL command-line tool (`psql`).

### Setting Up the Database

The database setup script is located at `db/setup.sql`, outside the `db/data` folder.

During development, the script can be created from the project's root directory using:

```bash
touch db/setup.sql
```

Once the script contains the required SQL commands, run:

```bash
psql -d postgres -f db/setup.sql
```

This script will:
1. Drop the existing `nc_plus_one` database if it exists.
2. Create a fresh database named `nc_plus_one`.

**Warning:** Running this script will delete any existing data in the database.

### Verifying the Database

To check that the database was created successfully, run:

```bash
psql -l
```

The `nc_plus_one` database should appear in the list.