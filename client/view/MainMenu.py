import tkinter as tk
from client.view.Menu import Menu
from client.view.Checklist import Checklist
from client.view.ManageUsers import ManageUsers
from client.view.ChangePassword import ChangePassword
from client.view.Personal import Personal
from client.service.api import API


class MainMenu(Menu):
    def __init__(self, master: tk.Frame, root: tk.Tk, username: str) -> None:
        super().__init__(master, "Main", root)

        self.__api = API()
        self.__initialize()

    def __initialize(self):
        self.clear_display()
        self.clear_options()
        if self.__api.user_is_new():
            self.get_root().title(f"User: ") #{username}")
            self.print("Welcome to the system! As a new user, you must change your password before continuing.")
            self.add_option("Change Password", self.__change_password)
        else:
            self.get_root().title(f"User: ") #{username}")
            self.add_option("Example checklist/filtering", self.__check)
            self.add_option("Example IO", self.get_input, 1, "Example io", self.__io,
                            "Enter the number of input prompts to test")
            self.add_option("Manage Users", self.__manage_users)
            self.add_option("Administration", self.__admin)
            self.add_option("Human Resources", self.__hr)
            self.add_option("Add", self.__add)
            self.add_option("Subtract", self.__subtract)
            self.add_option("Multiply", self.__multiply)
            self.add_option("Divide", self.__divide)
            self.add_option("Personal", self.__personal)
            self.rename_back_option("Logout")

    def __io(self, number_of_prompts: str):
        num = int(number_of_prompts)

        self.get_input(num, f"Testing with {num} inputs", self.__io1, *[f"Prompt #{i}" for i in range(num)])

    def __io1(self, *inputs):
        self.clear_display()
        self.print(f"You asked for {len(inputs)} inputs")
        
        for answer_index in range(len(inputs)):
            self.print(f"\tInput #{answer_index}:")
            self.print(f"\t\t{inputs[answer_index]}")

    def __check(self):
        check = Checklist(self, self.get_root())
        self.switch_menu(check)

    def __manage_users(self):
        mu = ManageUsers(self, self.get_root())
        self.switch_menu(mu)

    def __admin(self):
        pass

    def __hr(self):
        pass

    def __add(self):
        pass

    def __subtract(self):
        pass

    def __multiply(self):
        pass

    def __divide(self):
        pass

    def __personal(self):
        personal = Personal(self, self.get_root())
        self.switch_menu(personal)

    def __change_password(self):
        cp = ChangePassword(self, self.get_root())
        self.switch_menu(cp, self.__initialize())

    def __logout(self):
        pass



        