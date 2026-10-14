"""Account storage and validation (no GUI code in this module).

Accounts are saved in accounts.txt, one per line:  username|salt|sha256(salt+password)
User names are unique, ignoring upper/lower case.
"""
import hashlib
import os
import secrets

ACCOUNT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "accounts.txt")


def _hash(password, salt):
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()


def load_accounts():
    """Return {lowercase username: (username, salt, hash)}."""
    accounts = {}
    try:
        with open(ACCOUNT_FILE, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.rstrip("\n").split("|")
                if len(parts) == 3:
                    accounts[parts[0].lower()] = tuple(parts)
    except FileNotFoundError:
        pass
    return accounts


def any_accounts():
    return len(load_accounts()) > 0


def username_exists(username):
    return username.strip().lower() in load_accounts()


def validate_username(username):
    """Return a list of problems (empty list = valid)."""
    problems = []
    username = username.strip()
    if not username:
        problems.append("User name cannot be empty.")
        return problems
    if len(username) < 3:
        problems.append("User name must be at least 3 characters.")
    if "|" in username or " " in username:
        problems.append("User name cannot contain spaces or the '|' character.")
    if not problems and username_exists(username):
        problems.append("That user name is already taken.")
    return problems


def validate_password(password):
    """Return a list of problems (empty list = valid)."""
    problems = []
    if len(password) < 9:
        problems.append("Password must be at least 9 characters.")
    if not any(c.isdigit() for c in password):
        problems.append("Password must contain at least one digit.")
    if not any(c.isupper() for c in password):
        problems.append("Password must contain at least one uppercase letter.")
    if not any(c.islower() for c in password):
        problems.append("Password must contain at least one lowercase letter.")
    if "|" in password or "\n" in password:
        problems.append("Password cannot contain the '|' character.")
    return problems


def create_account(username, password):
    """Validate and save a new account. Returns a list of problems;
    an empty list means the account was created."""
    problems = validate_username(username) + validate_password(password)
    if problems:
        return problems
    username = username.strip()
    salt = secrets.token_hex(8)
    try:
        with open(ACCOUNT_FILE, "a", encoding="utf-8") as f:
            f.write(f"{username}|{salt}|{_hash(password, salt)}\n")
    except OSError as err:
        return [f"Could not save the account: {err}"]
    return []


def verify(username, password):
    """True if the account exists and the password matches."""
    record = load_accounts().get(username.strip().lower())
    if record is None:
        return False
    _, salt, stored = record
    return secrets.compare_digest(_hash(password, salt), stored)
