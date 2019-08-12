#To DB
from sqlalchemy import create_engine
import os
import pandas as pd
conn_url = "postgresql://postgres:<DETAILS TO THE POSTGRESSQL SERVER WHERE THE DATABASE WILL BE STORED>"

engine = create_engine(conn_url)

connection = engine.connect()

os.chdir('/Users/luislosada/Columbia Drive/SQL Project 2019/Tables')

country = pd.read_csv('country_table.csv')
country.columns = map(str.lower, country.columns)
country.to_sql(name='country',con=engine,if_exists='append',index=False, schema='vehicle_collection')

sales_method = pd.read_csv('sales_method_table.csv')
sales_method.columns = map(str.lower, sales_method.columns)
sales_method.to_sql(name='sales_method',con=engine,if_exists='append',index=False, schema='vehicle_collection')

payment_method = pd.read_csv('payment_method_table.csv')
payment_method.columns = map(str.lower, payment_method.columns)
payment_method.to_sql(name='payment_method',con=engine,if_exists='append',index=False,schema='vehicle_collection')

address = pd.read_csv('address_table.csv')
address.columns = map(str.lower, address.columns)
address.to_sql(name='address',con=engine,if_exists='append',index=False,schema='vehicle_collection')

branch = pd.read_csv('branch_table.csv').fillna('NA')
branch.columns = map(str.lower, branch.columns)
branch.to_sql(name='branch',con=engine,if_exists='append',index=False,schema='vehicle_collection')

customers = pd.read_csv('customers_table.csv')
customers.columns = map(str.lower, customers.columns)
customers.to_sql(name='customers',con=engine,if_exists='append',index=False,schema='vehicle_collection')

product_line = pd.read_csv('product_line_table.csv')
product_line.columns = map(str.lower, product_line.columns)
product_line.to_sql(name='product_line',con=engine,if_exists='append',index=False,schema='vehicle_collection')

supplier = pd.read_csv('supplier_table.csv')
supplier.columns = map(str.lower, supplier.columns)
supplier.to_sql(name='supplier',con=engine,if_exists='append',index=False,schema='vehicle_collection')

products = pd.read_csv('products_table.csv')
products.columns = map(str.lower, products.columns)
products.to_sql(name='products',con=engine,if_exists='append',index=False,schema='vehicle_collection')

sales_rep = pd.read_csv('sales_rep_table.csv')
sales_rep.columns = map(str.lower, sales_rep.columns)
sales_rep.to_sql(name='sales_rep',con=engine,if_exists='append',index=False,schema='vehicle_collection')

orders = pd.read_csv('orders_table.csv')
orders.columns = map(str.lower, orders.columns)
orders.to_sql(name='orders',con=engine,if_exists='append',index=False,schema='vehicle_collection')

calendar = pd.read_csv('calendar_table.csv')
calendar.columns = map(str.lower, calendar.columns)
calendar.to_sql(name='calendar',con=engine,if_exists='append',index=False,schema='vehicle_collection')

Orders_Products = pd.read_csv('orders_products_table.csv')
Orders_Products.columns = map(str.lower, Orders_Products.columns)
Orders_Products.to_sql(name='orders_products',con=engine,if_exists='append',index=False,schema='vehicle_collection')

deliveries = pd.read_csv('deliveries_table.csv')
deliveries.columns = map(str.lower, deliveries.columns)
deliveries.to_sql(name='deliveries',con=engine,if_exists='append',index=False,schema='vehicle_collection')

deliveries_orders = pd.read_csv('deliveries_orders_table.csv')
deliveries_orders.columns = map(str.lower, deliveries_orders.columns)
deliveries_orders.to_sql(name='deliveries_orders',con=engine,if_exists='append',index=False,schema='vehicle_collection')
