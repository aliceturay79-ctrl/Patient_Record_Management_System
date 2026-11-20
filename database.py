import psycopg2
from psycopg2 import Error


def connect_database():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="patient_record_management",
            user="postgres",
            password="alice2008",
            port="5432"
        )

        print("Database connected successfully!")
        return connection

    except Error as e:
        print("Database connection failed:", e)
        return None