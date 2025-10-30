import pandas as pd
import os
from pathlib import Path
from sqlalchemy import create_engine, text, Column, String, Integer, inspect
from dotenv import load_dotenv

def save_to_parquet(df: pd.DataFrame, output_path: str):
    """Сохраняет в Parquet"""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=False)
    print(f"Данные сохранены в Parquet: {output_path}")

def load_to_db(output_path: str):
    """Загружает первые 50 строк в базу данных"""
    load_dotenv()
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_url = os.getenv('DB_URL')
    db_port = os.getenv('DB_PORT')
    db_name = "homeworks"
    table_name = "parfenova"

    df = pd.read_parquet(output_path)
    df = df.head(50)
    


    engine = create_engine(
    f"postgresql+psycopg2://{db_user}:{db_password}@{db_url}:{db_port}/{db_name}"
)
    with engine.connect() as conn:
        print("Успешное подключение")
    
    df.to_sql(
    name=table_name,
    con=engine,
    schema="public", 
    if_exists="replace",
    index=True
)
    print("Данные успешно записаны в базу")
    # Проверка
    with engine.begin() as conn:
        conn.execute(text('ALTER TABLE public.parfenova ADD PRIMARY KEY (index)'))
    
    inspector = inspect(engine)
    columns = inspector.get_columns("parfenova", schema="public")
    
    print("\nСтруктура таблицы:")
    print({col["name"]: col["type"] for col in columns})