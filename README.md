# Patient Record Management System

## 1. Project Overview

The Patient Record Management System is a desktop application developed using Python, PyQt6 and PostgreSQL. It helps manage patient information and hospital records in an organised way.

The system connects a Python frontend to a PostgreSQL relational database backend.

## 2. Technologies Used

- Python
- PyQt6
- PostgreSQL 18
- pgAdmin 4
- psycopg2
- Visual Studio Code

## 3. Main Features

The application provides the following features:

- Patient Registration
- View Patients
- Appointment Management
- Medical Records Management
- Prescription Management

## 4. Database Structure

The PostgreSQL database is named `patient_record_management`.

It contains seven main tables:

1. Patients
2. Departments
3. Doctors
4. Appointments
5. Medical Records
6. Prescriptions
7. Medical Record Audit

The database uses primary keys, foreign keys, constraints and relationships to maintain data integrity.

## 5. Advanced PostgreSQL Features

The project demonstrates:

- INNER JOIN, LEFT JOIN and RIGHT JOIN queries
- Database views
- Indexes
- Stored procedures
- Functions
- Triggers
- Transactions using COMMIT and ROLLBACK
- Database testing

## 6. Installation and Setup

### Requirements

Install the following:

- Python
- PostgreSQL
- pgAdmin 4
- Required Python packages

### Install Python Packages

Open the VS Code terminal and run:

```bash
pip install PyQt6 psycopg2-binary
```

### Database Setup

1. Open PostgreSQL using pgAdmin 4.
2. Create the database named `patient_record_management` if it does not already exist.
3. Execute the SQL commands in `patient_record_management.sql` to create the database tables and supporting database objects.

Do not execute the script again on an already populated database unless you have checked its contents.

### Configure the Database Password

The application reads the PostgreSQL password from an environment variable named `DB_PASSWORD`.

In Git Bash, enter:

```bash
export DB_PASSWORD='alice2008'
```

Replace the example with your own PostgreSQL password.

### Run the Application

Open the project folder in VS Code and run:

```bash
python main.py
```

## 7. Project Files

- `main.py` – Main Python application.
- `database.py` – PostgreSQL database connection.
- `patient_record_management.sql` – SQL database implementation and queries.
- `README.md` – Project documentation.
- `LICENSE` – Project licence.
- `.gitignore` – Files excluded from Git tracking.

## 8. Frontend and Backend Integration

The application uses PyQt6 to provide the graphical user interface. Python connects to PostgreSQL using psycopg2.

When users register patients or manage appointments, medical records and prescriptions, the application communicates with the PostgreSQL database to store and retrieve information.

## 9. Purpose of the Project

This project demonstrates the design and implementation of a relational database backend integrated with a Python desktop application. It applies database design principles, SQL development and advanced PostgreSQL features to a real-world patient record management scenario.
