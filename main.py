from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# --------------------------- SEARCH FUNCTION ----------------------------------- #
def find_password():
    website = website_input.get().title()
    try:
        with open('password_manager.json', 'r') as datafile:
            data = json.load(datafile)
    except FileNotFoundError:
        messagebox.showerror(title='Error', message="No Data File Found", icon='error')
    else:
        if website in data:
            password = data[website]['password']
            email = data[website]['username']
            messagebox.showinfo(title=f'{website} Details', message=f'Email: {email}\n\npassword: {password}')
        else:
            messagebox.showinfo(title='Error', message=f'No details for this website')


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# Password Generator Project

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for _ in range(nr_letters)]
    password_list += [random.choice(symbols) for _ in range(nr_symbols)]
    password_list += [random.choice(numbers) for _ in range(nr_numbers)]

    random.shuffle(password_list)

    password = "".join(password_list)

    password_input.delete(0, END)

    password_input.insert(END, string=f'{password}')

    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    with open('password_manager.json', 'a+') as data_file:
        website = website_input.get().title()
        username = username_input.get()
        password = password_input.get().title()
        new_data = {
            website: {
                'username': username,
                'password': password,
            },
        }

        if len(website) == 0 or len(password) == 0:
            messagebox.showerror(title='Error', message=f'You can not have any empty fields', icon='error',
                                 default='ok')
        elif website in data_file:
            messagebox.askokcancel(title=f"Warning",
                                   message=f'{website} already exists\n \nEmail: {username}\nPassword: {password} \n'
                                           f'\nClick OK to Change update the details?')
            print(data_file)

        else:
            is_ok = messagebox.askokcancel(title=website,
                                           message=f'Website Details\n \nEmail: {username}\nPassword: {password} \n'
                                                   f'\nClick OK to Save?')

            if is_ok:
                # Dumps helps to write new data to a Json file
                # json.dump(new_data, data_file, indent=4)
                # Load helps read from a Json file and converts to py dictionary
                try:
                    with open('password_manager.json', 'r') as data_file:
                        data = json.load(data_file)
                except FileNotFoundError:
                    with open('password_manager.json', 'w') as data_file:
                        json.dump(new_data, data_file, indent=4)
                else:
                    # with open('password_manager.json', 'r') as data_file:

                    data.update(new_data)
                    with open('password_manager.json', 'w') as data_file:
                        json.dump(data, data_file, indent=4)

                website_input.delete(0, END)
                password_input.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_image = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo_image)
canvas.grid(row=0, column=1)

# -------------------------labels --------------------------------------- #
website_label = Label()
website_label.config(text='website:')
website_label.grid(row=1, column=0)

username_label = Label()
username_label.config(text='Email/Username:')
username_label.grid(row=2, column=0)

password_label = Label()
password_label.config(text='password:')
password_label.grid(row=3, column=0)

# ----------------------- Entries ------------------------------------------- #
website_input = Entry(width=36)
website_input.focus()

website_input.grid(row=1, column=1)
username_input = Entry(width=54)
username_input.insert(END, string='obumanichebe@gmail.com')
username_input.grid(row=2, column=1, columnspan=2)

password_input = Entry(width=36)
password_input.grid(row=3, column=1)

# ----------------------- Buttons ------------------------------------------- #
search_button = Button(text='Search', width=14, command=find_password)
search_button.grid(row=1, column=2)

generate_password_button = Button(text='Generate password', command=generate_password)
generate_password_button.grid(row=3, column=2)

add_button = Button(text='Add', width=46, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
