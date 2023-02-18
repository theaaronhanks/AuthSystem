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
    EMAIL = 4
    ROLE = 5
    NEW_USER = 6
    LAST_LOGIN = 7


class PasswordFields(Enum):
    ID = 0
    USER_NAME = 1
    PASSWORD_HASH = 2


ROLES = ["admin", "hr", "ja", "sa", "je", "se", "math"]

def login(user, password):
    with open("server/data/passwd.txt", "r") as f:
        for line in f:
            items = line.strip().split(",")
            if len(items) < len(list(PasswordFields)):
                continue
            if items[PasswordFields.USER_NAME.value] == user:
                if bcrypt.checkpw(password.encode('utf-8'), items[PasswordFields.PASSWORD_HASH.value].encode('utf-8')):
                    __edit_user_data(items[PasswordFields.ID.value], UserFields.LAST_LOGIN, round(time.time() * 1000))
                    return items[0]
    return "error"


def change_password(user_id, password, confirm_password):
    if password != confirm_password:
        return {"status": "error", "message": "Passwords do not match"}
    # if len(password) < 12:
    #     return {"status": "error", "message": "Password must be at least 12 characters"}
    found = False
    
    if found:
        __edit_user_data(user_id, UserFields.NEW_USER, "false")
        return {"status": "ok", "message": "Password successfully changed"}
    else:
        return {"status": "error", "message": "Password change failed. Please try again."}


def logout():
    pass


def get_user_data(user_id):
    user_data = __get_user_data(user_id)
    if "error" in user_data:
        return {"status": "error"}
    else:
        return {"status": "ok", "data": user_data}


def __get_user_data(user_id):
    with open("server/data/users.txt", "r") as f:
        for line in f:
            items = line.strip().split(",")
            if len(items) < len(list(UserFields)):
                # log error {"error": "User data corrupted or incomplete"}
                continue
            if items[UserFields.ID.value] == user_id:
                user_data = {
                    "id": items[UserFields.ID.value],
                    "user_name": items[UserFields.USER_NAME.value],
                    "first_name": items[UserFields.FIRST_NAME.value],
                    "last_name": items[UserFields.LAST_NAME.value],
                    "email": items[UserFields.EMAIL.value],
                    "role": items[UserFields.ROLE.value],
                    "new_user": items[UserFields.NEW_USER.value],
                    "last_login": items[UserFields.LAST_LOGIN.value]
                }
                return user_data
    return {"error": "User not found"}


def edit_user_data(user_id, field, value):
    value = value.strip()
    if field == "first_name":
        if len(value) < 1:
            return {"status": "error", "message": "First name must be at least 1 character"}
        if len(value) > 20:
            return {"status": "error", "message": "First name must be less than 20 characters"}
        if not value.isalpha():
            return {"status": "error", "message": "First name must only contain letters"}
        if __edit_user_data(user_id, UserFields.FIRST_NAME, value):
            return {"status": "ok", "message": "First name successfully changed"}
    elif field == "last_name":
        if len(value) < 1:
            return {"status": "error", "message": "Last name must be at least 1 character"}
        if len(value) > 20:
            return {"status": "error", "message": "Last name must be less than 20 characters"}
        if not value.isalpha():
            return {"status": "error", "message": "Last name must only contain letters"}
        if __edit_user_data(user_id, UserFields.LAST_NAME, value):
            return {"status": "ok", "message": "Last name successfully changed"}
    elif field == "user_name":
        if len(value) < 1:
            return {"status": "error", "message": "Username must be at least 1 character"}
        if len(value) > 20:
            return {"status": "error", "message": "Username must be less than 20 characters"}
        if not value.isalnum():
            return {"status": "error", "message": "Username must only contain letters and numbers"}
        if __edit_user_data(user_id, UserFields.USER_NAME, value):
            return {"status": "ok", "message": "Username successfully changed"}
    elif field == "email":
        if len(value) < 1:
            return {"status": "error", "message": "Email must be at least 1 character"}
        if len(value) > 50:
            return {"status": "error", "message": "Email must be less than 50 characters"}
        if "@" not in value or "." not in value or value.index("@") > value.index(".") or value.index(".") == len(value) - 1:
            return {"status": "error", "message": "Email must be a valid email address"}
        if __edit_user_data(user_id, UserFields.EMAIL, value):
            return {"status": "ok", "message": "Email successfully changed"}
    elif field == "role":
        # todo: check if user has hr permissions
        if value not in ROLES:
            return {"status": "error", "message": "Invalid role"}
        if __edit_user_data(user_id, UserFields.ROLE, value):
            return {"status": "ok", "message": "Role successfully changed"}
    else:
        return {"status": "error", "message": "Invalid field. Modification forbidden."}


def __edit_user_data(user_id, field, value):
    edited = False
    with open("server/data/users.txt", "r") as f:
        lines = f.readlines()
    with open("server/data/users.txt", "w") as f:
        for line in lines:
            items = line.strip().split(",")
            if len(items) < len(list(UserFields)):
                continue
            if items[UserFields.ID.value] == user_id:
                items[field.value] = value
                f.write(f"{items[UserFields.ID.value]},"
                        f"{items[UserFields.USER_NAME.value]},"
                        f"{items[UserFields.FIRST_NAME.value]},"
                        f"{items[UserFields.LAST_NAME.value]},"
                        f"{items[UserFields.EMAIL.value]},"
                        f"{items[UserFields.ROLE.value]},"
                        f"{items[UserFields.NEW_USER.value]},"
                        f"{items[UserFields.LAST_LOGIN.value]}\n")
                edited = True
            else:
                f.write(line)
    return edited


def __edit_password_data(user_id, field, value):
    value = value.strip()
    edited = False
    with open("server/data/passwd.txt", "r") as f:
        lines = f.readlines()
    with open("server/data/passwd.txt", "w") as f:
        for line in lines:
            items = line.strip().split(",")
            if len(items) < len(list(PasswordFields)):
                # todo: log error
                continue
            if items[PasswordFields.ID.value] == user_id:
                new_line = f"{items[PasswordFields.ID.value]},"
                if field == "user_name":
                    new_line += f"{value},"
                else:
                    new_line += f"{items[PasswordFields.USER_NAME.value]},"
                if field == "password_hash":
                    new_line += f"{bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')}\n"
                else:
                    new_line += f"{items[PasswordFields.PASSWORD_HASH.value]}\n"
                f.write(new_line)
                edited = True
            else:
                f.write(line)
    return edited



def get_name(user_id):
    return "bob"
    pass


def is_new_user(user_id):
    user_data = __get_user_data(user_id)
    if "error" in user_data:
        return {"status": "error"}
    else:
        if user_data["new_user"] == "false":
            return {"status": "ok", "new_user": "false"}
        else:
            return {"status": "ok", "new_user": "true"}


def demo_option(thing1, thing2):
    return float(thing1) + float(thing2)

def calculate(user_id, operation: str, input1: str, input2: str):
    try:
        num1 = float(input1)
        num2 = float(input2)
    except ValueError:
        return {"status": "error", "message": "Invalid input"}
    if operation == "add":
        result = num1 + num2
    elif operation == "subtract":
        result = num1 - num2
    elif operation == "multiply":
        result = num1 * num2
    elif operation == "divide":
        if num2 == 0:
            return {"status": "error", "message": "Cannot divide by zero"}
        result = num1 / num2
    else:
        return {"status": "error", "message": "Invalid operation"}
    return {"status": "ok", "result": result}


def get_users():
    return "Alice Bob Charlie Denise"