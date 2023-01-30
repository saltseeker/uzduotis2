from sqlalchemy.orm import sessionmaker
from database import *

Session = sessionmaker(bind=engine)
session = Session()



warehouses = [{'name': 'Warehouse 1'}, {'name': 'Warehouse 2'},{'name': 'Warehouse 3'} ]

session.bulk_insert_mappings(Warehouse, warehouses)


products = [{'name': 'Lighter', 'price': 10, 'amount': 100, 'warehouse_id': 1},
            {'name': 'Swiss Chard', 'price': 20, 'amount': 200, 'warehouse_id': 2},
            {'name': 'Flour', 'price': 170, 'amount': 600, 'warehouse_id': 1},
            {'name': 'Pastry', 'price': 84, 'amount': 750, 'warehouse_id': 3},
            {'name': 'Pork', 'price': 20, 'amount': 732, 'warehouse_id': 2},
            {'name': 'Pie Filling', 'price': 70, 'amount': 712, 'warehouse_id': 2},
            {'name': 'Juice ', 'price': 90, 'amount': 1233, 'warehouse_id': 1},
            {'name': 'Boogies', 'price': 51, 'amount': 452, 'warehouse_id': 2},
            {'name': 'Beef', 'price': 22, 'amount': 756, 'warehouse_id': 3}
            ]

session.bulk_insert_mappings(Product, products)


purchases = [Purchase(product_id=1, customer_id=2, amount=2),             
Purchase(product_id=2, customer_id=3, amount=3),             
Purchase(product_id=3, customer_id=4, amount=4),
Purchase(product_id=3, customer_id=2, amount=4),
Purchase(product_id=3, customer_id=1, amount=4)
]

for purchase in purchases:
    session.add(purchase)

session.commit()


customers = [    
    {'name': 'John', 'surname': 'Doe'},    
    {'name': 'Jane', 'surname': 'Doe'},    
    {'name': 'Jim', 'surname': 'Smith'},
    ]

for customer in customers:
    c = Customer(name=customer['name'], surname=customer['surname'])
    session.add(c)

session.commit()