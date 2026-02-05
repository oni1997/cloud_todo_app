import os
import re
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore, auth
from getpass import getpass

# ---------------------------
# Load Environment Variables
# ---------------------------
load_dotenv()
service_account_path = os.getenv("FIREBASE_CREDENTIALS")
if not service_account_path:
    raise ValueError("FIREBASE_CREDENTIALS not set in .env")

# ---------------------------
# Initialize Firebase
# ---------------------------
cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

# ---------------------------
# CRUD Functions
# ---------------------------

def create_task(user_uid, title, description):
    task_ref = db.collection("tasks").document()
    task_ref.set({
        "user_uid": user_uid,
        "title": title,
        "description": description,
        "completed": False,
        "timestamp": firestore.SERVER_TIMESTAMP
    })
    print("Task created successfully!")

def read_tasks(user_uid):
    tasks = db.collection("tasks").where("user_uid", "==", user_uid).stream()
    print("\n--- Your Tasks ---")
    found = False
    for task in tasks:
        found = True
        t = task.to_dict()
        print(
            f"ID: {task.id}\n"
            f"Title: {t['title']}\n"
            f"Description: {t['description']}\n"
            f"Completed: {t['completed']}\n"
        )
    if not found:
        print("No tasks found.")

def update_task(task_id, user_uid, title=None, description=None, completed=None):
    task_ref = db.collection("tasks").document(task_id)
    task = task_ref.get()

    if not task.exists:
        print("Task not found.")
        return

    if task.to_dict().get("user_uid") != user_uid:
        print("Unauthorized action.")
        return

    updates = {}
    if title is not None:
        updates["title"] = title
    if description is not None:
        updates["description"] = description
    if completed is not None:
        updates["completed"] = completed

    if not updates:
        print("No updates provided.")
        return

    updates["timestamp"] = firestore.SERVER_TIMESTAMP
    task_ref.update(updates)
    print("Task updated successfully!")

def delete_task(task_id, user_uid):
    task_ref = db.collection("tasks").document(task_id)
    task = task_ref.get()

    if not task.exists:
        print("Task not found.")
        return

    if task.to_dict().get("user_uid") != user_uid:
        print("Unauthorized action.")
        return

    task_ref.delete()
    print("Task deleted successfully!")

# ---------------------------
# Authentication Functions
# ---------------------------

def is_valid_email(email):
    # Simple regex for email validation
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def login():
    while True:
        email = input("Email: ")
        if not is_valid_email(email):
            print("Invalid email format. Please enter a valid email (example@domain.com).")
            continue

        password = getpass("Password: ")

        try:
            user = auth.get_user_by_email(email)
            # Firebase Admin cannot verify password
            print(f"Logged in as {user.email}")
            return user.uid
        except auth.UserNotFoundError:
            print("User does not exist.")
            return None  # Don't ask retry here, let authenticate handle it

def register():
    while True:
        email = input("Email: ")
        if not is_valid_email(email):
            print("Invalid email format. Please enter a valid email (example@domain.com).")
            continue

        password = getpass("Password: ")

        try:
            user = auth.create_user(email=email, password=password)
            print("Account created successfully!")
            return user.uid
        except auth.EmailAlreadyExistsError:
            print("Email already registered. Please log in instead.")
            return None  # Don't ask retry here, let authenticate handle it

def authenticate():
    while True:
        print("\n1. Login")
        print("2. Register")
        choice = input("Select an option: ")

        if choice == "1":
            uid = login()
        elif choice == "2":
            uid = register()
        else:
            print("Invalid selection.")
            uid = None

        if uid:
            return uid  # Successfully logged in or registered

        # Only one retry prompt for everything
        retry = input("Do you want to try again or switch option? (yes/no): ").lower()
        if retry != "yes":
            return None

# ---------------------------
# Main Program
# ---------------------------

def main():
    print("Welcome to Cloud To-Do App")

    user_uid = authenticate()
    if not user_uid:
        print("Authentication failed.")
        return

    while True:
        print("\nOptions:")
        print("1. Create Task")
        print("2. Read Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            title = input("Task Title: ")
            description = input("Task Description: ")
            create_task(user_uid, title, description)

        elif choice == "2":
            read_tasks(user_uid)

        elif choice == "3":
            task_id = input("Task ID to update: ")
            title = input("New Title (leave blank to skip): ") or None
            description = input("New Description (leave blank to skip): ") or None

            completed_input = input("Completed? (yes/no/leave blank): ").lower()
            completed = None
            if completed_input == "yes":
                completed = True
            elif completed_input == "no":
                completed = False

            update_task(task_id, user_uid, title, description, completed)

        elif choice == "4":
            task_id = input("Task ID to delete: ")
            delete_task(task_id, user_uid)

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()