import requests
import threading

def create_user(url, name):
    user_data = {
        "name": name,
        "username": name
    }
    response = requests.post(url + "users", json=user_data)
    return response

# Function to create users on the Python backend
def create_users_1k(url, suffix):
    users = []
    for i in range(1, 1001):
        user_data = {
            "name": f"user{suffix}{i}",
            "username": f"user{suffix}{i}"
        }
        response = requests.post(url + 'users', json=user_data)
        if response.status_code == 201:
            users.append(i)
    return users

# Function to delete a user from the backend
def delete_user(url, user_id):
    response = requests.delete(f"{url}users/{user_id}")
    return response

# Creating threads for each backend
def create_all_users(python_backend_url, java_backend_url):
    thread_python = threading.Thread(target=create_users_1k, args=(python_backend_url, "Python",))
    thread_java = threading.Thread(target=create_users_1k, args=(java_backend_url, "Java",))

    # Starting threads
    thread_python.start()
    thread_java.start()

    # Waiting for threads to complete
    thread_python.join()  
    thread_java.join()

    print("Finished creating users on both backends.")

def create_and_delete_users(python_backend_url, offset,suffix,users):
    for i in range(1, 1001):
        response = create_user(python_backend_url, f'user{suffix}{i}')
        if response.status_code == 201:
            users.append(i)
        if i % 10 == 0:
            delete_response = delete_user(python_backend_url, i - offset)
            if delete_response.status_code == 200:
                users.remove(i-offset)
    return users

def create_and_delete_users_parallel(java_url, python_url,python_offset,java_offset):
    python_users = []
    java_users = []


    thread_python = threading.Thread(target=create_and_delete_users, args=(python_url, python_offset,"Python",python_users))
    thread_java = threading.Thread(target=create_and_delete_users, args=(java_url, java_offset,"Java",java_users))

    thread_java.start()
    thread_python.start()

    thread_python.join()
    thread_java.join()

    return python_users, java_users

