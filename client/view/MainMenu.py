import tkinter as tk
from client.view.Menu import Menu
from client.view.HumanResources import HumanResources
from client.view.AdminMain import AdminMain
from client.view.ChangePassword import ChangePassword
from client.view.Personal import Personal
from client.service.api import API


class MainMenu(Menu):
    def __init__(self, master: tk.Frame, root: tk.Tk, *args, **kwargs) -> None:
        super().__init__(master, "Main", root, *args, **kwargs)

        self.__api = API()
        self.__initialize()

    def __initialize(self):
        self.get_root().title(f"User: {self.__api.get_name()} || Main Menu")
        self.clear_display()
        self.clear_options()
        result = self.__api.user_is_new()
        frames = self.__api.get_frames()

        if result["status"] == "error":
            self.print("Error: Something went wrong. Please logout (Select Back) and try again.")
            return

        if result["new_user"] == "true":
            self.print("Welcome to the system! As a new user, you must change your password before continuing.")
            self.add_option("Change Password", self.__change_password)
        else:
            self.set_display(f"\nWelcome, {self.__api.get_name()}! Select an option below to continue.\n")
            if "admin" in frames:
                self.add_option("Administration", self.__admin)
            if "hr" in frames:
                self.add_option("Human Resources", self.__hr)
            if "add" in frames:
                self.add_option("Add", self.get_input, 2, "Adding 2 numbers", self.__add, "First number", "Second number")
            if "sub" in frames:
                self.add_option("Subtract", self.get_input, 2, "Subtracting 2 numbers", self.__subtract, "First number", "Second number")
            if "mul" in frames:
                self.add_option("Multiply", self.get_input, 2, "Multiplying 2 numbers", self.__multiply, "First number", "Second number")
            if "div" in frames:
                self.add_option("Divide", self.get_input, 2, "Dividing 2 numbers", self.__divide, "First number", "Second number")
            self.add_option("Personal", self.__personal)

    def __admin(self):
        admin = AdminMain(self, self.get_root())
        self.switch_menu(admin, self.__initialize)

    def __hr(self):
        hr = HumanResources(self, self.get_root())
        self.switch_menu(hr, self.__initialize)

    def __add(self, num1: str, num2: str):
        self.__initialize()
        self.set_display("\nAdding...\n")
        self.__calculate("add", num1, num2)      

    def __subtract(self, num1: str, num2: str):
        self.__initialize()
        self.set_display("\nSubtracting...\n")
        self.__calculate("sub", num1, num2)

    def __multiply(self, num1: str, num2: str):
        self.__initialize()
        self.set_display("\nMultiplying...\n")
        self.__calculate("mul", num1, num2)

    def __divide(self, num1: str, num2: str):
        self.__initialize()
        self.set_display("\nDividing...\n")
        self.__calculate("div", num1, num2)

    def __calculate(self, operation: str, num1: str, num2: str):
        result = self.__api.calculate(operation, num1, num2)
        if result["status"] == "error":
            self.print(f"Error: {result['message']}")
        else:
            self.print(f"{num1} {self.__get_op_symbol(operation)} {num2} = {result['result']}")

    def __personal(self):
        personal = Personal(self, self.get_root())
        self.switch_menu(personal, self.__initialize)

    def __change_password(self):
        cp = ChangePassword(self, self.get_root())
        self.switch_menu(cp, self.__initialize)

    def __get_op_symbol(self, operation: str):
        if operation == "add":
            return "+"
        elif operation == "sub":
            return "-"
        elif operation == "mul":
            return "*"
        elif operation == "div":
            return "/"




        