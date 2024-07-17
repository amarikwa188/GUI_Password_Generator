from tkinter import Tk, Checkbutton, DoubleVar, Spinbox, Button, BooleanVar, Toplevel
from tkinter.ttk import Label

from string import ascii_lowercase as l_case, ascii_uppercase as u_case
from string import digits
import random as rng
from itertools import cycle  

import subprocess


class PasswordGenertator:
    """
    Represents and instance of the password generator application.
    """
    def __init__(self) -> None:
        self.root: Tk = Tk()
        self.root.geometry("300x200+500+200")
        self.root.resizable(0,0)
        self.root.title("Random Password Generator")

        self.FONT: str = "Helvetica"

        self.length_label: Label = Label(self.root, text="Length:",
                                         font=(self.FONT, 11))
        self.length_label.place(relx=0.1, rely=0.1, anchor="w")

        default: DoubleVar = DoubleVar(value=10)
        self.length_spinbox: Spinbox = Spinbox(self.root, from_=4, to=20,
                                               state="readonly", width=13,
                                               textvariable=default,
                                               relief="sunken")
        self.length_spinbox.place(relx=0.6, rely=0.1, anchor="center")
        

        self.uppercase_label: Label = Label(self.root, font=(self.FONT, 11),
                                            text="Contain uppercase?")
        self.uppercase_label.place(relx=0.1, rely=0.25, anchor="w")

        self.upper: BooleanVar =  BooleanVar(value=0)
        self.uppercase_check: Checkbutton = Checkbutton(self.root,
                                                        variable=self.upper)
        self.uppercase_check.place(relx=0.7, rely=0.25, anchor="center")


        self.lowercase_label: Label = Label(self.root, font=(self.FONT, 11),
                                            text="Contain lowercase?")
        self.lowercase_label.place(relx=0.1, rely=0.4, anchor="w")

        self.lower: BooleanVar =  BooleanVar(value=0)
        self.lowercase_check: Checkbutton = Checkbutton(self.root,
                                                        variable=self.lower)
        self.lowercase_check.place(relx=0.7, rely=0.4, anchor="center")


        self.digits_label: Label = Label(self.root, font=(self.FONT, 11),
                                            text="Contain digits?")
        self.digits_label.place(relx=0.1, rely=0.55, anchor="w")

        self.digits: BooleanVar =  BooleanVar(value=0)
        self.digits_check: Checkbutton = Checkbutton(self.root, 
                                                     variable=self.digits)
        self.digits_check.place(relx=0.7, rely=0.55, anchor="center")


        self.symbols_label: Label = Label(self.root, font=(self.FONT, 11),
                                            text="Contain symbols?")
        self.symbols_label.place(relx=0.1, rely=0.7, anchor="w")

        self.symbols: BooleanVar =  BooleanVar(value=0)
        self.symbols_check: Checkbutton = Checkbutton(self.root, 
                                                      variable=self.symbols)
        self.symbols_check.place(relx=0.7, rely=0.7, anchor="center")
        
        self.generate_button: Button = Button(self.root, text="Generate",
                                              command=self.display_password)
        self.generate_button.place(relx=0.5, rely=0.9, anchor="center")

        self.root.mainloop()


    def randomize(self, string: str) -> str:
        """
        Give a random permutation of a string.

        :param string: the given string.
        :return: a random permutation of the string.
        """
        chars: list[str] = list(string)
        rng.shuffle(chars)
        return ''.join(chars)


    def generate_password(self, length: int, upper: bool, lower: bool,
                          nums: bool, sym: bool) -> str:
        """
        Generate a random password with a given length and character range.

        :param length: the length of the password.
        :param upper: whether the password should contain uppercase letters.
        :param lower: whether the password should contain lowercase letters.
        :param nums: whether the password should contain digits.
        :param sym: whether the password should contain symbols.
        :return: the random password.
        """
        
        char_pool: list[str] = list()

        symbols: str = '!@$%\#?/'
        
        if upper: char_pool.append(u_case)
        if lower: char_pool.append(l_case)
        if nums: char_pool.append(digits)
        if sym: char_pool.append(symbols)

        draw: cycle = cycle(char_pool)

        password: str = ""

        for _ in range(length):
            current: str = next(draw)
            random_char: str = current[rng.randint(0, len(current)-1)]
            password += random_char

        password = self.randomize(password)

        return password


    def display_password(self) -> None:
        """
        Generate a random password and launch a pop-up window to display it.
        """
        length: int = int(self.length_spinbox.get())
        upper: bool = self.upper.get()
        lower: bool = self.lower.get()
        nums: bool = self.digits.get()
        sym: bool = self.symbols.get()

        valid_char_set: bool = any([upper, lower, nums, sym])

        if valid_char_set:
            password: str = self.generate_password(length, upper, lower, nums, sym)
            self.pop_up(password)


    def pop_up(self, password: str) -> None:
        """
        Create a pop-up window that displays a generated password.

        :param password: the given password.
        """
        display: Toplevel = Toplevel()
        display.geometry("260x90+520+250")
        display.resizable(0,0)
        display.title("Password")
        display.grab_set()

        def new_password() -> None:
            # Generate a new password
            info: list[int | bool] = [int(self.length_spinbox.get()),
                                      self.upper.get(),
                                      self.lower.get(),
                                      self.digits.get(),
                                      self.symbols.get()]
            new: str = self.generate_password(*info)
            password_text.config(text=new)
            

        def copy_password():
            # Copy te generated password to the clipboard
            current_password: str = password_text.cget("text")
            cmd: str = f'echo {current_password}|clip'
            return subprocess.check_call(cmd, shell=True)


        password_text: Label = Label(display, text=password, font=6,
                                     state="readonly", relief="sunken",
                                     padding=3)
        password_text.place(relx=0.5, rely=0.3, anchor="center")

        generate_button: Button = Button(display, text="Generate", width=7,
                                         command=new_password)
        generate_button.place(relx=0.35, rely=0.7, anchor="center")

        copy_button: Button = Button(display, text="Copy", width=7,
                                     command=copy_password)
        copy_button.place(relx=0.65, rely=0.7, anchor="center")
    
        self.root.wait_window(display)


if __name__ == "__main__":
    PasswordGenertator()