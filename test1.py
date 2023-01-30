from tkinter import messagebox, font
from sqlalchemy.orm import sessionmaker
from database import *
import tkinter as tk


Session = sessionmaker(bind=engine)
session = Session()


def add_product():
    name = product_name_entry.get()
    price = int(product_price_entry.get())
    amount = int(product_amount_entry.get())
    warehouse_name = warehouse_name_entry.get()

    existing_product = session.query(Product).filter_by(name=name).all()
    product_exists = False
    for product in existing_product:
        if product.warehouse.name == warehouse_name:
            product_exists = True
            product.price = price
            product.amount = amount
            break
    
    if not product_exists:
        new_product = Product(name=name, price=price, amount=amount)
        new_warehouse = Warehouse(name=warehouse_name)
        new_warehouse.products.append(new_product)
        session.add(new_warehouse)

    session.commit()
    messagebox.showinfo("Product Added/Updated", "The product has been added/updated in the database.")

    product = session.query(Product).filter_by(name=name).first()
    warehouse = session.query(Warehouse).filter_by(name=warehouse_name).first()

    purchase_text.config(state='normal')
    purchase_text.insert('1.0', f'Product Name: {product.name}\n')
    purchase_text.insert('2.0', f'Product Price: {product.price}\n')
    purchase_text.insert('3.0', f'Product Amount: {product.amount}\n')
    purchase_text.insert('4.0', f'Warehouse name: {warehouse.name}\n')
    purchase_text.config(state='disabled')



def show_purchases():
    purchases_window = tk.Toplevel(root)
    purchases_window.title("Purchases")

    header_font = tk.font.Font(weight="bold")
    tk.Label(purchases_window, text="Product Name", width=15, font=header_font).grid(row=0, column=0, sticky="w")
    tk.Label(purchases_window, text="Name", width=15, font=header_font).grid(row=0, column=1, sticky="w")
    tk.Label(purchases_window, text="Amount", width=10, font=header_font).grid(row=0, column=2, sticky="w")

    purchases = session.query(Purchase, Product, Customer)\
        .join(Product, Purchase.product_id == Product.id)\
        .join(Customer, Purchase.customer_id == Customer.id).all()
    
    for i, (purchase, product, customer) in enumerate(purchases, 1):
        tk.Label(purchases_window, text=product.name, width=15).grid(row=i, column=0, sticky="w")
        tk.Label(purchases_window, text=f"{customer.name} {customer.surname}", width=20).grid(row=i, column=1, sticky="w")
        tk.Label(purchases_window, text=str(purchase.amount), width=10).grid(row=i, column=2, sticky="w")
        
    


def show_warehouse_info():
    warehouse_window = tk.Toplevel(root)
    warehouse_window.title("Warehouse Info")

    header_font = tk.font.Font(weight="bold")
    tk.Label(warehouse_window, text="Warehouse Name", font=header_font).grid(row=0, column=0, sticky="w")
    tk.Label(warehouse_window, text="Product Name", font=header_font).grid(row=0, column=1, sticky="w")
    tk.Label(warehouse_window, text="Amount", font=header_font).grid(row=0, column=2, sticky="w")
    tk.Label(warehouse_window, text="Price", font=header_font).grid(row=0, column=3, sticky="w")

    warehouses = session.query(Warehouse, Product).join(Product).all()

    for i, (warehouse, product) in enumerate(warehouses, 1):
        tk.Label(warehouse_window, text=warehouse.name, width=20).grid(row=i, column=0, sticky="w")
        tk.Label(warehouse_window, text=product.name, width=20).grid(row=i, column=1, sticky="w")
        tk.Label(warehouse_window, text=str(product.amount), width=10).grid(row=i, column=2, sticky="w")
        tk.Label(warehouse_window, text=str(product.price), width=5).grid(row=i, column=3, sticky="w")



def search_product():
    name = product_name_entry.get()
    products = session.query(Product).filter_by(name=name).all()
    warehouses = session.query(Warehouse).filter(Warehouse.products.any(Product.name == name)).all()
    
    if products:
        purchase_text.config(state='normal')
        purchase_text.delete('1.0', 'end')
        purchase_text.see("1.0")
        for i, product in enumerate(products):
            warehouse = warehouses[i]
            purchase_text.insert('1.0', f'Product Name: {product.name}\n')
            purchase_text.insert('2.0', f'Product Price: {product.price}\n')
            purchase_text.insert('3.0', f'Product Amount: {product.amount}\n')
            purchase_text.insert('4.0', f'Warehouse Name: {warehouse.name}\n\n')
        purchase_text.config(state='disabled')
    else:
        messagebox.showinfo("Product Not Found", "The product was not found in the database.")






    
# Create the main window
root = tk.Tk()
root.geometry("300x700")
root.title("Product Database")

bottom_frame = tk.Frame(root)
bottom_frame.pack(side='bottom', fill='both', expand=True)

# Create labels and entry widgets for product name, price, and amount
product_name_label = tk.Label(root, text="Product Name:")
product_name_label.pack()
product_name_entry = tk.Entry(root)
product_name_entry.pack()
product_price_label = tk.Label(root, text="Product Price:")
product_price_label.pack()
product_price_entry = tk.Entry(root)
product_price_entry.pack()
product_amount_label = tk.Label(root, text="Product Amount:")
product_amount_label.pack()
product_amount_entry = tk.Entry(root)
product_amount_entry.pack()
warehouse_name_label = tk.Label(root, text="Warehouse name:")
warehouse_name_label.pack()
warehouse_name_entry = tk.Entry(root)
warehouse_name_entry.pack()

# Creating a label and a text widget to display the product information.
purchase_label = tk.Label(bottom_frame, text="Product Added/Updated")
purchase_label.pack()
purchase_text = tk.Text(bottom_frame, height=20, width=30)
purchase_text.pack()
purchase_text.config(state='disabled')

# Create a button to add the product to the database
warehouse_info_button = tk.Button(root, text="Show Warehouse Info", command=show_warehouse_info, width=20, height=1)
warehouse_info_button.pack(pady=2)
show_purchases_button = tk.Button(root, text="Show Purchases", command=show_purchases, width=20, height=1)
show_purchases_button.pack(pady=2)
add_button = tk.Button(root, text="Add Product", command=add_product, width=20, height=1)
add_button.pack(pady=2)
search_button = tk.Button(root, text="Search", command=search_product, width=20, height=1)
search_button.pack(pady=2)


root.mainloop()
