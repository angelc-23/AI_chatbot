import streamlit as st
import json
import os

USER_FILE = "users.json"

# ---------- LOAD USERS ----------
def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

# ---------- SAVE USERS ----------
def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# ---------- SIGNUP ----------
def signup(username, password):
    users = load_users()

    if username in users:
        return False, "User already exists"

    users[username] = password
    save_users(users)

    return True, "Signup successful"

# ---------- LOGIN ----------
def login(username, password):
    users = load_users()

    if username in users and users[username] == password:
        return True

    return False
