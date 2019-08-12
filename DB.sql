set search_path to team_5;

drop schema if exists vehicle_collection cascade;

create schema vehicle_collection;

set search_path = 'vehicle_collection';

CREATE TABLE COUNTRY(
COUNTRY_CODE CHAR(3) NOT NULL,
COUNTRY VARCHAR(30) NOT NULL,
PRIMARY KEY (COUNTRY_CODE)
);

CREATE TABLE SALES_METHOD(
SALES_METHOD_CODE CHAR(6) NOT NULL,
SALES_METHOD VARCHAR(30) NOT NULL,
PRIMARY KEY (SALES_METHOD_CODE),
CHECK (SALES_METHOD IN ('Sale Effort', 'Online Order', 'Recurrent'))
);


CREATE TABLE PAYMENT_METHOD(
PAYMENT_CODE CHAR(6) NOT NULL,
PAYMENT_METHOD VARCHAR(30) NOT NULL,
PRIMARY KEY (PAYMENT_CODE),
CHECK (PAYMENT_METHOD IN ('Credit Card', 'Wire Transfer', 'Cash', 'Check'))
);

CREATE TABLE ADDRESS(
ADDRESS_ID CHAR(6) NOT NULL,
COUNTRY_CODE CHAR(3) NOT NULL,
CITY VARCHAR(30),
POSTALCODE  VARCHAR(20),
ADDRESSLINE1 TEXT,
ADDRESSLINE2 TEXT,
PRIMARY KEY (ADDRESS_ID),
FOREIGN KEY (COUNTRY_CODE) REFERENCES COUNTRY(COUNTRY_CODE)
ON UPDATE CASCADE
ON DELETE CASCADE
);

CREATE TABLE BRANCH(
BRANCH_ID CHAR(6) NOT NULL,
TERRITORY_CODE VARCHAR(10) NOT NULL,
COUNTRY_CODE CHAR(3) NOT NULL,
PRIMARY KEY (BRANCH_ID),
FOREIGN KEY (COUNTRY_CODE) REFERENCES COUNTRY(COUNTRY_CODE)
ON UPDATE CASCADE
ON DELETE CASCADE
);

CREATE TABLE CUSTOMERS(
CUSTOMER_ID CHAR(6) NOT NULL,
CUSTOMERNAME VARCHAR(50) NOT NULL,
PHONE VARCHAR(30) NOT NULL,
CONTACTLASTNAME VARCHAR(30) NOT NULL,
CONTACTFIRSTNAME VARCHAR(30) NOT NULL,
PRIMARY KEY (CUSTOMER_ID)
);


CREATE TABLE PRODUCT_LINE(
PRODUCT_LINE_CODE CHAR(6) NOT NULL,
PRODUCTLINE VARCHAR(30) NOT NULL,
PRIMARY KEY(PRODUCT_LINE_CODE)
);

CREATE TABLE SUPPLIER(
SUPPLIER_ID CHAR(6) NOT NULL,
SUPPLIERNAME VARCHAR(30),
PRIMARY KEY (SUPPLIER_ID)
);

CREATE TABLE PRODUCTS (
PRODUCTCODE VARCHAR(10) NOT NULL,
PRODUCTNAME VARCHAR(30),
PRODUCT_LINE_CODE CHAR(6) NOT NULL,
MSRP INTEGER,
PRIMARY KEY(PRODUCTCODE),
FOREIGN KEY (PRODUCT_LINE_CODE) REFERENCES PRODUCT_LINE(PRODUCT_LINE_CODE)
ON UPDATE CASCADE
ON DELETE CASCADE
);

CREATE TABLE SALES_REP(
SALES_REP_ID CHAR(6) NOT NULL,
BRANCH_ID CHAR(6) NOT NULL,
SALES_REP VARCHAR(30),
PRIMARY KEY (SALES_REP_ID),
FOREIGN KEY (BRANCH_ID) REFERENCES BRANCH(BRANCH_ID)
ON UPDATE CASCADE
ON DELETE CASCADE
);


CREATE TABLE ORDERS (
ORDERNUMBER INTEGER NOT NULL,
ORDERLINENUMBER INT NOT NULL,
CUSTOMER_ID CHAR(6) NOT NULL,
STATUS VARCHAR(20),
SALES_REP_ID CHAR(6),
SALES_METHOD_CODE CHAR(6) NOT NULL,
PRIMARY KEY(ORDERNUMBER,ORDERLINENUMBER),
FOREIGN KEY (CUSTOMER_ID) REFERENCES CUSTOMERS(CUSTOMER_ID)
ON UPDATE CASCADE
ON DELETE CASCADE,
FOREIGN KEY (SALES_REP_ID) REFERENCES SALES_REP(SALES_REP_ID)
ON UPDATE CASCADE
ON DELETE CASCADE,
FOREIGN KEY (SALES_METHOD_CODE) REFERENCES SALES_METHOD(SALES_METHOD_CODE)
ON UPDATE CASCADE
ON DELETE CASCADE,
CHECK (STATUS IN ('Shipped', 'Disputed', 'In Process', 'Cancelled', 'On Hold', 'Resolved'))
);

