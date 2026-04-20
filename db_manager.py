import os

USERS_FILE = "users.txt"

def user_saqlash(user_id):
    if not os.path.exists(USERS_FILE):
        open(USERS_FILE, "w").close()

    with open(USERS_FILE, "r") as f:
        azolar = f.read().splitlines()

    if str(user_id) not in azolar:
        with open(USERS_FILE, "a") as f:
            f.write(f"{user_id}\n")