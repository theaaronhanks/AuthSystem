# This module acts like the server. Queries come in as function calls and
# something is returned. You should probably have it return: numbers, strings,
# dictionaries, lists, or JSON. Let the client side change that into data objects
# if necessary.
import datetime
import random
import time
from enum import Enum
import uuid
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

class CalculationFields(Enum):
    TIMESTAMP = 0
    USER_ID = 1
    INPUT1 = 2
    INPUT2 = 3
    OPERATION = 4
    RESULT = 5


ROLES = ["admin", "hr", "ja", "sa", "je", "se", "math"]


def check_privelage(user_id, action):
    privelages = __get_access_list(user_id)
    if action in privelages:
        return {"status": "ok"}
    else:
        return {"status": "error", "message": "You do not have permission to do that"}


def __get_access_list(user_id):
    user = __get_user_data(user_id)
    if "error" in user:
        return []
    role = user["role"]
    privelages = []
    with open("server/data/access.txt", "r") as f:
        for line in f:
            items = line.strip().split(",")
            if len(items) < 2:
                continue
            if items[0] == role:
                privelages = items[1:]
                break
    return privelages


def login(user, password):
    with open("server/data/passwd.txt", "r") as f:
        for line in f:
            items = line.strip().split(",")
            if len(items) < len(list(PasswordFields)):
                continue
            if items[PasswordFields.USER_NAME.value] == user:
                if bcrypt.checkpw(password.encode('utf-8'), items[PasswordFields.PASSWORD_HASH.value].encode('utf-8')):
                    __edit_user_data(items[PasswordFields.ID.value], UserFields.LAST_LOGIN, round(time.time() * 1000))
                    __log_action(items[PasswordFields.ID.value], "login", "success")
                    return items[PasswordFields.ID.value]
    __log_action("unknown", "login", "failed")
    return "error"


def change_password(user_id, password, confirm_password):
    if password != confirm_password:
        return {"status": "error", "message": "Passwords do not match"}
    if len(password) < 12:
        return {"status": "error", "message": "Password must be at least 12 characters"}
    upper = False
    lower = False
    digit = False
    special = False
    for char in password:
        if char.isupper():
            upper = True
            continue
        if char.islower():
            lower = True
            continue
        if char.isdigit():
            digit = True
            continue
        if char in "!@#$%^&*()":
            special = True
            continue
    if upper and lower and digit and special:
        changed = __set_password(user_id, password)
        
        if changed: 
            __edit_user_data(user_id, UserFields.NEW_USER, "false")
            __log_action(user_id, "change_password", "success")
            return {"status": "ok", "message": "Password successfully changed"}
        else:
            return {"status": "error", "message": "Password change failed. Please try again."}
    else:
        __log_action(user_id, "change_password", "failed")
        return {"status": "error", "message": "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character."}
        

def __set_password(user_id, password):
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    return __edit_password_data(user_id, PasswordFields.PASSWORD_HASH, password_hash)


def get_screen_list(user_id):
    return __get_access_list(user_id)


def get_user_data(user_id):
    user_data = __get_user_data(user_id)
    if "error" in user_data:
        return {"status": "error"}
    else:
        return {"status": "ok", "data": user_data}


def __get_user_data(user_id):
    with open("server/data/users.txt", "r") as f:
        lines = f.readlines()
    for line in lines:
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

def __verify_first_name(first_name):
    if len(first_name) < 1:
        return False
    if len(first_name) > 20:
        return False
    if not first_name.isalpha():
        return False
    return True
    

def __verify_last_name(last_name):
        if len(last_name) < 1:
            return False
        if len(last_name) > 20:
            return False
        if not last_name.isalpha():
            return False
        return True

def __verify_user_name(user_name):
    if len(user_name) < 1:
        return False
    if len(user_name) > 20:
        return False
    if not user_name.isalnum():
        return False
    if user_name[0].isdigit():
        return False
    with open("server/data/users.txt", "r") as f:
        for line in f:
            items = line.strip().split(",")
            if len(items) < len(list(UserFields)):
                continue
            if items[UserFields.USER_NAME.value] == user_name:
                return False
    return True
    

def __verify_email(email):
    if len(email) < 1:
        return False
    if len(email) > 50:
        return False
    if "@" not in email or "." not in email or email.index("@") > email.index(".") or email.index(".") == len(email) - 1:
        return False
    with open("server/data/users.txt", "r") as f:
        for line in f:
            items = line.strip().split(",")
            if len(items) < len(list(UserFields)):
                continue
            if items[UserFields.EMAIL.value] == email:
                return False
    return True

def __verify_role(role, user_id):
    if role not in ROLES:
        return False
    if role == "admin":
        return False
    if role == "hr":
        return check_privelage(user_id, "admin")["status"] == "ok"
    return True


