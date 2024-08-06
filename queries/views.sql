-- Представление для агрегации продаж с датой
create or replace view sales_summary as
select 
    sm.date as date,
    date_trunc('month', sm.date) as month,
    c.customer,
    sum(sm.sold_quantity) as total_sold_quantity
from 
    sales_monthly sm
join 
    customer c on sm.customer_code = c.customer_code
where 
    sm.date between '2017-01-01' and '2023-12-31'
group by 
    date_trunc('month', sm.date),
    c.customer,
    sm.date;

-- представление для агрегации данных о доходах от продаж по категориям продуктов, годам и платформам клиентов
create or replace view sales_revenue_summary as
select 
    p.category,
    extract(year from sd.date) as year,
    c.platform,
    sum(sd.gross_price * sd.sold_quantity) as total_revenue
from 
    sales_domain sd
join 
    product p on sd.product_code = p.product_code
join 
    customer c on sd.customer_code = c.customer_code
group by 
    p.category,
    extract(year from sd.date),
    c.platform
order by 
    p.category, 
    year, 
    c.platform;

-- представление, которое агрегирует данные о доходах от продаж по каналам и рынкам
create or replace view channel_market_revenue as
select 
    channel, 
    market, 
    sum(gross_price) as revenue
from 
    sales_domain
group by 
    channel, 
    market;


-- представление агрегирует данные о количестве продаж по годам, месяцам и регионам клиентов
create or replace view monthly_sales_summary as
select
    extract(year from sm.date) as year,
    extract(month from sm.date) as month,
    c.region,
    count(*) as sales_count
from
    sales_monthly sm
inner join
    customer c on c.customer_code = sm.customer_code
group by
    extract(year from sm.date),
    extract(month from sm.date),
    c.region;


-- представление для агрегации данныч о продажах продуктов за три месяца с использованием оконной функции
create or replace view product_sales_summary as
with sales_with_lag as (
    select
        sm.product_code,
        sm.date,
        sum(sm.sold_quantity) over (
            partition by sm.product_code
            order by sm.date
            rows between 2 preceding and current row
        ) as three_month_sales
    from
        sales_monthly sm
)
select
    p.product,
    swl.date,
    max(swl.three_month_sales) as three_month_sales
from
    sales_with_lag swl
join
    product p on swl.product_code = p.product_code
group by
    p.product,
    swl.date
order by
    p.product,
    swl.date;


-- представление которое агрегирует данные о валовой цене продуктов по годам
create or replace view yearly_product_gross_price as
select 
    extract(year from sm.date) as year,
    p.product,
    sum(gp.gross_price) as total_gross_price
from 
    sales_monthly sm
join 
    product p on sm.product_code = p.product_code
join 
    gross_price gp on sm.product_code = gp.product_code
group by 
    extract(year from sm.date),
    p.product
order by 
    year, 
    p.product;
