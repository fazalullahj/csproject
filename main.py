import mysql.connector as mysql
print("\t\t ABC Supermarket, Dubai branch\t\t")
#signin and sign up function -->
def authentication():
    choice = int(input('Sign In : 1\nSign Up : 2\nEnter your choice number: '))
#sign in
    if choice == 1:
        print('Welcome Back!')
        while True:
            uname = input('Enter Username: ')
            passwd = input('Enter password: ')
            try:
                cursor.execute(f"select * from user_details where uname='{uname}'")
                row = cursor.fetchone()
                if passwd == row[1]:
                    currentUser,currentRole = uname,row[2]
                    print(f'Signed In as {currentUser} - {currentRole} ')
                    
                    break
            except Exception as e:
                print(e)
                print('Error!')
#sign up
    elif choice == 2:
        print('New User Sign up!')
        while True:
            uname = input('Enter Username: ')
            passwd = input('Enter password: ')
            urole = input('Enter user role: ')
            try:
                cursor.execute(f"INSERT INTO user_details (uname,password,urole) VALUES ('{uname}','{passwd}','{urole}');")
                print('Account created successfully!')
                con.commit()
                currentUser,currentRole = uname,urole
                print(f'Signed In as {currentUser} - {currentRole} ')
                break
            except Exception as e:
                print('Username not available')
while True:
    try:
        password = input('Enter password: ')
        con = mysql.connect(host = 'localhost', user = 'root', password = password)
        if con.is_connected():
            print("Connected to MySQL database Successfully.")
            break
    except:
        print("Failed to connect to MySQL ")
#main menu
def menu():
    while True:
        choice = int(input("View products : 1\nAdd products : 2\nMake sale : 3\nQuit : 4\n Enter choice number: "))
        if choice == 1:
            viewproduct()
        elif choice == 2:
            addproduct()
        elif choice == 3:
            sale()
        elif choice == 4:
            break

def viewproduct():
    cursor.execute("Select * from product;")
    allproducts = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    #if no products
    if len(allproducts) == 0:
        print('No products')
    else:#displaying the table of data in a nice format
        print("\t".join(column_names))  # Print columnnames
        for row in allproducts:
            formatted_row = "\t".join(map(str, row))
            print(formatted_row)


def addproduct():
        pass

        
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



currentUser = ''
currentRole = ''
authentication()
menu()