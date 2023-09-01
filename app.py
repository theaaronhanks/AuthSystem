import sys
import os
sys.path.append(os.getcwd())

import tkinter as tk
from client.view.Login import Login

class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        login = Login(self, self)


app = App()
app.mainloop()