CREATE TABLE CALENDAR (
ORDERNUMBER INTEGER NOT NULL,
ORDERLINENUMBER INT NOT NULL,
ORDERDATE DATE NOT NULL,
YEAR_ID NUMERIC(4),
MONTH_ID NUMERIC(2),
DAY_ID NUMERIC(2),
QTR_ID NUMERIC(2),
FOREIGN KEY (ORDERNUMBER,ORDERLINENUMBER) REFERENCES ORDERS(ORDERNUMBER,ORDERLINENUMBER)
ON UPDATE CASCADE
ON DELETE CASCADE
);

CREATE TABLE ORDERS_PRODUCTS(
ORDERNUMBER INTEGER NOT NULL,
ORDERLINENUMBER INT NOT NULL,
PRODUCTCODE VARCHAR(10) NOT NULL,
SUPPLIER_ID CHAR(6) NOT NULL,
QUANTITYORDERED INTEGER,
PRICEEACH NUMERIC,
SALES NUMERIC,
DEALSIZE VARCHAR(10),
PAYMENT_CODE CHAR(6),
FOREIGN KEY (PAYMENT_CODE) REFERENCES PAYMENT_METHOD(PAYMENT_CODE)
ON UPDATE CASCADE
ON DELETE CASCADE,
FOREIGN KEY (SUPPLIER_ID) REFERENCES SUPPLIER(SUPPLIER_ID)
ON UPDATE CASCADE
ON DELETE CASCADE,
PRIMARY KEY(ORDERNUMBER,ORDERLINENUMBER,PRODUCTCODE),
FOREIGN KEY (ORDERNUMBER,ORDERLINENUMBER) REFERENCES ORDERS(ORDERNUMBER,ORDERLINENUMBER)
ON UPDATE CASCADE
ON DELETE CASCADE,
FOREIGN KEY (PRODUCTCODE) REFERENCES PRODUCTS(PRODUCTCODE)
ON UPDATE CASCADE
ON DELETE CASCADE,
CHECK (DEALSIZE IN ('Small', 'Medium', 'Large'))
);

CREATE TABLE DELIVERIES (
DELIVERY_ID CHAR(6) NOT NULL,
DELIVERY_DATE DATE NOT NULL,
CUSTOMER_ID CHAR(6) NOT NULL,
ADDRESS_ID CHAR(6) NOT NULL,
BRANCH_ID CHAR(6) NOT NULL,
DELIVERY_METHOD VARCHAR(10) NOT NULL,
DELIVERY_COST INTEGER,
PRIMARY KEY (DELIVERY_ID),
FOREIGN KEY (CUSTOMER_ID) REFERENCES CUSTOMERS(CUSTOMER_ID)
ON UPDATE CASCADE
ON DELETE CASCADE,
FOREIGN KEY (ADDRESS_ID) REFERENCES ADDRESS(ADDRESS_ID)
ON UPDATE CASCADE
ON DELETE CASCADE,
FOREIGN KEY (BRANCH_ID) REFERENCES BRANCH(BRANCH_ID)
ON UPDATE CASCADE
ON DELETE CASCADE,
CHECK (DELIVERY_METHOD IN ('Standard', 'Express', 'No Rush'))
);

CREATE TABLE DELIVERIES_ORDERS(
DELIVERY_ID CHAR(6) NOT NULL,
DELIVERY_DATE DATE NOT NULL,
ORDERNUMBER INTEGER NOT NULL,
ORDERLINENUMBER INT NOT NULL,
FOREIGN KEY (DELIVERY_ID) REFERENCES DELIVERIES(DELIVERY_ID)
ON UPDATE CASCADE
ON DELETE CASCADE,
FOREIGN KEY (ORDERNUMBER,ORDERLINENUMBER) REFERENCES ORDERS(ORDERNUMBER,ORDERLINENUMBER)
ON UPDATE CASCADE
ON DELETE CASCADE
);


--To Lucid Chart
SELECT 'postgresql' AS dbms,t.table_catalog,t.table_schema,t.table_name,c.column_name,c.ordinal_position,c.data_type,c.character_maximum_length,n.constraint_type,k2.table_schema,k2.table_name,k2.column_name FROM information_schema.tables t NATURAL LEFT JOIN information_schema.columns c LEFT JOIN(information_schema.key_column_usage k NATURAL JOIN information_schema.table_constraints n NATURAL LEFT JOIN information_schema.referential_constraints r)ON c.table_catalog=k.table_catalog AND c.table_schema=k.table_schema AND c.table_name=k.table_name AND c.column_name=k.column_name LEFT JOIN information_schema.key_column_usage k2 ON k.position_in_unique_constraint=k2.ordinal_position AND r.unique_constraint_catalog=k2.constraint_catalog AND r.unique_constraint_schema=k2.constraint_schema AND r.unique_constraint_name=k2.constraint_name WHERE t.TABLE_TYPE='BASE TABLE' AND t.table_schema NOT IN('information_schema','pg_catalog');