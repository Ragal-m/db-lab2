# Database Lab 2: Login and To-Do Application

A web application that allows users to register, log in, and manage their personal to-do tasks.

## Team Members

- Mahmoud Hassan Elragal — ID: 2304247
- Marwan Tamer Hassan — ID: 2304015

## Technologies Used

- **Back end:** Python, Flask, PyMySQL, bcrypt
- **Front end:** HTML5, JavaScript, Tailwind CSS
- **Database:** MySQL 8.0

## Features

- User registration with input validation
- Login and logout
- Protected user sessions
- Add, edit, complete, and delete tasks
- Client-side and server-side validation
- Secure password hashing with bcrypt
- Parameterized SQL queries
- Responsive interface for desktop and mobile
- Bonus features: remaining-task count, live search, and task filters

## Project Structure

```text
db-lab2/
├── .env
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

## How to Run

1. Install Python and MySQL.
2. Install the Python dependencies:

   ```bash
   python -m pip install flask pymysql bcrypt python-dotenv
   ```

3. Create a `.env` file using `.env.example` and enter your local MySQL credentials.
4. Execute `database/schema.sql` in MySQL Workbench to create the database and tables.

   **Warning:** The script resets the `registration` database and deletes any existing data.

5. Run the application:

   ```bash
   python app.py
   ```

6. Open http://127.0.0.1:5000/register in your browser.
