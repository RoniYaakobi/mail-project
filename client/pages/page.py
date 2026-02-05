from enum import Enum

import tkinter as tk
from tkinter import messagebox

class PageType(Enum):
    BLANK = 0
    LOGIN = 1
    SIGNUP = 2
    FORGOT = 3


class Page(tk.Frame):
    PAGE_TYPE = PageType.BLANK

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.links = dict()

        self.controller = controller  # PageManager / App

    def show(self):
        print(self.links)
        self.tkraise()

    def set_title(self, text="Title", font=("Arial", 20)):
        tk.Label(self, text=text, font=font).pack(pady=10)

    def create_field(self, text="field", hidden= False):
        tk.Label(self, text=text).pack()
        field = tk.Entry(self, show="*") if hidden else tk.Entry(self)
        return field
    
    def create_action_button(self, text="Action",
        command= lambda: messagebox.showerror("Action button","No action"), pack_pady=0):
        
        tk.Button(self, text= text, command= command).pack(pady=pack_pady)

    def add_link(self, page_type: type , text="Go to a page", pack_pady=0):
        self.links[page_type] = self
        self.create_action_button(text=text,
                                   command= lambda: self.links[page_type].show(), pack_pady=pack_pady)

    def set_link(self, page_type: type, page):
        self.links[page_type] = page
    
    def get_links(self):
        return self.links

    


   