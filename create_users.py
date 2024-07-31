import requests
import threading

# Function to create users on the Python backend
def create_users_python_backend():
    url = "http://localhost:5000/users"
    for i in range(1, 1001):
        user_data = {
            "name": f"userPython{i}",
            "username": f"userPython{i}"
        }
        response = requests.post(url, json=user_data)
        if response.status_code == 201:
            print(f"Python backend: Successfully created user {i}")
        else:
            print(f"Python backend: Failed to create user {i}, Status Code: {response.status_code}")

# Function to create users on the Java backend
def create_users_java_backend():
    url = "http://localhost:8080/users"
    for i in range(1, 1001):
        user_data = {
            "username": f"userJava{i}",
            "name": f"userJava{i}"
        }
        response = requests.post(url, json=user_data)
        if response.status_code == 201:
            print(f"Java backend: Successfully created user {i}")
        else:
            print(f"Java backend: Failed to create user {i}, Status Code: {response.status_code}")

# Creating threads for each backend
def create_all_users():
    thread_python = threading.Thread(target=create_users_python_backend)
    thread_java = threading.Thread(target=create_users_java_backend)

    # Starting threads
    thread_python.start()
    thread_java.start()

    # Waiting for threads to complete
    thread_python.join()
    thread_java.join()

    print("Finished creating users on both backends.")
