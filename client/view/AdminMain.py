import tkinter as tk
from client.view.Menu import Menu
from client.view.ViewCalcs import ViewCalcs
from client.view.AdminUsers import AdminUsers
from client.service.api import API


class AdminMain(Menu):
    def __init__(self, master: tk.Frame, root: tk.Tk, *args, **kwargs) -> None:
        super().__init__(master, "Admin Main", root, *args, **kwargs)

        self.__api = API()
        self.__initialize()
        self.get_root().title(f"User: {self.__api.get_name()} || Admin Menu")


    def __initialize(self):
        self.clear_display()
        self.clear_options()

        self.set_display(f"\nWelcome, {self.__api.get_name()}! Select an option below to continue.\n")
        self.add_option("Manage Users", self.__admin_users)
        self.add_option("View Calculations", self.__calculations)

    def __admin_users(self):
        au = AdminUsers(self, self.get_root())
        self.switch_menu(au, self.__initialize)

    def __calculations(self):
        vc = ViewCalcs(self, self.get_root())
        self.switch_menu(vc, self.__initialize)
