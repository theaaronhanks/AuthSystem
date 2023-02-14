import tkinter as tk
from client.view.Menu import Menu
from client.service.api import API

class Personal(Menu):
    def __init__(self, master: tk.Frame, root: tk.Tk, *args, **kwargs) -> None:
        super().__init__(master, "Personal Information", root, *args, **kwargs)

        self.__api = API()
        self.__populate_user_data()
        self.__populate_edit_options()

    def __populate_user_data(self):
        self.clear_display()

        self.print("Name: ")
        self.print("UserName: ")
        self.print("Email:")
        self.print("Employee ID: ")
        self.print("Last Login: ")

    def __populate_edit_options(self):
        self.clear_options()
        self.set_options_header("Select an option to edit:")
        self.add_option("Edit Name", self.__edit_name)
        self.add_option("Edit Username", self.__edit_username)
        self.add_option("Edit Email", self.__edit_email)
        self.add_option("Edit Password", self.__edit_password)

    def __edit_name(self):
        self.get_input(1, "Editing Name", self.__process_edit, "Enter new name")

    def __edit_username(self):
        self.get_input(1, "Editing Username", self.__process_edit, "Enter new username")

    def __edit_email(self):
        self.get_input(1, "Editing Email", self.__process_edit, "Enter new email")

    def __edit_password(self):
        self.get_input(1, "Editing Password", self.__process_edit, "Enter new password")

    def __edit_user(self, username):
        self.__selected_old_user = username
        self.get_input(1, f"Editing user: {username}", self.__process_edit, f"Enter a new username for account: {username}")

    def __process_edit(self, new_username):
        self.set_display("NOTE: Nothing was actually saved")



