# Database Lab 2 — Login and To-Do Application

## Project Description

This project is a web application developed using Flask and MySQL. It allows users to create accounts, log in securely, and manage their personal to-do lists. Users can add, edit, complete, and delete tasks through a responsive interface.

## Team Members

- **Mahmoud Hassan Elragal** — ID: 2304247
- **Marwan Tamer Hassan** — ID: 2304015

## Team Contributions

Both team members collaborated throughout the project using pair programming.

Their shared work included:

- Designing and implementing the database schema.
- Developing Flask routes and database operations.
- Implementing registration, login, logout, and session management.
- Building the responsive frontend with Tailwind CSS and Jinja2.
- Implementing task management and validation.
- Testing security, database constraints, and unauthorized access.
- Preparing screenshots and project documentation.
- Testing the bonus features, including the task counter, search, filters, and theme switching.

## Technologies Used

- Python and Flask
- MySQL 8.0
- HTML5 and JavaScript
- Tailwind CSS
- Jinja2
- PyMySQL
- bcrypt
- python-dotenv
- MySQL Workbench
- Visual Studio Code

## Requirements and Features

- **R1 — Registration:** Create an account using a name, email, password, and password confirmation. Duplicate emails display `Email Already Exists`.
- **R2 — Authentication:** Log in with registered credentials and log out securely. Invalid credentials display `Invalid email or password`.
- **R3 — Access Control:** Protect the to-do page and ensure users can access only their own tasks.
- **R4 — Add Tasks:** Create new to-do items.
- **R5 — Edit Tasks:** Modify task titles using inline editing.
- **R6 — Complete Tasks:** Mark tasks as completed or reopen them.
- **R7 — Delete Tasks:** Remove tasks after confirming the action.
- **R8 — Validation:** Validate form data in both the browser and Flask backend.
- **R9 — Security:** Use bcrypt password hashes, parameterized SQL queries, and session-based user identification.
- **R10 — User Interface:** Provide a responsive layout, an empty-state message, and visible indicators for completed tasks.

## Bonus Features

- **Task Counter:** Displays the number of remaining open tasks.
- **Live Search:** Searches tasks by title as the user types.
- **Status Filters:** Filter tasks by All, Open, or Completed.
- **Dark and Light Modes:** Allow users to switch between the two interface themes.

## How to Run the Project

### 1. Install the Requirements

Make sure Python 3 and MySQL Server 8.0 are installed on your computer.

Install the project dependencies:

```bash
python -m pip install -r requirements.txt
```

Alternatively, install the main packages manually:

```bash
python -m pip install flask pymysql bcrypt python-dotenv
```

### 2. Configure MySQL

Open MySQL Workbench and connect to your local MySQL server.

Execute the SQL script:

`database/schema.sql`

This script creates the `registration` database and the required `users` and `todos` tables.

**Warning:** Check the SQL script before executing it because database reset commands may delete existing data.

### 3. Configure Environment Variables

Copy `.env.example` to `.env` and enter your local database settings, including `DB_HOST`, `DB_USER`, `DB_PASSWORD`, and `SECRET_KEY`.

Do not commit your `.env` file to Git.

### 4. Start the Application

Open the project folder in Visual Studio Code and run:

```bash
python app.py
```

### 5. Open the Website

Visit the following address in your browser:

http://127.0.0.1:5000

Register a new account or open the registration page directly:

http://127.0.0.1:5000/register

## Project Structure

```text
db-lab2/
├── .env.example
├── .gitignore
├── .vscode/
│   └── settings.json
├── app.py
├── database/
│   └── schema.sql
├── requirements.txt
├── screenshots/
│   ├── login.png
│   ├── mobile_view.png
│   ├── register_errors.png
│   └── todos.png
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   └── todos.html
└── README.md
```

## Screenshots

The project screenshots demonstrate the application's main pages and responsive design.

- **Registration validation:** `screenshots/register_errors.png`
- **Login page:** `screenshots/login.png`
- **To-do list and completed tasks:** `screenshots/todos.png`
- **Mobile interface:** `screenshots/mobile_view.png`

## Security

The application follows several security practices:

- Passwords are stored as bcrypt hashes rather than plaintext.
- Parameterized SQL queries help protect against SQL injection.
- Authentication is required before accessing the task list.
- Each task operation checks ownership using the authenticated user's ID.
- The user's ID is obtained from the server-side session.
- Form data is validated on both the client and server.
- Logout destroys the active session.
- Database credentials and secret keys are kept in environment variables.

## Theory Questions and Answers

### Q1: Why do `UPDATE` and `DELETE` use `AND user_id = ?`?

The condition ensures that users can modify or delete only tasks that belong to them. Without it, a user could change a task ID in a request and potentially access another user's task. This condition helps prevent unauthorized modifications and IDOR vulnerabilities.

### Q2: What happens if a to-do is inserted with a `user_id` that does not exist?

MySQL rejects the insertion because the specified user does not exist in the referenced `users` table. The **foreign key constraint** enforces referential integrity by requiring the referenced user record to exist.

### Q3: Why do we store a password hash instead of the actual password?

Storing bcrypt hashes helps protect user credentials if the database is exposed. Bcrypt uses a salt and a computational cost that make password guessing more difficult. The application verifies passwords without storing their original values.

### Q4: Why is an empty-name check needed if the column is `NOT NULL`?

The `NOT NULL` constraint prevents SQL `NULL` values, but it does not prevent empty strings or strings containing only spaces. Application-level validation is needed to ensure that users enter a valid name.

## Conclusion

The project demonstrates how Flask and MySQL can be combined to create a secure and responsive task management application. It covers authentication, database relationships, CRUD operations, input validation, access control, and additional features that improve task organization and usability.