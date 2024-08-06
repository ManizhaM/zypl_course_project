-- Создание таблицы customer_dim
create table customer (
    customer_code int primary key,
    customer varchar(255),
    platform varchar(255),
    channel varchar(255),
    market varchar(255),
    sub_zone varchar(255),
    region varchar(255)  
);

-- Создание таблицы product_dim
create table product (
    product_code varchar(255) primary key,
    division varchar(255)  ,
    segment varchar(255)  ,
    category varchar(255)  ,
    product varchar(255)  ,
    variant varchar(255)  
);

-- Создание таблицы gross_price_fact
create table gross_price (
    product_code varchar(255),
    fiscal_year int,
    gross_price numeric(10, 4),
    primary key (product_code, fiscal_year),
    foreign key (product_code) references product(product_code)
);

-- Создание таблицы manufacturing_cost_fact
create table manufacturing_cost (
    product_code varchar(255),
    cost_year int,
    manufacturing_cost numeric(10, 4),
    primary key (product_code, cost_year),
    foreign key (product_code) references product(product_code)
);

-- Создание таблицы pre_discount_fact
create table pre_discount (
    customer_code int,
    fiscal_year int,
    pre_invoice_discount_pct numeric(10, 4),
    primary key (customer_code, fiscal_year),
    foreign key (customer_code) references customer(customer_code)
);

-- Создание таблицы sales_monthly_fact
create table sales_monthly (
    date date,
    product_code varchar(255),
    customer_code int,
    sold_quantity int,
    fiscal_year int,
    primary key (date, product_code, customer_code),
    foreign key (product_code) references product(product_code),
    foreign key (customer_code) references customer(customer_code)
);

-- Создание таблицы sales_domain
create table sales_domain (
    Date date,
    product_code varchar(255),
    customer_code int,
    sold_quantity int,
    fiscal_year int,
    division varchar(255),
    segment varchar(255),
    variant varchar(255),
    platform varchar(255),
    channel varchar(255),
    market varchar(255),
    sub_zone varchar(255),
    region varchar(255),
    gross_price numeric(10, 4),
    cost_year int,
    manufacturing_cost numeric(10, 4),
    pre_invoice_discount_pct numeric(10, 4),
    primary key (Date, product_code, customer_code, fiscal_year, cost_year),
    foreign key (product_code) references product(product_code),
    foreign key (customer_code) references customer(customer_code)
);
