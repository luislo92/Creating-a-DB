import pandas as pd
import os
import xlrd
os.chdir('/Users/luislosada/Columbia Drive/SQL Project 2019')

data = pd.read_csv('sales_data_sample.csv',encoding='latin-1')
data[['TERRITORY']] = data[['TERRITORY']].fillna('NA') #NA is interpreted as missing value when reading the file but it is actually an abbreviation for North America
tables = pd.read_excel('Table_Attributes.xlsx',encoding='latin-1')
table_names = tables.Table.unique()

#Set Up

def id_creator(x,names):
    df = pd.DataFrame(columns=names)
    for i in range(len(names)):
        id_for = []
        fv = list(names[i])
        if names[i].find('_') >= 0:
            for j in range(len(x)):
                num = str(j + 1)
                dash = names[i].find('_')+1
                if len(num) < 4:
                    zz = [0] * (4 - len(num))
                    zz = "".join(map(str, zz))
                nn = ''.join(fv[0] + fv[dash] + zz + num).lower()
                id_for.append(nn)
        else:
            for j in range(len(x)):
                num = str(j+1)
                if len(num) < 4:
                    zz = [0] * (4 - len(num))
                    zz = "".join(map(str, zz))
                nn = ''.join(fv[0]+fv[1]+zz+num).lower()
                id_for.append(nn)
        df[names[i]] = id_for
    return df

id_table = id_creator(data,table_names)

def add_to_table(pre,add,what_to_add):
    hh = []
    name = what_to_add.name
    for pp in range(len(pre)):
        for cu in range(len(add)):
            if add.loc[cu] == pre[pp]:
                hh.append(what_to_add.loc[cu])
    hh = pd.Series(hh,name=name)
    return hh

#Country Table
def country_code(var,distinct=True):
    if distinct == True:
        var = var.unique()
    else:
        var = var
    cc = []
    oc = []
    for i in range(len(var)):
        oc.append(var[i])
        if var[i] == 'USA' or var[i] == 'United States':
            cc.append('USA')
        elif var[i] == 'France':
            cc.append('FRA')
        elif var[i] == 'Norway':
            cc.append('NOR')
        elif var[i] == 'Australia':
            cc.append('AUS')
        elif var[i] == 'Finland':
            cc.append('FIN')
        elif var[i] == 'Austria':
            cc.append('AUT')
        elif var[i] == 'UK' or var[i] == 'United Kingdom':
            cc.append('GBR')
        elif var[i] == 'Spain':
            cc.append('ESP')
        elif var[i] == 'Sweden':
            cc.append('SWE')
        elif var[i] == 'Singapore':
            cc.append('SGP')
        elif var[i] == 'Canada':
            cc.append('CAN')
        elif var[i] == 'Japan':
            cc.append('JPN')
        elif var[i] == 'Italy':
            cc.append('ITA')
        elif var[i] == 'Denmark':
            cc.append('DNK')
        elif var[i] == 'Belgium':
            cc.append('BEL')
        elif var[i] == 'Philippines':
            cc.append('PHL')
        elif var[i] == 'Germany':
            cc.append('DEU')
        elif var[i] == 'Switzerland':
            cc.append('CHE')
        elif var[i] == 'Ireland':
            cc.append('IRL')
        else:
            cc.append('NaN')
    cc = pd.Series(cc)
    oc = pd.Series(oc)
    cc = cc.rename('COUNTRY_CODE')
    oc = oc.rename('COUNTRY')
    cdf = pd.concat([oc, cc], axis=1)
    return cdf
country = country_code(data.COUNTRY)

country.to_csv('country_table.csv',index=False)

data.insert(loc=data.columns.get_loc('COUNTRY')+1,column='COUNTRY_CODE',value=add_to_table(data.COUNTRY,country.COUNTRY,country.COUNTRY_CODE))


#Address Table
pre_address = data[['CITY','POSTALCODE','ADDRESSLINE1','ADDRESSLINE2','COUNTRY']]
hh = []
for pre in range(len(pre_address.COUNTRY)):
    for cu in range(len(country.COUNTRY)):
        if country.COUNTRY.loc[cu] == pre_address.COUNTRY[pre]:
            hh.append(country.COUNTRY_CODE.loc[cu])
hh = pd.Series(hh,name='COUNTRY_CODE')
pre_address = pd.concat([pre_address,hh],axis=1)
pre_address = pre_address.drop(['COUNTRY'],axis=1)
pre_address = pre_address.drop_duplicates()
pre_address = pre_address.reset_index(drop=True)
address = pd.concat([id_table[["Address"]][0:len(pre_address)],pre_address],axis=1)
address = address.rename(columns={"Address": "ADDRESS_ID"})

