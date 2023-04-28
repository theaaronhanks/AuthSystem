import tkinter as tk
from client.view.Menu import Menu
import random

class Checklist(Menu):
    def __init__(self, master: tk.Frame, root: tk.Tk) -> None:
        super().__init__(master, "Checklist", root)

        self.__words = [
            "adorn",
            "abdicate",
            "bomb",
            "bjorn",
            "break",
            "cake",
            "cat",
            "fake",
            "zylophone",
            "adorn",
            "abdicate",
            "bomb",
            "bjorn",
            "break",
            "cake",
            "cat",
            "fake",
            "zylophone", 
            "adorn",
            "abdicate",
            "bomb",
            "bjorn",
            "break",
            "cake",
            "cat",
            "fake",
            "zylophone"
        ]
        random.shuffle(self.__words)

        for word in self.__words:
            self.print(word)

        self.__filters = {}
        for ascii_value in range(ord('a'), ord('z') + 1):
            self.__filters.update({chr(ascii_value) : True})


        self.add_option("[X] | Words that start with a", self.filter, 'a')
        self.add_option("[X] | Words that start with b", self.filter, 'b')
        self.add_option("[X] | Words that start with c", self.filter, 'c')
        self.add_option("[X] | Words that start with z", self.filter, 'z')
        self.add_option("[X] | Words that start with f", self.filter, 'f')


    def rerender(self):
        self.clear_display()

        for word in self.__words:
            if not self.__filters[word.lower()[0]]:
                continue

            self.print(word)



    def filter(self, char):
        if self.__filters[char]:
            self.__filters[char] = False
            self.edit_option(self.get_option_index_by_char(char), name = f"[ ] | Words that start with {char}")
        
        else:
            self.__filters[char] = True
            self.edit_option(self.get_option_index_by_char(char), name = f"[X] | Words that start with {char}")

        self.rerender()        

    def get_option_index_by_char(self, char):
        if char == 'a': return 0
        if char == 'b': return 1
        if char == 'c': return 2
        if char == 'z': return 3
        if char == 'f': return 4
