import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from customtkinter import CTkButton, CTk
#from tkinter import ttk, messagebox
from db import get_create_user
from PIL import Image, ImageTk



#function to log user name and assign a unique ID foe each
def open_log(callback):
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("dark-blue")

    def login():
        name = entry_name.get()
        password = entry_pass.get()

        if not name.strip() or not password.strip():
            CTkMessagebox(title="Warning", message="Please enter your TCS ID or password to continue", icon="warning", option_1="Retry")
            return

        user_id = get_create_user(name, password, mod="login")
        if user_id is None:
            CTkMessagebox(title="Error", message="Incorrect password or user doesn't exist", icon="cancel", option_1="Retry")
            return

        logwindow.destroy()
        callback(user_id, name.title())

    def confirm_register():
        name = entry_name.get()
        password = entry_pass.get()
        fullname = entry_fullname.get()

        if not name.strip() or not password.strip() or not fullname.strip() or fullname.isdigit():
            CTkMessagebox(title="Warning", message="Please fill in all fields or enter valid values", icon="warning", option_1="Retry")
            return

        user_id = get_create_user(name, password, mod="register", user_name=fullname)
        if user_id is None:
            CTkMessagebox(title="Error", message="User already exists", icon="cancel", option_1="Retry")
            return

        CTkMessagebox(title="Success", message="User successfully registered", icon="check", option_1="Ok")
        logwindow.destroy()
        callback(user_id, name.title())

    def show_register():
        # to show full name field
        fullname_label.pack(pady=10)
        entry_fullname.pack()

        confirm_reg_button.pack(pady=20)
        cancel_reg_button.pack(pady=8)

        logbutton.pack_forget()
        registbutton.pack_forget()
        exitbutton.pack_forget()

    def cancel_register():
        #if you want to cancel register command
        fullname_label.pack_forget()
        entry_fullname.pack_forget()
        confirm_reg_button.pack_forget()
        cancel_reg_button.pack_forget()
        logbutton.pack(pady=20)
        registbutton.pack(pady=10)
        exitbutton.pack(pady=20)

    logwindow = ctk.CTk()
    logwindow.title("StepByStep")
    logwindow.geometry("750x600")

    welcome = ctk.CTkLabel(logwindow, text="Welcome to\n StepByStep", font=("Arial", 22, "bold"))
    welcome.pack(pady=10)
    
    tcslogo = Image.open(r"C:\Users\2928703\Documents\Proposal\tcs_logo.png")
    img = ctk.CTkImage(light_image=tcslogo, dark_image=tcslogo, size=(300, 150))
    label_img = ctk.CTkLabel(logwindow, image=img, text="")
    label_img.pack(pady=15)

    loglabel = ctk.CTkLabel(logwindow, text="Enter your TCS ID:")
    loglabel.pack(pady=10)

    global entry_name
    entry_name = ctk.CTkEntry(logwindow)
    entry_name.pack()

    passlabel = ctk.CTkLabel(logwindow, text="Password:")
    passlabel.pack(pady=10)

    global entry_pass
    entry_pass = ctk.CTkEntry(logwindow, show="*")
    entry_pass.pack()

    fullname_label = ctk.CTkLabel(logwindow, text="Full Name:")
    entry_fullname = ctk.CTkEntry(logwindow)

 # main buttons to show
    logbutton = ctk.CTkButton(logwindow, text="Login", corner_radius=20, command=login)
    logbutton.pack(pady=20)

    registbutton = ctk.CTkButton(logwindow, text="Register", corner_radius=20, command=show_register)
    registbutton.pack(pady=10)

    exitbutton = ctk.CTkButton(logwindow, text="Exit", corner_radius=20, fg_color="#880000", hover_color="#aa0000", command=logwindow.destroy)
    exitbutton.pack(pady=20)

    # If register button is clicked (hidden until click)
    confirm_reg_button = ctk.CTkButton(logwindow, text="Confirm Register", corner_radius=20, command=confirm_register)
    cancel_reg_button = ctk.CTkButton(logwindow, text="Cancel", corner_radius=20, fg_color="#880000", hover_color="#aa0000", command=cancel_register)

    logwindow.mainloop()

