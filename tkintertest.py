from tkinter import *
import mysql.connector as mysql
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedTk
import tkinter.font as font

root = ThemedTk()
root.title("Raz's Supermarket, Dubai Br.")
root.geometry("300x350")
Heading = font.Font(family = "Arial", size = 15 , weight = "bold")
style = ttk.Style(root)
style.theme_use("breeze")  # 'winnative', 'clam', 'alt', 'default' and more...


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
            sign_frame.pack()
            return con, cursor
    except Exception as e:
        messagebox.showerror("Error", "Wrong Password for MySQL.")


def sign_in():
    sign_frame.destroy()
    sign_in_frame.pack()
    uname_label = ttk.Label(sign_in_frame, text="Username")
    password_label = ttk.Label(sign_in_frame, text="Password")
    uname_label.pack()
    uname_entry = ttk.Entry(sign_in_frame, text="Username")
    uname_entry.pack()
    password_label.pack()
    password_entry = ttk.Entry(sign_in_frame, text="Password", show="*")
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
                sign_in_label = ttk.Label(
                    menu_frame, text=f"Signed in as {currentUser} - {currentRole}"
                )
                sign_in_label.pack()
                menu_frame.pack()
                sign_in_frame.destroy()
        except Exception as e:
            print(e)
            print("Error!")
            quit()

    sign_in_submit = ttk.Button(sign_in_frame, text="Submit", command=submit)
    sign_in_submit.pack()


def sign_up():
    sign_frame.destroy()
    sign_up_frame.pack()
    uname_label = ttk.Label(sign_up_frame, text="New Username")
    password_label = ttk.Label(sign_up_frame, text="Password")
    uname_label.pack()
    uname_entry = ttk.Entry(sign_up_frame)
    uname_entry.pack()
    password_label.pack()
    password_entry = ttk.Entry(sign_up_frame, show="*")
    password_entry.pack()
    # roles menu
    roles_list = ["","Sales Manager", "Cashier"]
    role_inside = StringVar(sign_up_frame)
    role_inside.set("Select Role")
    role_menu = ttk.OptionMenu(sign_up_frame, role_inside, *roles_list)
    role_menu.pack()

    def submit():
        global currentRole, currentUser
        uname = uname_entry.get()
        password = password_entry.get()
        urole = role_inside.get()
        try:
            if uname != "" and password != "" and urole != "Select Role" and urole != "":
                cursor.execute(
                    f"INSERT INTO user_details (uname,password,urole) VALUES ('{uname}','{password}','{urole}');"
                )
                con.commit()
                currentUser, currentRole = uname, urole
                sign_up_label = ttk.Label(
                    menu_frame, text=f"Signed in as {currentUser} - {currentRole}"
                )
                sign_up_label.pack()
                menu_frame.pack()
                sign_up_frame.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Username not available \n {e}")

    sign_up_submit = ttk.Button(sign_up_frame, text="Submit", command=submit)
    sign_up_submit.pack()


def view():
    cursor.execute("SELECT * FROM product;")
    allproducts = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    if len(allproducts) == 0:
        messagebox.showerror("Error", "No products available")
    else:
        data_view = Tk()
        data_view.title("View Products")

        tree = ttk.Treeview(data_view, columns=column_names, show="headings")

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


def add():
    add_win = Tk()
    add_win.title("Add New Product")
    pname_label = ttk.Label(add_win, text="Product Name: ")
    price_label = ttk.Label(add_win, text="Price: ")
    stock_label = ttk.Label(add_win, text="Stock:")
    pname_label.pack()
    pname_entry = ttk.Entry(add_win)
    pname_entry.pack()
    price_label.pack()
    price_entry = ttk.Entry(add_win)
    price_entry.pack()
    stock_label.pack()
    stock_entry = ttk.Entry(add_win)
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

    add_product_btn = ttk.Button(add_win, text="Add Product", command=submit)
    add_product_btn.pack()


currentUser = ""
currentRole = ""

s = ttk.Style()
s.configure('my.TButton', font=('Helvetica', 15))



auth_frame = ttk.Frame(root)
auth_frame.pack()
auth_label = ttk.Label(auth_frame, text="Enter MySQL Password: ")
auth_label.pack()
auth_entry = ttk.Entry(auth_frame, show="*")
auth_entry.pack()
auth_button = ttk.Button(auth_frame, text="Authenticate", style = "my.TButton",command=auth  )
auth_button.pack()

sign_frame = ttk.Frame(root)
sign_in_btn = ttk.Button(sign_frame, text="Sign in", command=sign_in)
sign_in_btn.pack()
sign_up_btn = ttk.Button(sign_frame, text="Sign up", command=sign_up)
sign_up_btn.pack()

# sign IN
sign_in_frame = ttk.Frame(root)
sign_in_h1 = ttk.Label(sign_in_frame, text="Sign in", font=Heading ,padding = 10)
sign_in_h1.pack()

# sign UP
sign_up_frame = ttk.Frame(root)
sign_up_h1 = ttk.Label(sign_up_frame, text="Sign up",font=Heading, padding=10)
sign_up_h1.pack()

menu_frame = ttk.Frame(root)
view_btn = ttk.Button(menu_frame, text="View Available Products", command=view)
view_btn.pack()
add_btn = ttk.Button(menu_frame, text="Add Product", command=add)
add_btn.pack()

root.mainloop()
