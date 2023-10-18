from tkinter import *
import mysql.connector as mysql

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
    uname  = uname_entry.get()
    password = password_entry.get()
    def submit():
        try:
            cursor.execute(f"select * from user_details where uname='{uname}'")
            row = cursor.fetchone()
            if row is not None and password == row[1]:
                currentUser,currentRole = uname,row[2]
        except Exception as e:
                    print(e)
                    print('Error!')
                    quit()
    sign_in_submit = Button(sign_in_frame, text="Submit", command=submit)
    sign_in_submit.pack()
def sign_up():
    pass


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
sign_in_label = Label(sign_in_frame, text = f"Signed in as {currentUser} - {currentRole}")
sign_in_label.pack()
uname_entry = Entry(sign_in_frame,text = "Username")
uname_entry.pack()
password_entry = Entry(sign_in_frame,text = "Password")
password_entry.pack()

root.mainloop()
