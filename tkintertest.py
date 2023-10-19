from tkinter import *
import mysql.connector as mysql
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedTk
import tkinter.font as font

root = ThemedTk()
root.title("Raz's Supermarket, Dubai Br.")
root.geometry("300x350")

Heading = font.Font(family="Arial Black", size=23, weight="bold")
Standard = font.Font(family="Arial", size=12)
hidden_Entry_font = font.Font(size=12)
style = ttk.Style(root)
style.theme_use("adapta")  # 'winnative', 'clam', 'alt', 'default' and more...
s = ttk.Style()
s.configure("my.TButton", takefocus=False, font=("Arial", 14, "bold"), padding=(5, 2))
s.configure("big.TButton", font=("Arial Black", 16, "bold"))


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
            sign_frame.pack(expand=True, fill="both")
            sign_frame.place(in_=root, anchor="c", relx=0.5, rely=0.5)
            return con, cursor
    except Exception as e:
        messagebox.showerror("Error", "Wrong Password for MySQL.")


def sign_in():
    sign_frame.destroy()
    sign_in_frame.pack(expand=True, fill="both")
    sign_in_frame.place(in_=root, anchor="center", relx=0.5, rely=0.5)
    uname_label = ttk.Label(
        sign_in_frame, text="Username", font=Standard, padding=(10, 2)
    )
    password_label = ttk.Label(
        sign_in_frame, text="Password", font=Standard, padding=(10, 2)
    )
    uname_label.pack(pady =3 )
    uname_entry = ttk.Entry(sign_in_frame)
    uname_entry.pack()
    password_label.pack()
    password_entry = ttk.Entry(sign_in_frame, show="•", font=("Arial", 11))
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
                    menu_frame,
                    text=f"Signed in as {currentUser} - {currentRole}",
                    font=Standard,
                )
                sign_in_label.pack()
                menu_frame.pack(expand=True, fill="both")
                menu_frame.place(in_=root, anchor="c", relx=0.5, rely=0.5)
                sign_in_frame.destroy()
        except Exception as e:
            print(e)
            print("Error!")
            quit()

    sign_in_submit = ttk.Button(
        sign_in_frame, text="Submit", command=submit, style="my.TButton"
    )
    sign_in_submit.pack(pady=10)


def sign_up():
    sign_frame.destroy()
    sign_up_frame.pack(expand=True, fill="both")
    sign_up_frame.place(in_=root, anchor="c", relx=0.5, rely=0.5)
    uname_label = ttk.Label(sign_up_frame, text="New Username", font=Standard)
    password_label = ttk.Label(sign_up_frame, text="Password", font=Standard)
    uname_label.pack()
    uname_entry = ttk.Entry(sign_up_frame)
    uname_entry.pack()
    password_label.pack()
    password_entry = ttk.Entry(sign_up_frame, show="•", font=hidden_Entry_font)
    password_entry.pack()
    # roles menu
    roles_list = ["", "Sales Manager", "Cashier"]
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
                sign_in_label = ttk.Label(
                    menu_frame,
                    text=f"Signed in as {currentUser} - {currentRole}",
                    font=Standard,
                )
                sign_in_label.pack()

                sign_up_frame.destroy()
                menu_frame.pack(expand=True, fill="both")
                menu_frame.place(in_=root, anchor="c", relx=0.5, rely=0.5)
        except Exception as e:
            messagebox.showerror("Error", f"Username not available \n {e}")

    sign_up_submit = ttk.Button(
        sign_up_frame, text="Submit", command=submit, style="my.TButton"
    )
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
    add_win = ThemedTk()
    style = ttk.Style(add_win)
    style.theme_use("breeze")
    add_frame = ttk.Frame(add_win)
    add_frame.pack(expand=True, fill="both")
    add_frame.place(in_=add_win, anchor="c", relx=0.5, rely=0.5)
    add_win.title("Add New Product")
    pname_label = ttk.Label(add_frame, text="Product Name: ", font=Standard)
    price_label = ttk.Label(add_frame, text="Price: ", font=Standard)
    stock_label = ttk.Label(add_frame, text="Stock:", font=Standard)
    pname_label.pack()
    pname_entry = ttk.Entry(add_frame)
    pname_entry.pack()
    price_label.pack()
    price_entry = ttk.Entry(add_frame)
    price_entry.pack()
    stock_label.pack()
    stock_entry = ttk.Entry(add_frame)
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

    bstyle = ttk.Style(add_win)
    bstyle.configure(".TButton", font=("Calibri", 14, "bold"))
    add_product_btn = ttk.Button(
        add_frame, text="Add Product", command=submit, style=".TButton"
    )
    add_product_btn.pack()


currentUser = ""
currentRole = ""


auth_frame = ttk.Frame(root)
auth_frame.pack(expand=True, fill="both")
auth_frame.place(in_=root, anchor="c", relx=0.5, rely=0.5)
auth_label = ttk.Label(
    auth_frame,
    text="MySQL Password ",
    font=("Arial Black", 16, "bold"),
    padding=(10, 5),
)
auth_label.pack()
auth_entry = ttk.Entry(auth_frame, show="•", font=hidden_Entry_font)
auth_entry.pack()
auth_button = ttk.Button(
    auth_frame, text="Authenticate", style="my.TButton", command=auth
)
auth_button.pack(pady=10)

sign_frame = ttk.Frame(root, padding=(10, 10))
sign_in_btn = ttk.Button(
    sign_frame, text="Sign in", command=sign_in, style="big.TButton", padding=(10, 10)
)
sign_in_btn.pack()
sign_up_btn = ttk.Button(
    sign_frame, text="Sign up", command=sign_up, style="big.TButton", padding=(10, 10)
)
sign_up_btn.pack()

# sign IN
sign_in_frame = ttk.Frame(root)
sign_in_h1 = ttk.Label(sign_in_frame, text="Sign in", font=Heading, padding=(10, 10))
sign_in_h1.pack()

# sign UP
sign_up_frame = ttk.Frame(root)
sign_up_h1 = ttk.Label(sign_up_frame, text="Sign up", font=Heading, padding=10)
sign_up_h1.pack()

menu_frame = ttk.Frame(root)
view_btn = ttk.Button(
    menu_frame, text="View Products", command=view, style="big.TButton"
)
view_btn.pack(pady=5)
add_btn = ttk.Button(menu_frame, text="Add Product", command=add, style="big.TButton")
add_btn.pack(pady=5)

root.mainloop()