def edit_user_data(actor_user_id, user_id, field, value):
    if actor_user_id != user_id:
        check = check_privelage(actor_user_id, "admin")
        if check["status"] == "error":
            check = check_privelage(actor_user_id, "hr")
            if check["status"] == "error":
                return {"status": "error", "message": "You do not have permission to edit user data"}
    value = value.strip()
    if field == "first_name":
        if not __verify_first_name(value):
            __log_action(actor_user_id, f"edit first name for {user_id}", "failed")
            return {"status": "error", "message": "First name must be between 1 and 20 characters and only contain letters"}
        if __edit_user_data(user_id, UserFields.FIRST_NAME, value):
            __log_action(actor_user_id, f"edit first name for {user_id}", "success")
            return {"status": "ok", "message": "First name successfully changed"}
    elif field == "last_name":
        if not __verify_last_name(value):
            __log_action(actor_user_id, f"edit last name for {user_id}", "failed")
            return {"status": "error", "message": "Last name must be between 1 and 20 characters and only contain letters"}
        if __edit_user_data(user_id, UserFields.LAST_NAME, value):
            __log_action(actor_user_id, f"edit last name for {user_id}", "success")
            return {"status": "ok", "message": "Last name successfully changed"}
    elif field == "user_name":
        if not __verify_user_name(value):
            __log_action(actor_user_id, f"edit username for {user_id}", "failed")
            return {"status": "error", "message": "Username must be between 1 and 20 characters and only contain letters and numbers, and cannot start with a number"}
        if __edit_user_data(user_id, UserFields.USER_NAME, value):
            if __edit_password_data(user_id, PasswordFields.USER_NAME, value):
                __log_action(actor_user_id, f"edit username for {user_id}", "success")
                return {"status": "ok", "message": "Username successfully changed"}
            else:
                __log_action(actor_user_id, f"edit username for {user_id}", "failed")
                return {"status": "error", "message": "Username change failed. Please try again."}
    elif field == "email":
        if not __verify_email(value):
            __log_action(actor_user_id, f"edit email for {user_id}", "failed")
            return {"status": "error", "message": "Invalid email"}
        if __edit_user_data(user_id, UserFields.EMAIL, value):
            __log_action(actor_user_id, f"edit email for {user_id}", "success")
            return {"status": "ok", "message": "Email successfully changed"}
    elif field == "role":
        if not __verify_role(value, actor_user_id):
            __log_action(actor_user_id, f"edit role for {user_id}", "failed")
            return {"status": "error", "message": "Invalid role"}
        if __edit_user_data(user_id, UserFields.ROLE, value):
            __log_action(actor_user_id, f"edit role for {user_id}", "success")
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
                items[field.value] = value
                f.write(f"{items[PasswordFields.ID.value]},"
                        f"{items[PasswordFields.USER_NAME.value]},"
                        f"{items[PasswordFields.PASSWORD_HASH.value]}\n")
                edited = True
            else:
                f.write(line)
    return edited


def get_name(user_id):
    user_data = __get_user_data(user_id)
    if "error" in user_data:
        return {"status": "error"}
    else:
        return {"status": "ok", "name": user_data["user_name"]} 

def is_new_user(user_id):
    user_data = __get_user_data(user_id)
    if "error" in user_data:
        return {"status": "error"}
    else:
        if user_data["new_user"] == "false":
            return {"status": "ok", "new_user": "false"}
        else:
            return {"status": "ok", "new_user": "true"}
            

def calculate(user_id, operation: str, input1: str, input2: str):
    try:
        num1 = float(input1)
        num2 = float(input2)
    except ValueError:
        __log_action(user_id, "calculate", "failed")
        return {"status": "error", "message": "Invalid input"}
    if operation == "add":
        check = check_privelage(user_id, "add")
        if check["status"] == "error":
            __log_action(user_id, "calculate", "failed")
            return check
        result = num1 + num2
    elif operation == "sub":
        check = check_privelage(user_id, "sub")
        if check["status"] == "error":
            __log_action(user_id, "calculate", "failed")
            return check
        result = num1 - num2
    elif operation == "mul":
        check = check_privelage(user_id, "mul")
        if check["status"] == "error":
            __log_action(user_id, "calculate", "failed")
            return check
        result = num1 * num2
    elif operation == "div":
        check = check_privelage(user_id, "div")
        if check["status"] == "error":
            __log_action(user_id, "calculate", "failed")
            return check
        if num2 == 0:
            __log_action(user_id, "calculate", "failed")
            return {"status": "error", "message": "Cannot divide by zero"}
        result = num1 / num2
    else:
        __log_action(user_id, "calculate", "failed")
        return {"status": "error", "message": "Invalid operation"}
    with open("server/data/calcs.txt", "a") as f:
        f.write(f"{round(time.time() * 1000)},"
                f"{user_id},"
                f"{input1},"
                f"{input2},"
                f"{operation},"
                f"{result}\n")
    __log_action(user_id, "calculate", "success")
    return {"status": "ok", "result": result}

