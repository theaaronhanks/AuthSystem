import datetime
import tkinter as tk
from client.view.Menu import Menu
from client.service.api import API
import random

class ViewCalcs(Menu):
    def __init__(self, master: tk.Frame, root: tk.Tk) -> None:
        super().__init__(master, "View Calculations", root)

        self.__api = API()
        self.get_root().title(f"User: {self.__api.get_name()} || View Calculations")
        
        self.__operations = ["add", "sub", "mul", "div"]
        self.__calculations = []
        response = self.__api.get_calculations()
        if response["status"] == "ok":
            self.__calculations = response["calculations"]

        self.__filters = {}

        for op in self.__operations:
            self.__filters.update({op : True})

        self.render()
        self.add_option("[X] | Addition Calculations", self.filter, 'add')
        self.add_option("[X] | Subtraction Calculations", self.filter, 'sub')
        self.add_option("[X] | Multiplication Calculations", self.filter, 'mul')
        self.add_option("[X] | Division Calculations", self.filter, 'div')


    def render(self):
        self.clear_display()
        self.set_display("Time | User | Operation | Input1 | Input2 | Result\n\n")

        for calc in self.__calculations:
            op = calc["operation"]
            if op not in self.__operations:
                continue
            if not self.__filters[calc["operation"]]:
                continue

            time = datetime.datetime.fromtimestamp(int(calc["timestamp"])/1000.0)
            self.print(f"{time.strftime('%m/%d/%Y, %H:%M:%S')} | {self.__api.get_name(calc['user_id'])} | {calc['operation']} | {calc['input1']} | {calc['input2']} | {calc['result']}")


    def filter(self, op):
        if self.__filters[op]:
            self.__filters[op] = False
            self.edit_option(self.get_option_index_by_char(op), name = f"[ ] | {self.get_full_op_name(op)} Calculations")
        
        else:
            self.__filters[op] = True
            self.edit_option(self.get_option_index_by_char(op), name = f"[X] | {self.get_full_op_name(op)} Calculations")

        self.render()        

    def get_option_index_by_char(self, op):
        if op == 'add': return 0
        if op == 'sub': return 1
        if op == 'mul': return 2
        if op == 'div': return 3

    def get_full_op_name(self, op):
        if op == "add": return "Addition"
        if op == "sub": return "Subtraction"
        if op == "mul": return "Multiplication"
        if op == "div": return "Division"
