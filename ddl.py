import duckdb
import pandas as pd

# Подключение к базе данны  х DuckDB
def connect_db(db_file):
    conn = duckdb.connect(database=db_file, read_only=False)
    return conn

# Создание таблиц и заполнение данными
def create_tables_and_insert_data(db_file):
    conn = connect_db(db_file)
    
    # Чтение SQL-скриптов для создания таблиц
    with open('queries/queries.sql', 'r', encoding='utf-8') as file:
        create_tables_sql = file.read()
    conn.execute(create_tables_sql)
    
    file_to_table_map = {
    'dim_customer': 'customer',
    'dim_product': 'product',
    'fact_gross_price': 'gross_price',
    'fact_manufacturing_cost': 'manufacturing_cost',
    'fact_pre_discount': 'pre_discount',
    'fact_sales_monthly': 'sales_monthly',
    'Sales_domain': 'sales_domain'
}

    # Загрузка данных в таблицы
    for file_name, table_name in file_to_table_map.items():
        if(file_name=='Sales_domain'):  
            df = pd.read_csv(f'source/{file_name}.csv', encoding='Windows-1252')
        else:
            df = pd.read_csv(f'source/{file_name}.csv', encoding='utf-8')
        df.to_sql(table_name, conn, if_exists='append', index=False)

    result = conn.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'").fetchall()

    # Вывод результатов
    for row in result:
        print(row[0])
        
    with open('queries/views.sql', 'r') as file:
        create_view = file.read()
        conn.execute(create_view)

    conn.close()

if __name__ == "__main__":
    create_tables_and_insert_data('my.db')