address.to_csv('address_table.csv',index=False)

#Branch
pre_branch = data[['TERRITORY','COUNTRY_CODE']]
pre_branch = pre_branch.drop_duplicates()
pre_branch = pre_branch.reset_index(drop=True)
branch = pd.concat([id_table[['Branch']][0:len(pre_branch)],pre_branch],axis=1)
branch = branch.rename(columns={"Branch": "BRANCH_ID"})

branch.to_csv('branch_table.csv',index=False)

#Customers
pre_customers = data[['CUSTOMERNAME','PHONE','CONTACTLASTNAME','CONTACTFIRSTNAME']]
pre_customers = pre_customers.drop_duplicates()
pre_customers = pre_customers.reset_index(drop=True)
customers = pd.concat([id_table[['Customers']][0:len(pre_customers)],pre_customers],axis=1)
customers = customers.rename(columns={"Customers": "CUSTOMER_ID"})

customers.to_csv('customers_table.csv',index=False)

#Product Line
pre_PL = data[['PRODUCTLINE']]
pre_PL = pre_PL.drop_duplicates()
pre_PL = pre_PL.reset_index(drop=True)
product_line = pd.concat([id_table[['Product_Line']][0:len(pre_PL)],pre_PL],axis=1)
product_line = product_line.rename(columns={"Product_Line": "PRODUCT_LINE_CODE"})

product_line.to_csv('product_line_table.csv',index=False)

#Products
pre_products = data[['PRODUCTCODE','PRODUCTNAME','MSRP','PRODUCTLINE']]
pre_products = pre_products.drop_duplicates().reset_index(drop=True)

products = pd.concat([pre_products,add_to_table(pre_products.PRODUCTLINE,product_line.PRODUCTLINE,product_line.PRODUCT_LINE_CODE)],axis=1)
products = products.drop(['PRODUCTLINE'],axis=1)

products.to_csv('products_table.csv',index=False)

#Calendar
pre_cal = data[['ORDERDATE','MONTH_ID','QTR_ID','YEAR_ID']]
data['ORDERDATE'] = pd.to_datetime(data['ORDERDATE'],infer_datetime_format=True)
data.insert(loc=data.columns.get_loc('QTR_ID'),column='DAY_ID',value=data['ORDERDATE'].dt.day)

calendar = data[['ORDERNUMBER','ORDERDATE','DAY_ID','MONTH_ID','QTR_ID','YEAR_ID']]

calendar.to_csv('calendar_table.csv',index=False)

#Supplier
data.insert(loc = 18,column='ADDRESS_ID',value=add_to_table(data.ADDRESSLINE1,address.ADDRESSLINE1,address.ADDRESS_ID))
pre_sup = data[['SUPPLIERNAME']]
pre_sup = pre_sup.drop_duplicates().reset_index(drop=True)
supplier = pd.concat([id_table[['Supplier']][0:len(pre_sup)],pre_sup],axis=1)
supplier = supplier.rename(columns={"Supplier": "SUPPLIER_ID"})
data.insert(loc = data.columns.get_loc('SUPPLIERNAME'),column='SUPPLIER_ID',value=add_to_table(data.SUPPLIERNAME,supplier.SUPPLIERNAME,supplier.SUPPLIER_ID))
data.insert(loc = data.columns.get_loc('CUSTOMERNAME'),column='CUSTOMER_ID',value=add_to_table(data.CUSTOMERNAME,customers.CUSTOMERNAME,customers.CUSTOMER_ID))

supplier.to_csv('supplier_table.csv',index=False)

#Orders_Product
Orders_Products = data[['ORDERNUMBER','PRODUCTCODE','QUANTITYORDERED','PRICEEACH','SALES','DEALSIZE']]
Orders_Products.to_csv('orders_products_table.csv',index=False)

#Sales Rep
import random
import numpy as np

def add_to_table2(pre,add,pre2,add2,what_to_add):
    hh = []
    name = what_to_add.name
    for pp in range(len(pre)):
        for cu in range(len(add)):
            if add.loc[cu] == pre[pp] and add2.loc[cu] == pre2[pp]:
                hh.append(what_to_add.loc[cu])
    hh = pd.Series(hh,name=name)
    return hh

data.insert(loc = data.columns.get_loc('TERRITORY'),column='BRANCH_ID',value=add_to_table2(data.TERRITORY,branch.TERRITORY,data.COUNTRY_CODE,branch.COUNTRY_CODE,branch.BRANCH_ID))

