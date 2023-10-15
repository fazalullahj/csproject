import mysql.connector as mysql
password = input('Enter password: ')
con = mysql.connect(host = 'localhost', user = 'root', password = password)
if con.is_connected():
    print("Connected to MySQL database Successfully.")
cursor = con.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS my_database;")
cursor.execute('USE my_database;')

# all tables creation-->
# user details
cursor.execute('create table if not exists user_details(uID int(20) primary key, uname varchar(25), password varchar(25) , urole varchar(15));')
# product
cursor.execute('create table if not exists product(pID int(20) primary key, pname varchar(25), price float(10,2) , stock int(15));')
# sales
cursor.execute('create table if not exists sales(sID int(20) primary key, pID int, quantity_sold int(25) , total_price float(10,2), sale_date date, cashier int(20), foreign key (pID) references product(pID), foreign key (cashier) references user_details(uID));')