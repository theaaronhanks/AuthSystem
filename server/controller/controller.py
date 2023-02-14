# This module acts like the server. Queries come in as function calls and
# something is returned. You should probably have it return: numbers, strings,
# dictionaries, lists, or JSON. Let the client side change that into data objects
# if necessary.
import time
from enum import Enum

import bcrypt

class UserFields(Enum):
    ID = 0
    USER_NAME = 1
    FIRST_NAME = 2
    LAST_NAME = 3
    ROLE = 4
    NEW_USER = 5

def login(user, password):
    with open("../server/data/passwd.txt", "r") as f:
        for line in f:
            items = line.strip().split(",")
            if len(items) < 3:
                continue
            if items[1] == user:
                if bcrypt.checkpw(password.encode('utf-8'), items[2].encode('utf-8')):
                    # __add_session(items[0])
                    return items[0]
    return "error"


def change_password(user_id, password, confirm_password):
    if password != confirm_password:
        return False
    # if len(password) < 12:
    #     return False
    found = False
    with open("../server/data/passwd.txt", "r") as f:
        lines = f.readlines()
    with open("../server/data/passwd.txt", "w") as f:
        for line in lines:
            items = line.strip().split(",")
            if len(items) < 3:
                # todo: log error
                continue
            if items[0] == user_id:
                f.write(f"{items[0]},{items[1]},{bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')}\n")
                found = True
            else:
                f.write(line)
    if found:
        __edit_user_data(user_id, UserFields.NEW_USER, "false")
    return found


def logout():
    pass


def __get_user_data(user_id):
    with open("../server/data/users.txt", "r") as f:
        for line in f:
            items = line.strip().split(",")
            if items[0] == "":
                return {"error": "User not found"}
            if len(items) < 6:
                return {"error": "User data corrupted"}
            if items[0] == user_id:
                user_data = {
                    "id": items[0],
                    "user_name": items[1],
                    "first_name": items[2],
                    "last_name": items[3],
                    "role": items[4],
                    "new_user": items[5],
                }
                print(user_data)
                return user_data

def __edit_user_data(user_id, field, value):
    edited = False
    with open("../server/data/users.txt", "r") as f:
        lines = f.readlines()
    with open("../server/data/users.txt", "w") as f:
        for line in lines:
            items = line.strip().split(",")
            if len(items) < 6:
                continue
            if items[0] == user_id:
                items[field.value] = value
                f.write(f"{items[0]},{items[1]},{items[2]},{items[3]},{items[4]},{items[5]}\n")
                edited = True
            else:
                f.write(line)
    return edited


def get_name(userId):
    return "bob"
    pass


def is_new_user(user_id):
    user_data = __get_user_data(user_id)
    if "error" in user_data:
        # todo: log error
        return {"status": "error", "message": "Invalid username or password"}
    else:
        if user_data["new_user"] == "true":
            return {"status": "ok", "new_user": "true"}
        else:
            return {"status": "ok", "new_user": "false"}


def demo_option(thing1, thing2):
    return float(thing1) + float(thing2)


def get_users():
    return "Alice Bob Charlie Denise"