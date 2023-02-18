import tkinter as tk
from client.view.ChangePassword import ChangePassword
from client.view.Menu import Menu
from client.service.api import API

class Personal(Menu):
    def __init__(self, master: tk.Frame, root: tk.Tk, *args, **kwargs) -> None:
        super().__init__(master, "Personal Information", root, *args, **kwargs)

        self.__api = API()
        self.__initialize()

    def __initialize(self):
        self.__populate_user_data()
        self.__populate_edit_options()

    def __populate_user_data(self):
        self.clear_display()

        response = self.__api.get_active_user_info()
        if response["status"] == "error":
            self.set_display("Error getting user info. Please try again later.")
        else: 
            user_info = response["data"]
            self.print("\n")
            self.print("Name: " + user_info["first_name"] + " " + user_info["last_name"])
            self.print("Username: " + user_info["user_name"])
            self.print("Email: " + user_info["email"])
            self.print("Employee ID: " + user_info["id"])
            self.print("Last Login: " + user_info["last_login"])
            self.print("\n")

    def __populate_edit_options(self):
        self.clear_options()
        self.set_options_header("Select an option to edit:")
        self.add_option("Edit Name", self.get_input, 2, "Editing Name", self.__edit_name, "Enter first name", "Enter last name")
        self.add_option("Edit Username", self.get_input, 1, "Editing Username", self.__edit_username, "Enter new username")
        self.add_option("Edit Email", self.get_input, 1, "Editing Email", self.__edit_email, "Enter new email")
        self.add_option("Edit Password", self.__edit_password)

    def __edit_name(self, first_name, last_name):
        self.__api.update_active_user_info("first_name", first_name)
        self.__api.update_active_user_info("last_name", last_name)

    def __edit_username(self, username):
        self.__api.update_active_user_info("user_name", username)

    def __edit_email(self, email):
        self.__api.update_active_user_info("email", email)

    def __edit_password(self):
        cp = ChangePassword(self, self.get_root())
        self.switch_menu(cp, self.__initialize)


