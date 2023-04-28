import tkinter as tk
from client.view.Menu import Menu
from client.service.api import API
from client.view.UserDetails import UserDetails

class HumanResources(Menu):
    def __init__(self, master: tk.Frame, root: tk.Tk) -> None:
        super().__init__(master, "Human Resources", root)

        self.__api = API()
        self.get_root().title(f"User: {self.__api.get_name()} || Human Resources")

        self.__roles = ["admin", "hr", "ja", "sa", "je", "se", "math"]
        self.__filters = {}
        for role in self.__roles:
            self.__filters.update({role : True})
        self.__users = []
        
        self.__initialize()

    def __initialize(self):
        self.clear_options()
        self.set_options_header("Select a user to edit:\nUse these filter options to filter the users by role.")
        self.set_filter_options() 
        self.set_user_options()  

    def set_filter_options(self):
        for role in self.__roles:
            self.add_option(f"[{'X' if self.__filters[role] else ' '}] | {self.__get_full_role_name(role)}", self.filter, role)

    def set_user_options(self):
        response = self.__api.get_users()
        if response["status"] == "ok":
            self.__users = response["users"]
        for user in self.__users:
            role = user["role"]
            if role not in self.__roles:
                continue
            if self.__filters[role]:
                self.add_option(f"{user['last_name'].capitalize()}, {user['first_name'].capitalize()} | {user['user_name']} | {self.__get_full_role_name(role)}", self.edit_user, user["id"])
        self.add_option("Add User",self.get_input, 5, "Creating New User", self.add_user, "First Name", "Last Name", "User Name", "Email Address", "Role")

    def rerender(self):
        self.clear_display()
        self.clear_options()

        self.set_filter_options()
        self.set_user_options()

    def filter(self, role):
        self.__filters[role] = not self.__filters[role]
        self.rerender()        

    def __get_full_role_name(self, role):
        if role == "admin": return "Administrator"
        if role == "hr": return "Human Resources"
        if role == "ja": return "Junior Accountant"
        if role == "sa": return "Senior Accountant"
        if role == "je": return "Junior Engineer"
        if role == "se": return "Senior Engineer"
        if role == "math": return "Mathematician"

    def add_user(self, first_name, last_name, user_name, email, role):
        response = self.__api.add_user(first_name, last_name, user_name, email, role)
        self.rerender()
        if response["status"] == "ok":
            self.print("User successfully added. Temporary password is: " + response["password"])
        else:
            self.set_display("\nError: " + response["message"] + "\n")

    def edit_user(self, user_id):
        ud = UserDetails(self, self.get_root(), user_id)
        self.switch_menu(ud, self.__initialize)
