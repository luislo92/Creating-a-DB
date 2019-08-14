
--Q1
SELECT "payment_method__via__payment_c"."payment_method" AS "payment_method", count(*) AS "count"
FROM "vehicle_collection"."orders_products"
LEFT JOIN "vehicle_collection"."payment_method" "payment_method__via__payment_c" ON "vehicle_collection"."orders_products"."payment_code" = "payment_method__via__payment_c"."payment_code"
GROUP BY "payment_method__via__payment_c"."payment_method"
ORDER BY "payment_method__via__payment_c"."payment_method" ASC;
--Q2
SELECT "country__via__country_code"."country" AS "country", count(*) AS "count"
FROM "vehicle_collection"."address"
LEFT JOIN "vehicle_collection"."country" "country__via__country_code" ON "vehicle_collection"."address"."country_code" = "country__via__country_code"."country_code"
GROUP BY "country__via__country_code"."country"
ORDER BY "count" DESC, "country__via__country_code"."country" ASC;
--Q3
SELECT "address__via__address_id"."country_code" AS "country_code", "vehicle_collection"."deliveries"."delivery_method" AS "delivery_method", count(*) AS "count"
FROM "vehicle_collection"."deliveries"
LEFT JOIN "vehicle_collection"."address" "address__via__address_id" ON "vehicle_collection"."deliveries"."address_id" = "address__via__address_id"."address_id"
WHERE ("vehicle_collection"."deliveries"."delivery_method" = 'Express'
    OR "vehicle_collection"."deliveries"."delivery_method" = 'No Rush' OR "vehicle_collection"."deliveries"."delivery_method" = 'Standard')
GROUP BY "address__via__address_id"."country_code", "vehicle_collection"."deliveries"."delivery_method"
ORDER BY "vehicle_collection"."deliveries"."delivery_method" DESC, "address__via__address_id"."country_code" ASC;
--Q4
select distinct on (branch_id) branch_id,sales_rep,count
from(
select sales_rep,branch_id,count(*) as count
from (select *
    FROM vehicle_collection.orders o
LEFT JOIN vehicle_collection.sales_rep sp ON o.sales_rep_id = sp.sales_rep_id) as foo
left join vehicle_collection.calendar c on foo.transaction_id = c.transaction_id
where sales_rep != 'Online' and year_id = '2005'
group by sales_rep, branch_id) as ah
ORDER  BY branch_id, count DESC NULLS LAST ;
--Q5
SELECT "products__via__productcode"."productname" AS "productname", count(*) AS "count"
FROM "vehicle_collection"."orders_products"
LEFT JOIN "vehicle_collection"."products" "products__via__productcode" ON "vehicle_collection"."orders_products"."productcode" = "products__via__productcode"."productcode"
GROUP BY "products__via__productcode"."productname"
ORDER BY "products__via__productcode"."count" DESC
LIMIT 20;
--Q6
SELECT "vehicle_collection"."deliveries"."branch_id" AS "branch_id", count(*) AS "count"
FROM "vehicle_collection"."deliveries"
GROUP BY "vehicle_collection"."deliveries"."branch_id"
ORDER BY "count" DESC, "vehicle_collection"."deliveries"."branch_id" ASC
;
--Q7
SELECT "product_line__via__product_lin"."productline" AS "productline", count(*) AS "count"
FROM "vehicle_collection"."products"
LEFT JOIN "vehicle_collection"."product_line" "product_line__via__product_lin" ON "vehicle_collection"."products"."product_line_code" = "product_line__via__product_lin"."product_line_code"
GROUP BY "product_line__via__product_lin"."productline"
ORDER BY "product_line__via__product_lin"."count" DESC ;
--Q8
SELECT "supplier__via__supplier_id"."suppliername" AS "suppliername", min("vehicle_collection"."orders_products"."priceeach") AS "min", avg("products__via__productcode"."msrp") AS "avg"
FROM "vehicle_collection"."orders_products"
LEFT JOIN "vehicle_collection"."supplier" "supplier__via__supplier_id" ON "vehicle_collection"."orders_products"."supplier_id" = "supplier__via__supplier_id"."supplier_id" LEFT JOIN "vehicle_collection"."products" "products__via__productcode" ON "vehicle_collection"."orders_products"."productcode" = "products__via__productcode"."productcode"
WHERE "products__via__productcode"."productname" = 'Boeing 707'
GROUP BY "supplier__via__supplier_id"."suppliername"
ORDER BY "supplier__via__supplier_id"."suppliername" ASC;

--Q10
SELECT "products__via__productcode"."productname" AS "productname", sum("vehicle_collection"."orders_products"."sales") AS "sum"
FROM "vehicle_collection"."orders_products"
LEFT JOIN "vehicle_collection"."products" "products__via__productcode" ON "vehicle_collection"."orders_products"."productcode" = "products__via__productcode"."productcode"
GROUP BY "products__via__productcode"."productname"
ORDER BY "sum" DESC, "products__via__productcode"."productname" ASC
LIMIT 10;
--Q10
SELECT "products__via__productcode"."productname" AS "productname", count(*) AS "count"
FROM "vehicle_collection"."orders_products"
LEFT JOIN "vehicle_collection"."products" "products__via__productcode" ON "vehicle_collection"."orders_products"."productcode" = "products__via__productcode"."productcode"
GROUP BY "products__via__productcode"."productname"
ORDER BY "products__via__productcode"."count" DESC
LIMIT 10;

--Q11
SELECT pl.productline,to_char(date(c.orderdate),'YYYY-QTR') as year_quarter, count(*) as count
FROM orders o
    NATURAL JOIN calendar c
    left join orders_products op
        on o.transaction_id = op.transaction_id
    left join products p
        on p.productcode = op.productcode
    left join product_line pl
        on pl.product_line_code = p.product_line_code
    GROUP BY year_quarter,pl.productline
    order by year_quarter asc;

--Q12
with sec as(
select *
    from(
select productname, productcode,round(AVG((priceeach - msrp)/MSRP)*100,2) as pp
                    from(products natural join orders_products)
                    GROUP BY productname,productcode
                    order by pp DESC
                    limit 10
                    ) as foo
natural join orders_products )
select sec.productname, sec.dealsize,round(AVG((priceeach - msrp)/MSRP)*100,2) as profit_perc
from (sec natural join products)
GROUP BY sec.productname,sec.dealsize
order by productname ASC;



