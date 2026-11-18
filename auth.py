from pathlib import Path

import bcrypt

USERS_FILE = Path(__file__).parent / "DATA" / "users.txt"


def generate_hash(password):
    """Turn a password into a bcrypt hash (returned as text)."""
    byte_password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(byte_password, salt)
    return hashed.decode("utf-8")


def is_valid_hash(password, hashed):
    """True if the password matches the stored hash."""
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def user_exists(username, path=USERS_FILE):
    """True if this username is already in the file."""
    if not path.exists():
        return False
    with open(path, "r") as file:
        for line in file:
            stored_name, _ = line.strip().split(",", 1)
            if stored_name.lower() == username.lower():
                return True
    return False


def register_user(username, password, path=USERS_FILE):
    """Add a new user. Returns (True or False, a message)."""
    username = username.strip()
    if username == "" or "," in username:
        return False, "Username cannot be empty or contain a comma."
    if len(password) < 8:
        return False, "Password must be at least 8 characters."
    if user_exists(username, path):
        return False, "That username is already taken."

    path.parent.mkdir(exist_ok=True)
    with open(path, "a") as file:
        file.write(f"{username},{generate_hash(password)}\n")
    return True, "Registered. You can log in now."


def login_user(username, password, path=USERS_FILE):
    """Check a username and password. Returns (True or False, a message)."""
    if path.exists():
        with open(path, "r") as file:
            for line in file:
                stored_name, stored_hash = line.strip().split(",", 1)
                if stored_name.lower() == username.strip().lower():
                    if is_valid_hash(password, stored_hash):
                        return True, "Welcome back!"
                    break
    return False, "Wrong username or password."      # the same message for both problems, on purpose


def main():
    """A small menu to try it out."""
    while True:
        print("\n1. Register\n2. Log in\n3. Exit")
        choice = input("> ")
        if choice == "3":
            print("Goodbye!")
            break
        if choice in ("1", "2"):
            name = input("Username: ")
            password = input("Password: ")
            if choice == "1":
                ok, message = register_user(name, password)
            else:
                ok, message = login_user(name, password)
            print(("OK: " if ok else "NO: ") + message)


if __name__ == "__main__":
    main()