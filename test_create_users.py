import unittest
import psycopg2
import subprocess
import os
from time import sleep
from functions import *

PythonUrl = "http://localhost:5000/"
JavaUrl = "http://localhost:8080/"
BACKUP_FILE = "db_backup.sql"
DB_CONTAINER_NAME = "ssdprototypepostgresdb-db-1"

def perform_backup(self):
    # Path to the backup file inside the Docker container
    backup_file_path = f"/backups/{BACKUP_FILE}"

    # Ensure the backups directory exists
    subprocess.run(["docker", "exec", DB_CONTAINER_NAME, "mkdir", "-p", "/backups"])

    # Command to create a backup of the database inside the Docker container
    command = [
        "docker", "exec", DB_CONTAINER_NAME, "pg_dump",
        "--dbname=postgresql://myuser:mypassword@localhost:5432/mydatabase",
        "--file", backup_file_path
    ]

    # Execute the pg_dump command
    result = subprocess.run(command, capture_output=True, text=True)

    # Check if the command was successful
    self.assertEqual(result.returncode, 0, f"pg_dump failed: {result.stderr}")

    # Copy the backup file from the Docker container to the host
    subprocess.run(["docker", "cp", f"{DB_CONTAINER_NAME}:{backup_file_path}", BACKUP_FILE])

    self.assertTrue(os.path.exists(BACKUP_FILE), "Backup file was not created")


class TestCreateUsers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Connect to the PostgreSQL database
        cls.conn = psycopg2.connect(
            dbname="mydatabase",
            user="myuser",
            password="mypassword",
            host="localhost",
            port="5432"
        )
        cls.cursor = cls.conn.cursor()

    @classmethod
    def tearDownClass(cls):
        # Close the database connection
        cls.cursor.close()
        cls.conn.close()

    def setUp(self):
        # Delete all entries in the users table before each test
        self.cursor.execute("DELETE FROM app_user")
        self.conn.commit()

        # Reset the sequence associated with the primary key
        self.cursor.execute("ALTER SEQUENCE app_user_id_seq RESTART WITH 1")
        self.conn.commit()
    
    def test_Python_create_and_delete_single_User(self):
        resp = create_user(PythonUrl, 'PythonTestUser')
        self.assertEqual(resp.status_code, 201, "Failed to create user")
        
        user_id = resp.json().get('id')
        self.assertIsNotNone(user_id, "No user ID returned")

        delete_resp = delete_user(PythonUrl, user_id)
        self.assertEqual(delete_resp.status_code, 200, "Failed to delete user")

        self.cursor.execute("SELECT COUNT(*) FROM app_user WHERE username = 'PythonTestUser'")
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 0, "User was not deleted from the database")

    def test_Java_create_and_delete_single_User(self):
        resp = create_user(JavaUrl, 'JavaTestUser')
        self.assertEqual(resp.status_code, 201, "Failed to create user")
        
        user_id = resp.json().get('id')
        self.assertIsNotNone(user_id, "No user ID returned")

        delete_resp = delete_user(JavaUrl, user_id)
        self.assertEqual(delete_resp.status_code, 200, "Failed to delete user")

        self.cursor.execute("SELECT COUNT(*) FROM app_user WHERE username = 'JavaTestUser'")
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 0, "User was not deleted from the database")

    def test_create_users(self):
        # Execute the function to create all users
        create_all_users(PythonUrl, JavaUrl)

        # Check if 1000 users exist in the database for both backends
        self.cursor.execute("SELECT COUNT(*) FROM app_user")
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 2000, "Not all users were created in the database.")

    def test_create_and_delete_users_overlap(self):
        # Execute the function to create and delete users
        python_users, java_users = create_and_delete_users_parallel(JavaUrl, PythonUrl,9,9)

        users = [i for i in python_users if i in java_users]

        # Verify the users in the list are in the database
        self.cursor.execute("SELECT id FROM app_user")  # Changed query to select id

        users_in_db = [row[0] for row in self.cursor.fetchall()]

        for user_id in users:
            self.assertIn(user_id, users_in_db, f"{user_id} was not found in the database")
        
        # Verify the total number of users
        self.cursor.execute("SELECT COUNT(*) FROM app_user")
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 1900, "The number of users in the database is incorrect after deletions.")

    def test_create_and_delete_users_distinct(self):
        # Execute the function to create and delete users
        python_users, java_users = create_and_delete_users_parallel(JavaUrl, PythonUrl,3,7)

        # Verify the users in the list are in the database
        self.cursor.execute("SELECT id FROM app_user")  # Changed query to select id

        users_in_db = [row[0] for row in self.cursor.fetchall()]

        users = [i for i in python_users if i in java_users]

        for user_id in users:
            self.assertIn(user_id, users_in_db, f"{user_id} was not found in the database")
        

        # Verify the total number of users
        self.cursor.execute("SELECT COUNT(*) FROM app_user")
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 1800, "The number of users in the database is incorrect after deletions.")

    def test_backup_database(self):
        # Start the user creation and deletion in parallel

        user_creation_thread = threading.Thread(target=create_and_delete_users_parallel, args=(JavaUrl, PythonUrl,3,7))
        user_creation_thread.start()

        sleep(3)

        # Perform the backup
        perform_backup(self)

        # Ensure the user creation and deletion thread completes
        user_creation_thread.join()
        # Verify the total number of users
        self.cursor.execute("SELECT COUNT(*) FROM app_user")
        count = self.cursor.fetchone()[0]


        self.assertEqual(count, 1800, "The number of users in the database is incorrect after deletions.")


    def test_backup_database2(self):
        # Start the user creation and deletion in parallel

        user_creation_thread = threading.Thread(target=create_and_delete_users_parallel, args=(JavaUrl, PythonUrl,8,8))
        user_creation_thread.start()

        sleep(5)

        # Perform the backup
        perform_backup(self)

        # Ensure the user creation and deletion thread completes
        user_creation_thread.join()
        # Verify the total number of users
        self.cursor.execute("SELECT COUNT(*) FROM app_user")
        count = self.cursor.fetchone()[0]


        self.assertEqual(count, 1900, "The number of users in the database is incorrect after deletions.")

    def test_backup_database3(self):
        # Start the user creation and deletion in parallel

        user_creation_thread = threading.Thread(target=create_and_delete_users_parallel, args=(JavaUrl, PythonUrl,5,5))
        user_creation_thread.start()


        # Perform the backup
        perform_backup(self)

        # Ensure the user creation and deletion thread completes
        user_creation_thread.join()
        # Verify the total number of users
        self.cursor.execute("SELECT COUNT(*) FROM app_user")
        count = self.cursor.fetchone()[0]


        self.assertEqual(count, 1900, "The number of users in the database is incorrect after deletions.")

