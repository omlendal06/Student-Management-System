# Project Overview

This project is a beginner-friendly Student Management System built with Python and SQLite.

## How it works

1. The user chooses an action from the console menu.
2. The controller receives the request and calls the service layer.
3. The service layer checks the data and applies business rules.
4. The repository layer interacts with the SQLite database.
5. Results are shown back to the user in the console.

## Main idea

The project splits responsibilities so that:
- models store student data,
- services handle validation and business logic,
- repositories manage database operations,
- controllers handle the menu and user interaction,
- utilities provide reusable helper functions.
