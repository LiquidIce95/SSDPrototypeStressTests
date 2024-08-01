import unittest
import psycopg2
from functions import *

PythonUrl = "http://localhost:5000/"
JavaUrl = "http://localhost:8080/"

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

        self.cursor.execute("SELECT COUNT(*) FROM app_user WHERE username = 'PythonTestUser'")
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
        create_and_delete_users_overlap(JavaUrl, PythonUrl)

        self.cursor.execute("SELECT username FROM app_user WHERE username LIKE 'userPython%' OR username LIKE 'userJava%'")
        # users = self.cursor.fetchall()
        # users = [user[0] for user in users]

        # for i in range(10, 1001, 10):
        #     self.assertNotIn(f"userPython{i-9}", users)
        #     self.assertNotIn(f"userJava{i-9}", users)

        # Verify the total number of users
        self.cursor.execute("SELECT COUNT(*) FROM app_user")
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 1900, "The number of users in the database is incorrect after deletions.")


    def test_create_and_delete_users_distinct(self):
        # Execute the function to create and delete users
        create_and_delete_users_distinct(JavaUrl, PythonUrl)

        self.cursor.execute("SELECT username FROM app_user WHERE username LIKE 'userPython%' OR username LIKE 'userJava%'")
        # users = self.cursor.fetchall()
        # users = [user[0] for user in users]

        # for i in range(10, 1001, 10):
        #     self.assertNotIn(f"userPython{i-7}", users)
        #     self.assertNotIn(f"userJava{i-3}", users)

        # Verify the total number of users
        self.cursor.execute("SELECT COUNT(*) FROM app_user")
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 1800, "The number of users in the database is incorrect after deletions.")


if __name__ == '__main__':
    unittest.main()
