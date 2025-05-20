import hashlib
import pandas as pd
import os
import re

USER_CSV = os.path.join("data", "users.csv")

# Hash password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Validate email format
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

# Authenticate user credentials
def authenticate_user(username, password):
    if not os.path.exists(USER_CSV):
        return False
    df = pd.read_csv(USER_CSV)
    hashed = hash_password(password)
    return not df[(df.username == username) & (df.password_hash == hashed)].empty

# Register a new user
def register_user(username, email, password):
    os.makedirs("data", exist_ok=True)

    # Validate email format
    if not is_valid_email(email):
        return False, "Invalid email format."

    hashed = hash_password(password)
    new_user = pd.DataFrame([[username, email, hashed]], columns=["username", "email", "password_hash"])

    if not os.path.exists(USER_CSV) or os.path.getsize(USER_CSV) == 0:
        df = new_user
    else:
        try:
            df = pd.read_csv(USER_CSV)
            if username in df.username.values:
                return False, "Username already exists."
            if email in df.email.values:
                return False, "Email already registered."
            df = pd.concat([df, new_user], ignore_index=True)
        except Exception as e:
            df = new_user

    df.to_csv(USER_CSV, index=False)
    return True, "Registration successful."
