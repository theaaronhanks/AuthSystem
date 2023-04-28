import datetime
import tkinter as tk
from client.view.ChangePassword import ChangePassword
from client.view.Menu import Menu
from client.service.api import API

class HRUserDetails(Menu):
    def __init__(self, master: tk.Frame, root: tk.Tk, user_id: str, *args, **kwargs) -> None:
        super().__init__(master, "HR User Details", root, *args, **kwargs)

        self.__api = API()
        self.__user_id = user_id
        self.__can_edit = True
        self.__roles = {
            "admin" : "Administrator",
            "hr" : "Human Resources",
            "ja" : "Junior Accountant",
            "sa" : "Senior Accountant",
            "je" : "Junior Engineer",
            "se" : "Senior Engineer",
            "math" : "Mathematician"
        }
        self.get_root().title(f"User Details: {self.__api.get_name(user_id=user_id)}")
        self.__initialize()

    def __initialize(self):
        self.__populate_user_data()
        self.__populate_edit_options()

    def __populate_user_data(self):
        self.clear_display()

        response = self.__api.get_user_info(self.__user_id)
        if response["status"] == "error":
            self.set_display("Error getting user info. Please try again later.")
        else: 
            user_info = response["data"]
            self.print("\n")
            self.print("Employee ID: " + user_info["id"])
            self.print("Name: " + user_info["first_name"].capitalize() + " " + user_info["last_name"].capitalize())
            self.print("Username: " + user_info["user_name"])
            role = user_info["role"]
            if role == "admin":
                self.__can_edit = False
            # check privelages
            if role == "hr":
                self.__can_edit = self.__api.check_privelage("admin")
            self.print("Job Title: " + self.__roles[role])
            self.print("Email: " + user_info["email"])
            if user_info["last_login"] == "0":
                self.print("Last Login: Never")
            else:
                date = datetime.datetime.fromtimestamp(int(user_info["last_login"])/1000.0)
                self.print("Last Login: " + date.strftime("%m/%d/%Y, %H:%M:%S"))
            self.print("\n")

    def __populate_edit_options(self):
        self.clear_options()
        if self.__can_edit:
            self.set_options_header("Select an option to edit:")
            self.add_option("Edit Name", self.get_input, 2, "Editing Name", self.__edit_name, "Enter first name", "Enter last name")
            self.add_option("Edit Username", self.get_input, 1, "Editing Username", self.__edit_username, "Enter new username")
            self.add_option("Edit Email", self.get_input, 1, "Editing Email", self.__edit_email, "Enter new email")
            self.add_option("Edit Job Title", self.get_input, 1, "Editing Job Title", self.__edit_job_title, "Enter new job title")
            self.add_option("Remove User", self.__remove_user)


    def __edit_name(self, first_name, last_name):
        first_response = self.__api.update_user_info(self.__user_id, "first_name", first_name)
        last_response = self.__api.update_user_info(self.__user_id, "last_name", last_name)
        self.__populate_user_data()
        self.print(first_response["message"])
        self.print(last_response["message"])

    def __edit_username(self, username):
        self.clear_display()
        response = self.__api.update_user_info(self.__user_id, "user_name", username)
        self.__populate_user_data()
        self.print(response["message"])

    def __edit_email(self, email):
        response = self.__api.update_user_info(self.__user_id, "email", email)
        if response["status"] == "ok":
            self.__populate_user_data()
        self.print(response["message"])

    def __edit_job_title(self, job_title):
        response = self.__api.update_user_info(self.__user_id, "role", job_title)
        if response["status"] == "ok":
            self.__populate_user_data()
        self.print(response["message"])

    def __remove_user(self):
        response = self.__api.remove_user(self.__user_id)
        if response["status"] == "ok":
            self.clear_display()
            self.clear_options()
            self.set_options_header("")
        self.print(response["message"])


