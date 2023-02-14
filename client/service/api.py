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

    # Get the name of the authenticated user
    def get_name(self):
        return controller.get_name(self.__userId)

    # Get the user id of the authenticated user
    def get_user_id(self):
        return self.__userId


    def user_is_new(self):
        return controller.is_new_user(self.__userId)

    # Login a user
    def login(self, user, password):
        user_id = controller.login(user, password)
        if user_id == "error":
            return {"status": "error", "message": "Invalid username or password"}
        else:
            self.__userId = user_id
            return controller.is_new_user(user_id)

    # Change the password of the authenticated user
    def change_password(self, password, confirm_password):
        if password != confirm_password:
            return False
        # if len(password) < 12:
        #     return False
        return controller.change_password(self.__userId, password, confirm_password)


    # Get the list of authorized screens for a user
    # Note: the argument is a hint as to how you need to do things
    def get_frames(self):
        return controller.get_screen_list(self.__userId)

    # Demo to show how to submit data to server
    def demo_option(self, thing1, thing2):
        return controller.demo_option(thing1, thing2)

    # Get list of users
    def get_users(self):
        return controller.get_users()