def assign_rep(id,data):
    rep = [['Nicole Delano', 'Wilhelmina Cash'], ['Delpha Blackston', 'Shane Canez'],
           ['Renita Henriquez', 'Rosalie Ethier'], ['Son Bjork', 'Hayley Rivenbark'], ['Bree Leist', 'Lulu Harries'],
           ['Anton Kittredge', 'Leisha Hannibal'], ['Tangela Valencia', 'Merlene Causey'],
           ['Rashad Vanguilder', 'Regina Mcnish'], ['Afton Zartman', 'Salome Reck'], ['Ramonita Zanders', 'Isa Swann'],
           ['Babara Mclaughin', 'Marta Tawil'], ['Loreen Kiesling', 'Jeanetta Edward'], ['Boyd Laver', 'Dustin Ozuna'],
           ['Mae Amsler', 'Nikia Flavors'], ['Bob Cisco', 'Allyson Harling'], ['Karsyn Robinson', 'Luka Norton'],
           ['Peyton Doyle', 'Maximus Romero'], ['Lana Chambers', 'Carmen Mcdonald'],
           ['Kaya Everett', 'Mikayla Charles'], ['Yoselin Tate', 'Adison Glenn']]
    data['SALES_REP'] = ''
    st=0
    ed=2 #the len of the data,2823, is divisible by 3 so it will fill the data in groups of 3
    ctr = 0
    for br in id:
        while ed <= len(data):
            data.loc[st:ed, 'SALES_REP'] = np.where(data.loc[st:ed].BRANCH_ID == br,
                                               random.choice(list(rep[ctr] + ['Online'])), data.loc[st:ed,'SALES_REP'])
            st = st+3
            ed = st+2
        st = 0
        ed = 2
        ctr += 1
    return data
assign_rep(branch.BRANCH_ID,data=data)

pre_sr = data[['SALES_REP','BRANCH_ID']]
pre_sr = pre_sr.drop_duplicates().reset_index(drop=True).sort_values(by=['BRANCH_ID','SALES_REP'])

sales_rep = pd.concat([id_table[['Sales_Rep']][0:len(pre_sr)],pre_sr],axis=1)
sales_rep = sales_rep.rename(columns={"Sales_Rep": "SALES_REP_ID"})

sales_rep.to_csv('sales_rep_table.csv',index=False)

data.insert(loc = data.columns.get_loc('SALES_REP'),column='SALES_REP_ID',value=add_to_table(data.SALES_REP,sales_rep.SALES_REP,sales_rep.SALES_REP_ID))

#Sales Method
def assign_sm(data):
    data['SALES_METHOD'] = ''
    data.SALES_METHOD = np.where(data.SALES_REP == 'Online',
                                               'Online Order', data.SALES_METHOD)
    prop_tab = pd.crosstab(index=data.CUSTOMERNAME, columns="count").sort_values('count')

    ind_small = prop_tab.iloc[np.where((prop_tab <= 50) & (prop_tab > 0))[0]].index
    for cnt in range(len(ind_small)):
        data.SALES_METHOD = np.where((data.CUSTOMERNAME == ind_small[cnt]) & (data.SALES_REP != 'Online'),
                                   'Sale Effort', data.SALES_METHOD)

    ind_big = prop_tab.iloc[np.where(prop_tab > 50)[0]].index
    for bcnt in range(len(ind_big)):
        data.SALES_METHOD = np.where((data.CUSTOMERNAME == ind_big[bcnt]) & (data.SALES_REP != 'Online'),
                                   'Recurrent', data.SALES_METHOD)
    return data
assign_sm(data)

pre_sm = data[['SALES_METHOD']]
pre_sm = pre_sm.drop_duplicates().reset_index(drop=True)
sales_method = pd.concat([id_table[['Sales_Method']][0:len(pre_sm)],pre_sm],axis=1)
sales_method = sales_method.rename(columns={"Sales_Method": "SALES_METHOD_CODE"})

sales_method.to_csv('sales_method_table.csv',index=False)

data.insert(loc = data.columns.get_loc('SALES_METHOD'),column='SALES_METHOD_CODE',value=add_to_table(data.SALES_METHOD,sales_method.SALES_METHOD,sales_method.SALES_METHOD_CODE))

#Payments
def assign_pay(data):
    data['PAYMENT_METHOD'] = ''
    rep = ['Wire Transfer', 'Credit Card', 'Cash', 'Check']
    data.PAYMENT_METHOD = np.where(data.SALES_REP == 'Online',
                                               'Credit Card', data.PAYMENT_METHOD)
    for i in range(len(data)):
        if data.loc[i, 'SALES_REP'] != 'Online':
            data.loc[i, 'PAYMENT_METHOD'] = random.choice(rep)
    return data
assign_pay(data)

