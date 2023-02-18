import tkinter as tk
from client.view.Menu import Menu
from client.service.api import API

class ManageUsers(Menu):
    def __init__(self, master: tk.Frame, root: tk.Tk, *args, **kwargs) -> None:
        super().__init__(master, "Administration", root, *args, **kwargs)

        self.__api = API()
        self.__populate_users()

    def __populate_users(self):
        print(self.__api.get_user_id())
        self.clear_options()
        self.set_options_header("Select a user to edit:")

        result = self.__api.get_users().split()

        for i in result:
            self.add_option(i, self.__edit_user, i)

    def __edit_user(self, username):
        self.__selected_old_user = username
        self.get_input(1, f"Editing user: {username}", self.__process_edit, f"Enter a new username for account: {username}")

    def __process_edit(self, new_username):
        self.set_display("NOTE: Nothing was actually saved" + new_username)
