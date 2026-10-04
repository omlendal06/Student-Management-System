# Student Management System

## Project Information

- Project name: Student Management System
- Short description: A simple Python-based system to manage student records.
- Objective: Help beginners understand CRUD operations, database usage, and code organization in a practical project.

## Technology Stack

- Programming language: Python 3
- Database: SQLite
- User interface: Console/terminal based
- Testing: Pytest
- Dependencies: Minimal, only pytest for automated checks

## Project Architecture

This project follows a simple beginner-friendly architecture:

- Models: Store the data structure of a student.
- Controllers: Handle menu actions and user input.
- Services: Apply validation and business rules.
- Repositories: Communicate with SQLite.
- Utilities: Provide helper functions like validation and database setup.
- Database: Stores student information safely.

## Folder Structure

```text
Student Management System/
├── .gitignore
├── README.md
├── FLOW.md
├── requirements.txt
├── database/
│   ├── schema.sql
│   ├── sample_data.sql
│   └── students.db
├── docs/
│   └── project_overview.md
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── main.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── student_controller.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── student.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── student_repository.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── student_service.py
│   └── utils/
│       ├── __init__.py
│       ├── database.py
│       └── validators.py
└── tests/
    ├── test_student_repository.py
    └── test_student_service.py
```

## Features

- Add student records
- View all students
- View a single student's details
- Update a student
- Delete a student
- Search a student by keyword
- Dashboard showing total students and total courses
- Validation for required fields, email, phone number, student ID, and duplicates

## Requirements

- Python 3.10 or newer
- Pytest (installed through requirements.txt)

## Installation

1. Open a terminal in the project folder.
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
3. Activate the environment:
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Database Setup

The project uses SQLite. The database file is created automatically when the app runs. A schema file is kept in the database folder.

To initialize the database manually:

```bash
python -c "from src.utils.database import initialize_database; initialize_database()"
```

## Configuration

There is no complex configuration required for this beginner project. The application makes use of the default SQLite database file located in the database folder.

## Running the Project

Run the project with:

```bash
python src/main.py
```

or:

```bash
python -m src.main
```

## Usage

After starting the application:

1. Choose an option from the menu.
2. Add or search for students.
3. Use the dashboard for summary information.
4. View or update student details when needed.

## API Documentation

This project is a console-based application, so it does not use HTTP routes or a web API.

## Screenshots

Screenshots can be added later in this section.

## Future Improvements

- Add login system with password hashing
- Add student photo upload
- Add export to CSV or Excel
- Add a graphical user interface (GUI)
- Add sorting and pagination

## Author

Student Management System project for beginner learning and college portfolio use.