def get_calculations(user_id):
    check = check_privelage(user_id, "admin")
    if check["status"] == "error":
        __log_action(user_id, "get calculations", "failed")
        return check
    calculations = []
    with open("server/data/calcs.txt", "r") as f:
        lines = f.readlines()
    for line in lines:
        items = line.strip().split(",")
        if len(items) < len(list(CalculationFields)):
            continue
        calculations.append({
                "timestamp": items[CalculationFields.TIMESTAMP.value],
                "user_id": items[CalculationFields.USER_ID.value],
                "input1": items[CalculationFields.INPUT1.value],
                "input2": items[CalculationFields.INPUT2.value],
                "operation": items[CalculationFields.OPERATION.value],
                "result": items[CalculationFields.RESULT.value],
            })
    if len(calculations) == 0:
        __log_action(user_id, "get calculations", "failed")
        return {"status": "error", "message": "Unable to retrieve calculations"}
    else:
        __log_action(user_id, "get calculations", "success")
        return {"status": "ok", "calculations": calculations}

def get_users(user_id):
    check = check_privelage(user_id, "admin")
    if check["status"] == "error":
        check = check_privelage(user_id, "hr")
        if check["status"] == "error":
            __log_action(user_id, "get users", "failed")
            return check
    users = []
    with open("server/data/users.txt", "r") as f:
        lines = f.readlines()
    for line in lines:
        items = line.strip().split(",")
        if len(items) < len(list(UserFields)):
            continue
        users.append({
                "id": items[UserFields.ID.value],
                "user_name": items[UserFields.USER_NAME.value],
                "first_name": items[UserFields.FIRST_NAME.value],
                "last_name": items[UserFields.LAST_NAME.value],
                "email": items[UserFields.EMAIL.value],
                "role": items[UserFields.ROLE.value],
                "new_user": items[UserFields.NEW_USER.value],
                "last_login": items[UserFields.LAST_LOGIN.value]
            })
    if len(users) == 0:
        __log_action(user_id, "get users", "failed")
        return {"status": "error", "message": "Unable to retrieve users"}
    else:
        __log_action(user_id, "get users", "success")
        return {"status": "ok", "users": users}


def add_user(actor_user_id, first_name, last_name, user_name, email, role):
    if role == "hr":
        check = check_privelage(actor_user_id, "admin")
    else:
        check = check_privelage(actor_user_id, "hr")
    if check["status"] == "error":
        __log_action(actor_user_id, "add user", "failed")
        return check
    user_id = str(uuid.uuid4())

    if not __verify_first_name(first_name):
        return {"status": "error", "message": "Invalid first name"}
    if not __verify_last_name(last_name):
        return {"status": "error", "message": "Invalid last name"}
    if not __verify_user_name(user_name):
        return {"status": "error", "message": "Invalid user name"}
    if not __verify_email(email):
        return {"status": "error", "message": "Invalid email"}
    if not __verify_role(role, actor_user_id):
        return {"status": "error", "message": "Invalid role"}

    lowers = [chr(i) for i in range(ord('a'),ord('z')+1)]
    uppers = [chr(i) for i in range(ord('A'),ord('Z')+1)]
    digits = [chr(i) for i in range(ord('0'),ord('9')+1)]
    specials = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')' ]
    characters = lowers + uppers + digits + specials
    password = ""
    for i in range(0, 13):
        password += random.choice(characters)

    with open("server/data/passwd.txt", "a") as f:
        f.write(f"{user_id},{user_name},\n")
    if not __set_password(user_id, password):
        remove_user(user_id)
        return {"status": "error", "message": "Unable to set password"}
    with open("server/data/users.txt", "a") as f:
        f.write(f"{user_id},{user_name},{first_name},{last_name},{email},{role},true,0\n")
    __log_action(actor_user_id, "add user", "success")
    return {"status": "ok", "user_id": user_id, "password": password}

def remove_user(actor_user_id, user_id):
    role = get_user_data(user_id)["data"]["role"]
    if role == "hr":
        check = check_privelage(actor_user_id, "admin")
    else:
        check = check_privelage(actor_user_id, "hr")
    if check["status"] == "error":
        __log_action(actor_user_id, "remove user", "failed")
        return check
    removed = False
    with open("server/data/users.txt", "r") as f:
        lines = f.readlines()
    with open("server/data/users.txt", "w") as f:
        for line in lines:
            items = line.strip().split(",")
            if len(items) < len(list(UserFields)):
                continue
            if items[UserFields.ID.value] == user_id:
                removed = True
            else:
                f.write(line)
    if removed:
        with open("server/data/passwd.txt", "r") as f:
            lines = f.readlines()
        with open("server/data/passwd.txt", "w") as f:
            for line in lines:
                items = line.strip().split(",")
                if len(items) < len(list(PasswordFields)):
                    continue
                if items[PasswordFields.ID.value] != user_id:
                    f.write(line)
        __log_action(actor_user_id, "remove user", "success")
        return {"status": "ok", "message": "User successfully removed"}
    else:
        __log_action(actor_user_id, "remove user", "failed")
        return {"status": "error", "message": "Unable to remove user"}


def __log_action(user_id, log_message, log_status):
    with open("server/data/logs.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} || "
                f"{user_id} performed action: "
                f"{log_message} || Status: "
                f"{log_status} \n")