pre_pay = data[['PAYMENT_METHOD']]
pre_pay = pre_pay.drop_duplicates().reset_index(drop=True)
payment_method = pd.concat([id_table[['Payments']][0:len(pre_pay)],pre_pay],axis=1)
payment_method = payment_method.rename(columns={"Payments": "PAYMENT_CODE"})

payment_method.to_csv('payment_method_table.csv',index=False)

data.insert(loc = data.columns.get_loc('PAYMENT_METHOD'),column='PAYMENT_CODE',value=add_to_table(data.PAYMENT_METHOD,payment_method.PAYMENT_METHOD,payment_method.PAYMENT_CODE))

#Orders
order = data[['ORDERNUMBER','CUSTOMER_ID','SALES_REP_ID','PAYMENT_CODE','STATUS']]

order.to_csv('order.csv',index=False)

#Deliveries_Orders
from datetime import timedelta

def add_d_date(od,data):
    data['DELIVERY_DATE'] = pd.Series(dtype='datetime64[ns]')
    data['DELIVERY_METHOD'] = pd.Series(dtype='str')
    data['DELIVERY_COST'] = pd.Series(dtype='float64')
    d = [3,4,5,6,7,8,9,12,13,14]
    od = od.ORDERNUMBER.drop_duplicates().reset_index(drop=True)
    for i in range(len(od)):
        ind = np.where(data.ORDERNUMBER == od[i])
        for j in ind:
            dd = random.choice(d)
            data.loc[j,'DELIVERY_DATE'] = data.loc[j,'ORDERDATE'] + timedelta(days=dd)
            if dd<=4:
                data.loc[j,'DELIVERY_METHOD'] = 'Express'
                data.loc[j, 'DELIVERY_COST'] = 10
            elif dd<=9:
                data.loc[j, 'DELIVERY_METHOD'] = 'Standard'
                data.loc[j, 'DELIVERY_COST'] = 6
            else:
                data.loc[j, 'DELIVERY_METHOD'] = 'No Rush'
                data.loc[j, 'DELIVERY_COST'] = 3
    return data

data = add_d_date(order,data)

pre_dev = data[['DELIVERY_DATE','ORDERNUMBER']]
pre_dev =pre_dev.drop_duplicates().reset_index(drop=True).sort_values(by='ORDERNUMBER')
deliveries_orders = pd.concat([id_table[['Deliveries']][0:len(pre_dev)],pre_dev],axis=1)
deliveries_orders = deliveries_orders.rename(columns={"Deliveries": "DELIVERY_ID"})

deliveries_orders.to_csv('deliveries_orders_table.csv',index=False)
data.insert(loc = data.columns.get_loc('DELIVERY_DATE'),column='DELIVERY_ID',value=add_to_table(data.ORDERNUMBER,deliveries_orders.ORDERNUMBER,deliveries_orders.DELIVERY_ID))

#Deliveries

deliveries = data[['DELIVERY_ID','DELIVERY_DATE','CUSTOMER_ID','ADDRESS_ID','BRANCH_ID','DELIVERY_METHOD','DELIVERY_COST']]
deliveries = deliveries.drop_duplicates().reset_index(drop=True)

deliveries.to_csv('deliveries_table.csv',index=False)

data.to_csv('proccesedDATA.csv',index=False)

#To DB
from sqlalchemy import create_engine
conn_url = "postgresql://luislosada:2030@localhost:5432/vehicle_collection"

engine = create_engine(conn_url)

connection = engine.connect()

address.to_sql(name='address',con=engine,if_exists='append',index=False)
branch.to_sql(name='branch',con=engine,if_exists='append',index=False)
calendar.to_sql(name='calendar',con=engine,if_exists='append',index=False)
country.to_sql(name='country',con=engine,if_exists='append',index=False)
customers.to_sql(name='customers',con=engine,if_exists='append',index=False)
deliveries.to_sql(name='deliveries',con=engine,if_exists='append',index=False)
deliveries_orders.to_sql(name='deliveries_orders',con=engine,if_exists='append',index=False)
order.to_sql(name='order',con=engine,if_exists='append',index=False)
Orders_Products.to_sql(name='orders_products',con=engine,if_exists='append',index=False)
payment_method.to_sql(name='payment',con=engine,if_exists='append',index=False)
products.to_sql(name='products',con=engine,if_exists='append',index=False)
product_line.to_sql(name='product_line',con=engine,if_exists='append',index=False)
sales_rep.to_sql(name='sales_rep',con=engine,if_exists='append',index=False)
supplier.to_sql(name='supplier',con=engine,if_exists='append',index=False)
sales_method.to_sql(name='sales_method',con=engine,if_exists='append',index=False)
