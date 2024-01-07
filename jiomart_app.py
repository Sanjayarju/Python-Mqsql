from datetime import datetime
import mysql.connector
mydb = mysql.connector.connect(host='localhost', user='root', password='Sanjay@1', database='jiomart')
mycursor = mydb.cursor()

def validate_user(phn_no, password):
    mycursor.execute("select * from users where phn_no like %s", (phn_no,))
    user_data = mycursor.fetchall()
    if  user_data and user_data[0][-1] == password:
        print("Login Successful\n")
        print('--------------------------------------------------------------------------')
        return 1

def display_products():
    print('\n--------------------------------------------------------------------------')
    print('Categories:\n1. Dresses \n2. Mobiles \n3. Homeappliances \n4. Medicals')
    category = int(input("\nChoose the category: "))
    if category == 1:
        mycursor.execute("select * from products where category like %s", ('dresses',))
        datas = mycursor.fetchall()
    elif category == 2:
        mycursor.execute("select * from products where category like %s", ('mobiles',))
        datas = mycursor.fetchall()
    elif category == 3:
        mycursor.execute("select * from products where category like %s", ('Homeappliances',))
        datas = mycursor.fetchall()
    elif category == 4:
        mycursor.execute("select * from products where category like %s", ('medicals',))
        datas = mycursor.fetchall()
    else:
        print("Invalid option.")
        return None
    print()
    print('--------------------------------------------------------------------------')
    product_ids = []
    for data in datas:
        print(f"{data[0]}-ID:{data[1]} | Name:{data[2]} | Rs:{data[3]}/-", end='\n', sep='\n')
        product_ids.append(data[1])
    return select_products(product_ids)

def select_products(product_ids):
    selected_product_id = int(input("\nEnter the product id: "))
    if selected_product_id in product_ids:
        mycursor.execute("select * from products where productid like %s", (selected_product_id,))
        data = mycursor.fetchall()
        if data:
            quantity = int(input("Enter quantity: "))
            if quantity > 0:
                cost = data[0][3]*quantity
                print('\n--------------------------------------------------------------------------')
                print("Order Preview:\n")
                print(f'Product Name: {data[0][2]} \nQuantity: {quantity} \nCost: {cost}')
                confirm_order = int(input("\nEnter 1 to confirm order: "))
                if confirm_order == 1:
                    return [selected_product_id, quantity, cost]
                else:
                    print('Invalid option')
                    return None
            else:
                print("Invalid Quantity")
                return None
    else:
        print("Invalid Product Id.")
        return None


def place_order(user_name, selected_productid, quantity, cost, time):
    mycursor.execute('insert into orders values(%s, %s,%s,%s,%s)', (user_name, selected_productid, quantity, cost, time,))
    mydb.commit()

    print("Order Successful")


def display_orders(user_name):
    mycursor.execute('select * from orders where user_name like %s', (user_name,))
    data = mycursor.fetchall()
    if data:
        for i in range(len(data)):
            print(
                f'Phn_No: {data[i][0]} | Product Id: {data[i][1]} | Quantity: {data[i][2]} | Cost: {data[i][3]} | Time: {data[i][4]}')
        print("\n")
    else:
        print("No Orders done.")
        print('--------------------------------------------------------------------------\n')


print("JIOMART Store.com")
print('__________________________________________________________________________')
choice = input("\nLogin/Signup: ").title()
if choice == 'Login':
    phn_no = input("\nEnter the phn_no: ")
    password = input("Enter the password: ")
    if validate_user(phn_no, password):
        stay_in = True
        while stay_in:
            print("1. Order Now \n2. Order History \n3. Logout\n")
            choice = int(input("Select among the options: "))
            if choice == 1:
                product_details = display_products()
                if product_details:
                    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    place_order(phn_no, product_details[0], product_details[1], product_details[2], time)
            if choice == 2:
                display_orders(phn_no)
            if choice == 3:
                print("\nLogout Successfully")
                stay_in = False
    else:
        print("Invalid Mail Id / Password.")

elif choice == 'Signup':
    user_name = input('\nEnter user name: ')
    phn_no = input('Enter your mobile number: ')
    password = input("Enter a strong password: ")
    #To avoid insertion of duplicate mail ids and errors by using try and except technique.
    try:
        mycursor.execute('insert into users values (%s, %s, %s)', (user_name, phn_no, password,))
        mydb.commit()
        print('Signed Up Successfully')
    except:
        print("Phn_No already exists.")