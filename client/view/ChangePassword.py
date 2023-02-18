import tkinter as tk

from client.view.Menu import Menu
from client.service.api import API


class ChangePassword(Menu):
    def __init__(self, master: tk.Frame, root: tk.Tk, *args, **kwargs) -> None:
        super().__init__(master, "Change Password", root, *args, **kwargs)

        self.__api = API()

        self.get_root().title("User: " + self.__api.get_name() + " || Change Password")
        self.add_option("Change Password", self.get_input, 2, "Enter Password", self.__change_password,
                        "Enter new password", "Confirm new password")

    def __change_password(self, new_password, confirm_password):
        message = self.__api.change_password(new_password, confirm_password)
        self.clear_display()
        self.print(message["message"])