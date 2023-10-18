from tkinter import *
import mysql.connector as mysql
from tkinter import messagebox


root = Tk()
root.title("Raz's Supermarket, Dubai Br.")
root.geometry("600x650")


def auth():
    global con,cursor
    try:
        password = auth_entry.get()
        con = mysql.connect(host="localhost", user="root", password=password)
        cursor = con.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS my_database;")
        cursor.execute('USE my_database;')

        # all tables creation-->
        # user details
        cursor.execute('create table if not exists user_details( uname varchar(25) primary key, password varchar(25) , urole varchar(15));')
        # product
        cursor.execute('create table if not exists product(pID int(20) primary key, pname varchar(25), price float(10,2) , stock int(15));')
        # sales
        cursor.execute('create table if not exists sales(sID int(20) primary key, pID int, quantity_sold int(25) , total_price float(10,2), sale_date date, cashier varchar(25), foreign key (pID) references product(pID), foreign key (cashier) references user_details(uname));')        
        if con.is_connected():
            # After successful authentication, update the label text
            authentication_label.config(text="Authentication Status: Authenticated")
            auth_frame.destroy()
            sign_frame.pack()
            return con,cursor
    except Exception as e:
        print(e)
        quit()


def sign_in():
    sign_frame.destroy()
    sign_in_frame.pack()
    uname_entry = Entry(sign_in_frame, text="Username")
    uname_entry.pack()
    password_entry = Entry(sign_in_frame, text="Password", show="*")
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
                sign_in_label = Label(menu_frame, text=f"Signed in as {currentUser} - {currentRole}")
                sign_in_label.pack()
                menu_frame.pack()
                sign_in_frame.destroy()
        except Exception as e:
            print(e)
            print('Error!')
            quit()

    sign_in_submit = Button(sign_in_frame, text="Submit", command=submit)
    sign_in_submit.pack()

def sign_up():
    sign_frame.destroy()
    sign_up_frame.pack()
    uname_entry = Entry(sign_up_frame, text="Username")
    uname_entry.pack()
    password_entry = Entry(sign_up_frame, text="Password", show="*")
    password_entry.pack()
    #roles menu
    roles_list = ['Sales Manager', 'Cashier']
    role_inside = StringVar(sign_up_frame)
    role_inside.set("Select Role")
    role_menu =  OptionMenu(sign_up_frame,role_inside,*roles_list)
    role_menu.pack()
    
    def submit():
        global currentRole, currentUser
        uname = uname_entry.get()
        password = password_entry.get()
        urole = role_inside.get()
        try:
            cursor.execute(f"INSERT INTO user_details (uname,password,urole) VALUES ('{uname}','{password}','{urole}');")
            con.commit()
            currentUser,currentRole = uname,urole
            sign_up_label = Label(menu_frame, text=f"Signed in as {currentUser} - {currentRole}")
            sign_up_label.pack()
            menu_frame.pack()
            sign_up_frame.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Username not available \n {e}")
    sign_up_submit = Button(sign_up_frame, text="Submit", command=submit)
    sign_up_submit.pack()
currentUser = ''
currentRole = ''



auth_frame = Frame(root)
auth_frame.pack()
authentication_label = Label(auth_frame, text="")
authentication_label.pack()
auth_label = Label(auth_frame, text="Enter MySQL Password: ")
auth_label.pack()
auth_entry = Entry(auth_frame, fg="red")
auth_entry.pack()
auth_button = Button(auth_frame, text="Authenticate", command=auth)
auth_button.pack()

sign_frame = Frame(root)
sign_in_btn = Button(sign_frame, text = "Sign in", command = sign_in)
sign_in_btn.pack()
sign_up_btn = Button(sign_frame, text = "Sign up", command = sign_up)
sign_up_btn.pack()

#sign IN
sign_in_frame = Frame(root)
sign_in_h1 = Label(sign_in_frame, text="Sign in")
sign_in_h1.pack()


#sign UP
sign_up_frame = Frame(root)
sign_up_h1 = Label(sign_up_frame,text = "Sign up")
sign_up_h1.pack()


menu_frame =Frame(root)


root.mainloop()
