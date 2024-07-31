import unittest
import psycopg2
from create_users import create_all_users

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

    def test_create_users(self):
        # Execute the function to create all users
        create_all_users()

        # Check if 1000 users exist in the database for both backends
        self.cursor.execute("SELECT COUNT(*) FROM app_user")
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 2000, "Not all users were created in the database.")

if __name__ == '__main__':
    unittest.main()
