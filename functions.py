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
def create_users_1k(url,suffix):
  for i in range(1, 1001):
      user_data = {
          "name": f"user{suffix}{i}",
          "username": f"user{suffix}{i}"
      }
      response = requests.post(url + 'users', json=user_data)
  return response

# Function to delete a user from the backend
def delete_user(url, user_id):
    response = requests.delete(f"{url}users/{user_id}")
    return response

# Creating threads for each backend
def create_all_users(python_backend_url, java_backend_url):
    thread_python = threading.Thread(target=create_users_1k, args=(python_backend_url,"Python",))
    thread_java = threading.Thread(target=create_users_1k, args=(java_backend_url,"Java",))

    # Starting threads
    thread_python.start()
    thread_java.start()

    # Waiting for threads to complete
    thread_python.join()
    thread_java.join()

    print("Finished creating users on both backends.")

def create_and_delete_users_python(python_backend_url,offset):
    for i in range(1, 1001):
        create_user(python_backend_url, f'userPython{i}')
        if i % 10 == 0:
            delete_user(python_backend_url, i-offset)

def create_and_delete_users_java(java_backend_url,offset):
    for i in range(1, 1001):
        create_user(java_backend_url, f'userJava{i}')
        if i % 10 == 0:
            delete_user(java_backend_url, i-offset)

def create_and_delete_users_overlap(java_url, python_url):
    thread_python = threading.Thread(target=create_and_delete_users_python, args=(python_url,9,))
    thread_java = threading.Thread(target=create_and_delete_users_java, args=(java_url,9,))

    thread_java.start()
    thread_python.start()

    thread_python.join()
    thread_java.join()

def create_and_delete_users_distinct(java_url, python_url):
    thread_python = threading.Thread(target=create_and_delete_users_python, args=(python_url,7,))
    thread_java = threading.Thread(target=create_and_delete_users_java, args=(java_url,3,))

    thread_java.start()
    thread_python.start()

    thread_python.join()
    thread_java.join()
