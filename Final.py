from customtkinter import *
import mysql.connector as mysql
from tkinter import messagebox
import pandas as pd
from tkinter import ttk

root = CTk()
root.geometry("350x300")
root.title("Graphical Retail Operation Hub")
set_default_color_theme("blue")
set_appearance_mode("light")
Heading = CTkFont(family="Arial Black", size=30, weight="bold")
Bfont = CTkFont(family="Arial",size = 28,weight="bold")
Standard = CTkFont(family="Arial", size=15, weight="bold")


def auth():
    global con, cursor
    try:
        password = auth_entry.get()
        con = mysql.connect(host="localhost", user="root", password=password)
        cursor = con.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS my_database;")
        cursor.execute("USE my_database;")

        # all tables creation-->
        # user details
        cursor.execute(
            "create table if not exists user_details( uname varchar(25) primary key, password varchar(25), urole varchar(15));"
        )
        # product
        cursor.execute(
            "create table if not exists product(pID int(20) primary key, pname varchar(25), price float(10,2), stock int(15));"
        )
        # sales
        cursor.execute(
            "create table if not exists sales(sID int(20) primary key, pID int, quantity_sold int(25), total_price float(10,2), sale_date date, cashier varchar(25), foreign key (pID) references product(pID), foreign key (cashier) references user_details(uname));"
        )
        if con.is_connected():
            auth_frame.destroy()
            sign_frame.pack(expand=True, fill="both", padx=20, pady=20)
            sign_frame.place(in_=root, anchor="c", relx=0.5, rely=0.5)
            return con, cursor
    except Exception as e:
        messagebox.showerror("Error", "Wrong Password for MySQL.")


def sign_in():
    sign_frame.destroy()
    sign_in_frame.pack(expand=True, fill="both", padx=20, pady=20)
    sign_in_frame.place(in_=root, anchor="center", relx=0.5, rely=0.5)
    uname_label = CTkLabel(master=sign_in_frame, text="Username", font=Standard)
    password_label = CTkLabel(master=sign_in_frame, text="Password", font=Standard)
    uname_label.pack(pady=3)
    uname_entry = CTkEntry(master=sign_in_frame, font=Standard)
    uname_entry.pack()
    password_label.pack()
    password_entry = CTkEntry(master=sign_in_frame, show="•", font=Standard)
    password_entry.pack()

    def submit():
        uname = uname_entry.get()
        password = password_entry.get()
        try:
            cursor.execute(f"select * from user_details where uname='{uname}'")
            row = cursor.fetchone()
            if row is not None and password == row[1]:
                global currentUser, currentRole
                currentUser, currentRole = uname, row[2]
                sign_in_label = CTkLabel(
                    master=menu_frame,
                    text=f"Signed in as {currentUser} - {currentRole}",
                    font=Standard,
                )
                sign_in_label.pack()
                menu_frame.pack(expand=True, fill="both", padx=20, pady=20)
                menu_frame.place(in_=root, anchor="c", relx=0.5, rely=0.5)
                sign_in_frame.destroy()
        except Exception as e:
            print(e)
            print("Error!")
            quit()

    sign_in_submit = CTkButton(
        master=sign_in_frame, text="Submit", command=submit, font=Standard
    )
    sign_in_submit.pack(pady=10)


def sign_up():
    sign_frame.destroy()
    sign_up_frame.pack(expand=True, fill="both", padx=20, pady=20)
    sign_up_frame.place(in_=root, anchor="c", relx=0.5, rely=0.5)
    uname_label = CTkLabel(master=sign_up_frame, text="New Username", font=Standard)
    password_label = CTkLabel(master=sign_up_frame, text="Password", font=Standard)
    uname_label.pack()
    uname_entry = CTkEntry(master=sign_up_frame, font=Standard)
    uname_entry.pack(pady =5)
    password_label.pack()
    password_entry = CTkEntry(master=sign_up_frame, show="•", font=Standard)
    password_entry.pack(pady =10)
    # roles menu
    roles_list = ["Sales Manager", "Cashier"]
    role_inside = StringVar(value="Select Role")
    role_menu = CTkOptionMenu(sign_up_frame, values=roles_list, variable=role_inside)
    role_menu.pack(pady =10)

    def submit():
        global currentRole, currentUser
        uname = uname_entry.get()
        password = password_entry.get()
        urole = role_inside.get()
        try:
            if (
                uname != ""
                and password != ""
                and urole != "Select Role"
                and urole != ""
            ):
                cursor.execute(
                    f"INSERT INTO user_details (uname,password,urole) VALUES ('{uname}','{password}','{urole}');"
                )
                con.commit()
                currentUser, currentRole = uname, urole
                sign_in_label = CTkLabel(
                    master=menu_frame,
                    text=f"Signed in as {currentUser} - {currentRole}",
                    font=Standard,
                )
                sign_in_label.pack()

                sign_up_frame.destroy()
                menu_frame.pack(expand=True, fill="both", padx=20, pady=20)
                menu_frame.place(in_=root, anchor="c", relx=0.5, rely=0.5)
        except Exception as e:
            messagebox.showerror("Error", f"Username not available \n {e}")

    sign_up_submit = CTkButton(sign_up_frame, text="Submit", command=submit)
    sign_up_submit.pack(pady = 20)


