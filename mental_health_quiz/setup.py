import sys
import os
import mysql.connector
from mysql.connector import errorcode
from getpass import getpass

DB_NAME = "mental_health_app"

def setup_database():
    print("--- Setting up the database ---")

    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", None) or getpass(f"Enter MySQL password for {user}: ")
    host = os.getenv("MYSQL_HOST", "127.0.0.1")

    try:
        cnx = mysql.connector.connect(user=user, password=password, host=host)
        cursor = cnx.cursor()
        print("Successfully connected to MySQL server.")
    except mysql.connector.Error as err:
        print(f"Failed to connect: {err}")
        sys.exit(1)

    try:
        cursor.execute(f"CREATE DATABASE {DB_NAME} DEFAULT CHARACTER SET 'utf8mb4'")
        print(f"Database '{DB_NAME}' created.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DB_CREATE_EXISTS:
            print(f"Database '{DB_NAME}' already exists.")
        else:
            print(err)
            sys.exit(1)

    cursor.execute(f"USE {DB_NAME}")

    table_description = (
        "CREATE TABLE IF NOT EXISTS `quiz_history` ("
        "  `id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `username` varchar(255) NOT NULL,"
        "  `test_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
        "  `score` int(11) NOT NULL,"
        "  `assessment` varchar(255) NOT NULL,"
        "  `recommendations` TEXT NOT NULL,"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"
    )

    try:
        print("Creating table 'quiz_history' if needed...")
        cursor.execute(table_description)
        print("Table 'quiz_history' is ready.")
    except mysql.connector.Error as err:
        print(f"Failed to prepare the table: {err}")
        sys.exit(1)
    finally:
        cursor.close()
        cnx.close()

    print("--- Database setup complete ---")
    return True

def main():
    print("Starting the application setup...\n")
    db_ok = setup_database()
    print("*************************************")
    if db_ok:
        print("Setup finished successfully!\nRun main.py to start the app.")
    else:
        print("Setup failed. Check the errors above.")
    print("*************************************")

if __name__ == "__main__":
    main()
