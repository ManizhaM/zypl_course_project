import duckdb

# Функция для создания подключения к базе данных DuckDB
def connect_db(db_file):
    conn = duckdb.connect(database=db_file, read_only=False)
    return conn