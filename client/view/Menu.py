import tkinter as tk
from typing import Callable, Any


class Menu(tk.Frame):
    """
    Represents an available text menu and display for tkinter. 
    Menu's can display options from the user to select from, 
    have a read only display area, get input, and switch to and from other Menus.
    """
    class MenuOption:
        """
        Wrapper around a string and a callback function.
        Represents one selectable option available to a user in a menu.
        """
        def __init__(self, name: str, callback: Callable, *args, **kwargs) -> None:
            self.__name: str = name #the displayed text for the option
            self.__callback: Callable = callback #the callback to call when the option is selected
            self.__callback_args: tuple = args #the positional args to pass to the callback
            self.__callback_kwargs: dict[str, Any] = kwargs #the keyword args to pass to the callback

        def __str__(self) -> str:
            return self.__name

        def __call__(self, *args, **kwds) -> Any:
            #ignore the args and kwargs passed at calltime, instead use the args and kwargs set beforehand
            return self.__callback(*self.__callback_args, **self.__callback_kwargs)

        def set_name(self, name: str) -> None:
            """
            @param name: str
                The displayed text for the menu option
            """
            self.__name = name

        def set_callback(self, callback: Callable) -> None:
            """
            @param callback: Callable
                The function to call when the option is selected by the end user
            """
            self.__callback = callback

        def set_args(self, *args) -> None:
            """
            @param *args
                The positional arguements to pass to the callback when it is called
            """
            self.__callback_args = args
        
        def set_kwargs(self, **kwargs) -> None:
            """
            @param **kwargs
                The keyword arguements to pass to the callback when it is called
            """
            self.__callback_kwargs = kwargs


    def __init__(self, master: tk.Frame, title: str, root: tk.Tk, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.__root: tk.Tk = root #a root window
        self.__title: str = title #the title for the menu

        self.__back_option: Menu.MenuOption | None = None #persistent option when set to return to the previous menu
        self.__options: list[Menu.MenuOption] = [] #list of menu options for the user to select from
        self.__selected: int = 0 #index of the currently selected option

        self.__input_texts: list[tk.Entry] = [] #future list of text entries for getting input
        self.__input_text_window: tk.Toplevel | None = None #future window for getting input
        self.__input_text_callback: Callable | None = None #future callback to call after receiving input

        self.__text_display: str = "" #string that gets displayed in the read only display
        self.__options_header: str = "****Options****" #optional header that separates the read only display from the selectable options

        self.__on_return_to_menu_callback: Callable | None = None #optional callback that gets called when returning to this menu from a submenu

        self.__text__init()

    def set_options_header(self, header: str) -> None:
        """
        @param header: str
            Set the optional header that separates the read only display from the selectable options
        """
        self.__options_header = header

    def add_option(self, name: str, callback: Callable, *args, **kwargs) -> None:
        """
        @param name: str
            The text to display for the option
        @param callback: Callable
            The function to call when the option is selected
        @param *args
            The positional args to pass to the callback
        @param **kwargs
            The keyword arguements to pass to the callback
        
        Adds a new MenuOption to the current menu that the user can select from
        """
        self.__options.append(Menu.MenuOption(name, callback, *args, **kwargs))
        self.draw()

    def delete_option(self, index: int) -> str:
        """
        @param index: int
            The index of the MenuOption to delete from the current menu
        @returns str
            The name of the deleted option

        Deletes the option at index from the current menu
        """
        op = self.__options.pop(index)
        self.draw()
        return op.__name

    def insert_option(self, index: int, name: str, callback: Callable, *args, **kwargs) -> None:
        """
        @param index: int
            The position to insert the option before
        @param name: str
            The text to display for the option
        @param callback: Callable
            The function to call when the option is selected
        @param *args
            The positional args to pass to the callback
        @param **kwargs
            The keyword arguements to pass to the callback
        
        Inserts a new MenuOption to the current menu that the user can select from before the postition index
        """
        self.__options.insert(index, Menu.MenuOption(
            name, callback, *args, **kwargs))
        self.draw()

    def edit_option(self, index: int, name: str | None = None, callback: Callable | None = None, *args, **kwargs) -> None:
        """
        @param index: int
            The position of the option to modify
        @param name: str | None = None
            The optional new name for the option
        @param callback: Callable | None = None
            The optional new callback for the option
        @param *args
            The optional new positional args for the callback
        @param **kwargs
            The optional new keyword args for the callback
        
        Edits the option at position index. If a parameter is not passed, it defaults to None and that specific field is not updated in the option.
        """
        option = self.__options[index]
        if name is not None:
            option.set_name(name)

        if callback is not None:
            option.set_callback(callback)

        if args is not None and len(args) > 0:
            option.set_args(args)

        if kwargs is not None and len(kwargs) > 0:
            option.set_kwargs(kwargs)
        self.draw()

    def rename_back_option(self, name: str | None = None) -> None:
        """
        @param name: str
            The new name for the back option
        """

        if self.__back_option is not None:
            self.__back_option.set_name(name)
        self.draw()

    def draw(self) -> None:
        """
        Redraws the menu
        """
        self.__clear_text()

        self.__write_text_title()
        self.__write_text_display()
        self.__write_text_options()

        self._text.pack(expand=True, fill="both")
        self._text.focus_set()

    def get_input(self, count: int, window_title: str, callback: Callable, *prompts) -> None:
        """
        @param count: int
            The number of inputs
        @param window_title: str
            The window title for the spawned input window
        @param callback: Callable
            The callback that gets called and passed the inputs that the user enters. 
            The callback needs to take in count positional arguements, one for each input. 
            The inputs are passed in the same order that the promtps are pass to this function.
        @param *prompts
            A list of prompts to display. One prompt for each desired input. The number of prompts should be the same as count

        Displays a new window with count input fields. Displays one prompt for each field. 
        When the user submits the inputs it calls the passed callbacks and passes the callback the input from the user
        """
        if count != len(prompts):
            raise Exception("Length of input prompts does not match the count")

        self.__input_text_callback = callback

        self.__input_text_window = tk.Toplevel(self)
        self.__input_text_window.title(window_title)

        for prompt in prompts:
            tk.Label(self.__input_text_window, text=prompt).pack()

            self.__input_texts.append(tk.Entry(self.__input_text_window))
            self.__input_texts[-1].pack(expand=True, fill="both")

        self.__input_texts[0].focus_set()

        self.__input_texts[-1].bind("<Return>",
                                   self.__get_input_from_input_window)

        submit_button = tk.Button(
            self.__input_text_window, text="Submit", command=self.__get_input_from_input_window)
        submit_button.pack()

    def switch_menu(self, new_menu: "Menu", on_return_callback: Callable | None = None) -> None:
        """
        @param new_menu: Menu
            The new menu to switch to
        @param on_return_callback: Callable | None = None
            Optional callback that gets called when returning to this menu from a submenu
        Switch from the current menu to the passed menu object
        """
        if on_return_callback is not None:
            self.__on_return_to_menu_callback = on_return_callback

        self.clear_display()
        self.__clear_menu()

        new_menu.__set_back_option(self.__switch_back, new_menu)
        new_menu.draw()

    def get_root(self) -> tk.Tk:
        """
        @returns tk.Tk
            Menu root window
        
        Returns the root window of the current menu
        """
        return self.__root

    def get_display(self) -> str:
        """
        @returns str
            value of the read only display

        Returns the current value of the read only display area
        """
        return self.__text_display

    def set_display(self, text: str) -> None:
        """
        @param text: set

        Overrides the previous value of the read only display area
        """
        self.__text_display = text
        self.draw()

    def print(self, text: str, end: str = "\n") -> None:
        """
        @param text: str
            The text to append to the read only display area
        @param end: str = "\\n" 
            The suffix to append to the end of the text parameter

        Appends the given text to the end of the read only display area
        """
        self.__text_display += text
        self.__text_display += end
        self.draw()

    def clear_display(self) -> str:
        """
        @returns str
            The old value of the read only display
        Clears the read only display. Returns the deleted value.
        """
        text = self.__text_display
        self.__text_display = ""
        self.draw()
        return text

    def clear_options(self) -> None:
        """
        Deletes all options
        """
        self.__options = []
        self.draw()

    def __set_back_option(self, callback: Callable, *args, **kwargs):
        self.__back_option = Menu.MenuOption("Back", callback, *args, **kwargs)

    def __write_text_display(self) -> None:
        self.__write_text(self.__text_display +
                         ("\n" if self.__text_display != "" else ""))

    def __write_text_options(self) -> None:
        self.__write_text(f"{self.__options_header}\n")
        for i in range(len(self.__options)):
            self.__write_text(
                f"{self.__options[i]} {'<------' if i == self.__selected else ''}\n")

        if self.__back_option is not None:
            self.__write_text(f"{self.__back_option} {'<------' if self.__selected == len(self.__options) else ''}")

    def __write_text_title(self) -> None:
        self.__write_text(f"------{self.__title}------\n", 1.0)

    def __clear_text(self) -> None:
        self._text.configure(state="normal")
        self._text.delete("1.0", "end")
        self._text.configure(state="disabled")

    def __write_text(self, text: str, index: str | float = "end") -> None:
        self._text.configure(state="normal")
        self._text.insert(index, text)
        self._text.configure(state="disabled")

    def __clear_menu(self) -> None:
        self._text.unbind("<Up>")
        self._text.unbind("<Down>")
        self._text.unbind("<Return>")

        self._text.pack_forget()
        self.pack_forget()

    def __text__init(self) -> None:
        self._text: tk.Text = tk.Text()
        self.__bindings()

    def __bindings(self) -> None:
        self._text.bind("<Up>", self.__select_up)
        self._text.bind("<Down>", self.__select_down)
        self._text.bind("<Return>", self.__call_option)

    def __call_option(self, event: tk.Event) -> None:
        if self.__selected == len(self.__options) and self.__back_option is not None:
            self.__back_option()
        else:
            self.__options[self.__selected]()

    def __select_up(self, event: tk.Event) -> None:
        self.__selected = (self.__selected - 1) % (len(self.__options) + (1 if self.__back_option is not None else 0))
        self.draw()

    def __select_down(self, event: tk.Event) -> None:
        self.__selected = (self.__selected + 1) % (len(self.__options) + (1 if self.__back_option is not None else 0))
        self.draw()

    def __get_input_from_input_window(self, event: tk.Event | None = None) -> None:
        texts = [self.__input_texts[i].get()
                 for i in range(len(self.__input_texts))]
        self.__input_text_window.destroy()

        self.__input_texts = []
        self.__input_text_window = None

        callback = self.__input_text_callback
        self.__input_text_callback = None

        callback(*texts)

    def __switch_back(self, other_menu: "Menu") -> None:
        other_menu.__clear_menu()
        other_menu.destroy()

        self.__bindings()
        self.draw()

        if self.__on_return_to_menu_callback is not None:
            self.__on_return_to_menu_callback()
