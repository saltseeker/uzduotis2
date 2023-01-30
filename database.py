from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///warehouse.db', echo=True)
Base = declarative_base()


class Warehouse(Base):
    __tablename__ = 'warehouses'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    products = relationship("Product", back_populates="warehouse")

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    amount = Column(Integer)
    warehouse_id = Column(Integer, ForeignKey('warehouses.id'))
    warehouse = relationship("Warehouse", back_populates="products")
    customers = relationship("Customer", secondary="purchases")
    
class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    purchases = relationship("Product", secondary="purchases")

class Purchase(Base):
    __tablename__ = 'purchases'
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), primary_key=True)
    amount = Column(Integer)

  
    
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()