from client.pages.page import Page, PageType
from tkinter import messagebox


class ForgotPage(Page):
    PAGE_ID = PageType.assign_id("forgot")
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.set_title("Forgot Password")

        self.forgot_email = self.create_field("Email:")
        self.forgot_email.pack()
        

        self.create_action_button("Send Reset Link", self.forgot_action, pack_pady=5)
        
        self.add_link(page_type=PageType.identify("login"), text="Back to Login")

    def forgot_action(self):
        email = self.forgot_email.get()
        messagebox.showinfo("Forgot Password", f"Password reset link sent to {email}!")

