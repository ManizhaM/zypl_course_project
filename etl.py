import pandas as pd
import duckdb
from connector import connect_db

# Функция для извлечения данных из базы данных
def extract_data(query, db_file):
    conn = connect_db(db_file)
    df = conn.execute(query).df()
    conn.close()
    return df

# загрузка данных
def load_data():
    query = 'select * from sales_summary'
    df = extract_data(query, 'my.db')
    return df


def load_data2():
    query = 'select * from sales_revenue_summary'
    df = extract_data(query, 'my.db')
    return df

def load_data3():
    query = 'select * from channel_market_revenue'
    df = extract_data(query, 'my.db')
    return df

def load_data4():
    query = 'select * from monthly_sales_summary'
    df = extract_data(query, 'my.db')
    return df

def load_data5():
    query = 'select * from product_sales_summary'
    df = extract_data(query, 'my.db')
    return df

def load_data6():
    query = 'select * from yearly_product_gross_price'
    df = extract_data(query, 'my.db')
    return df

if __name__ == "__main__":
    df = load_data6()
    print(df.head())
