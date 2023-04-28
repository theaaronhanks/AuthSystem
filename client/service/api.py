import server.controller.controller as controller # Fake network connection to server


class API:
    instance = None

    # Singleton management. This is called before __init__
    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        if self.instance is not None:
            return
        self.__userId = None  # The authenticated user id

########################################################
# All Function calls will make a call on the controller
# and return to the view that called it
########################################################

    def check_privelage(self, action):
        response = controller.check_privelage(self.__userId, action)
        return response["status"] == "ok"

    # Get the name of the authenticated user
    def get_name(self, user_id=None):
        if user_id is not None and self.check_privelage("hr"):
            response = controller.get_name(user_id)
        else:
            response = controller.get_name(self.__userId)
        if response["status"] == "ok":
            return response["name"]
        else:
            return "Unknown"

    # Get the user id of the authenticated user
    def get_user_id(self):
        return self.__userId

    # Check if the authenticated user is new
    def user_is_new(self):
        return controller.is_new_user(self.__userId)

    # Login a user
    def login(self, user, password):
        user_id = controller.login(user, password)
        if user_id == "error":
            return {"status": "error", "message": "Invalid username or password"}
        else:
            self.__userId = user_id
            return {"status": "ok", "message": "Login successful"}

    # Change the password of the authenticated user
    def change_password(self, password, confirm_password):
        return controller.change_password(self.__userId, password, confirm_password)

    # Get the list of authorized screens for a user
    # Note: the argument is a hint as to how you need to do things
    def get_frames(self):
        return controller.get_screen_list(self.__userId)

    def calculate(self, operation, num1, num2):
        if operation == "add":
            can_calc = self.check_privelage("add")
        elif operation == "sub":
            can_calc = self.check_privelage("sub")
        elif operation == "mul":
            can_calc = self.check_privelage("mul")
        elif operation == "div":
            can_calc = self.check_privelage("div")
        if can_calc:
            return controller.calculate(self.__userId, operation, num1, num2)
        else:
            return {"status": "error", "message": "You do not have permission to do that"}

    def get_active_user_info(self):
        return controller.get_user_data(self.__userId)

    def get_user_info(self, user_id):
        if self.check_privelage("hr") or self.check_privelage("admin"):
            return controller.get_user_data(user_id)
        else:
            return {"status": "error", "message": "You do not have permission to do that"}

    def update_active_user_info(self, field, value):
        return controller.edit_user_data(self.__userId, self.__userId, field, value)

    def update_user_info(self, user_id, field, value):
        if self.check_privelage("hr") or self.check_privelage("admin"):
            return controller.edit_user_data(self.__userId, user_id, field, value)
        return {"status": "error", "message": "You do not have permission to do that"}

    def get_calculations(self):
        if self.check_privelage("admin"):
            return controller.get_calculations(self.__userId)
        return {"status": "error", "message": "You do not have permission to do that"}

    # Get list of users
    def get_users(self):
        if self.check_privelage("hr") or self.check_privelage("admin"):
            return controller.get_users(self.__userId)
        return {"status": "error", "message": "You do not have permission to do that"}

    def add_user(self, first_name, last_name, user_name, email, role):
        if role == "hr" and not self.check_privelage("admin"):
            return {"status": "error", "message": "You do not have permission to do that"}
        elif not self.check_privelage("hr"):
            return {"status": "error", "message": "You do not have permission to do that"}
        return controller.add_user(self.__userId, first_name, last_name, user_name, email, role)

    def remove_user(self, user_id):
        response = controller.get_user_data(user_id)
        if response["status"] == "error":
            return response
        role = response["data"]["role"]
        if role == "hr" and not self.check_privelage("admin"):
            return {"status": "error", "message": "You do not have permission to do that"}
        elif not self.check_privelage("hr"):
            return {"status": "error", "message": "You do not have permission to do that"}
        return controller.remove_user(self.__userId, user_id)
