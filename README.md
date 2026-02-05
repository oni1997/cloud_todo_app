# Overview

As a software engineer, I built this project to deepen my understanding of how applications interact with cloud-based databases and authentication systems. The goal was to design a simple but complete system that securely stores user data in the cloud while enforcing proper access control.

The software is a command-line To-Do application written in Python that integrates with **Google Firebase Firestore** as a cloud database. Users can register and log in using Firebase Authentication, then create, view, update, and delete their own tasks. All task data is stored remotely in Firestore and retrieved through Firebase’s API.

To use the program, the user runs the Python application, authenticates with an email and password, and then selects from a menu of options to manage tasks. Each task is associated with the authenticated user, ensuring data isolation between users.

The purpose of writing this software was to gain hands-on experience with cloud databases, authentication, and CRUD operations, while following good practices such as environment-based configuration and modular code design.

[Software Demo Video](http://youtube.link.goes.here)

---

# Cloud Database

The cloud database used in this project is **Google Firebase Firestore**, which is a NoSQL key/value document database provided as part of Firebase.

The database consists of a **tasks** collection. Each document in the collection represents a single task and includes the following fields:

* `user_uid` – The Firebase Authentication user ID that owns the task
* `title` – The task title
* `description` – The task description
* `completed` – Boolean value indicating task completion
* `timestamp` – Server-generated timestamp for creation or updates

Firestore handles document IDs automatically, which are used by the application to update and delete specific tasks.

---

# Development Environment

The software was developed using the following tools:

* Visual Studio Code
* Python 3
* Git and GitHub
* Firebase Console

The programming language used is **Python**. The main libraries and packages include:

* `firebase-admin` for interacting with Firebase Authentication and Firestore
* `python-dotenv` for managing environment variables
* Standard Python libraries such as `os` and `getpass`

---

# Useful Websites

The following websites were helpful during development:

* [Google Firebase Documentation](https://firebase.google.com/docs)
* [Firestore Python API Reference](https://cloud.google.com/firestore/docs)
* [Firebase Admin SDK for Python](https://firebase.google.com/docs/admin/setup)
* [Python dotenv Documentation](https://pypi.org/project/python-dotenv/)

---

# Future Work

* Add due dates and task priorities
* Improve the authentication flow with additional validation
* Implement Firestore security rules
* Add real-time updates using Firestore listeners
* Build a web-based interface for the application