def add():
    add_win = CTk()
    add_win.title("Add New Product")
    add_win.geometry("200x300")
    add_frame = CTkFrame(master = add_win,fg_color="transparent")
    add_frame.pack(expand=True, fill="both")
    add_frame.place(in_=add_win, anchor="c", relx=0.5, rely=0.5)
    pname_label = CTkLabel(master=add_frame, text="Product Name ", font=Standard)
    price_label = CTkLabel(master=add_frame, text="Price ", font=Standard)
    stock_label = CTkLabel(master=add_frame, text="Stock", font=Standard)
    pname_label.pack()
    pname_entry = CTkEntry(master=add_frame, font=Standard)
    pname_entry.pack()
    price_label.pack()
    price_entry = CTkEntry(master=add_frame, font=Standard)
    price_entry.pack()
    stock_label.pack()
    stock_entry = CTkEntry(master=add_frame, font=Standard)
    stock_entry.pack()

    def submit():
        cursor.execute("select pID from product order by pID desc limit 1;")
        pID = int(cursor.fetchall()[0][0]) + 1
        pname = pname_entry.get()
        price = price_entry.get()
        stock = stock_entry.get()
        if pname != "" and price != "" and stock != "":
            cursor.execute(
                f'insert into product values("{pID}","{pname}","{price}","{stock}"); '
            )
            con.commit()
            messagebox.showinfo("Successful", f"Product {pname} added successfully!")
            add_win.destroy()
        else:
            messagebox.showerror("Failed to Add", "Please enter valid details.")

    add_product_btn = CTkButton(
        master=add_frame, text="Add Product", command=submit, font=Standard
    )
    add_product_btn.pack(pady=20)
    add_win.mainloop()


def view():
    query = "SELECT * FROM product;"
    cursor.execute(query)
    allproducts = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    if len(allproducts) == 0:
        messagebox.showerror("Error", "No products available")
    else:
        data_view = CTk()
        data_view.title("View Products")

        tree = ttk.Treeview(master=data_view, columns=column_names, show="headings")

        for col in column_names:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        for product in allproducts:
            tree.insert("", "end", values=product)

        scrollbar = ttk.Scrollbar(data_view, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(fill="both", expand=True)
        if len(allproducts) > 20:
            scrollbar.pack(side="right", fill="y")

        data_view.mainloop()

def combobox_callback(choice):
    set_appearance_mode(choice)
    theme_var.set(f"{choice.capitalize()} theme")
theme_var = StringVar(value = "Theme")
theme = CTkComboBox(master = root, values=["light", "dark"],command=combobox_callback, variable=theme_var,justify="center")
theme_var.set("Theme")
theme.pack()

auth_frame = CTkFrame(master=root, height = 300, width = 350,fg_color="transparent")
auth_frame.pack(expand=True, fill="y", padx=20, pady=50)
auth_frame.place(in_=root, anchor="center")
auth_label = CTkLabel(
    master=auth_frame, text="MySQL Password", font=Standard, padx=10, pady=10
)
auth_label.pack()
auth_entry = CTkEntry(master=auth_frame, show="• ", font=("Arial", 20))
auth_entry.pack()
auth_button = CTkButton(
    master=auth_frame, text="Authenticate", command=auth, font=Standard,corner_radius=180
)
auth_button.pack(pady=20, padx = 5)
auth_frame.pack()

sign_frame = CTkFrame(master=root,width=300,height=300,fg_color="transparent")
sign_in_btn = CTkButton(
    master=sign_frame, text="Sign in", command=sign_in, font=Bfont
)
sign_in_btn.pack(pady=10,padx=30)
sign_up_btn = CTkButton(
    master=sign_frame, text="Sign up", command=sign_up, font=Bfont
)
sign_up_btn.pack(pady=10,padx=30)

# sign IN
sign_in_frame = CTkFrame(master=root,fg_color="transparent")
sign_in_h1 = CTkLabel(master=sign_in_frame, text="Sign in", font=Heading)
sign_in_h1.pack()

# sign UP
sign_up_frame = CTkFrame(master=root,fg_color="transparent")
sign_up_h1 = CTkLabel(master=sign_up_frame, text="Sign up", font=Heading)
sign_up_h1.pack()

menu_frame = CTkFrame(master=root,fg_color="transparent")
view_btn = CTkButton(
    master=menu_frame, text="View Products", command=view, font=Bfont
)
view_btn.pack(pady=10)
add_btn = CTkButton(master=menu_frame, text="Add Product", command=add, font=Bfont)
add_btn.pack(pady=10)


root.mainloop()