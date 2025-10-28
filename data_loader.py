import pandas as pd

FILE_ID = "13FZ-XuVwak49XF5225IGnt5QfMR6fVjo"
file_url = f"https://drive.google.com/uc?id={FILE_ID}"

def load_data(url):
    """Загружает данные с Google Drive"""
    raw_data = pd.read_csv(url)
    
    return raw_data

def convert_data_types(df):
    """Выполняет приведение типов"""
    df_converted = df.copy()
    
    # Преобразование дат
    if 'FlightDate' in df_converted.columns:
        df_converted['FlightDate'] = pd.to_datetime(df_converted['FlightDate'], errors='coerce')
        print(f"FlightDate → {df_converted['FlightDate'].dtype}")
    
    #Числовые значения
    cost_cols = ['Cost: Total $', 'Cost: Repair (inflation adj)', 'Cost: Other (inflation adj)']
    num_cols = ['Speed (IAS) in knots', 'Feet above ground', 'Miles from airport', 'Aircraft: Number of engines?', 'Cost: Aircraft time out of service (hours)']
    
    for col in cost_cols + num_cols:
        if col in df_converted.columns:
            df_converted[col] = pd.to_numeric(df_converted[col], errors='coerce')
            print(f"{col} → {df_converted[col].dtype}")


    # Преобразование категориальных колонок
    cat_cols = ['Airport: Name', 'Wildlife: Species', 'When: Phase of flight', 'Effect: Indicated Damage', 'When: Time of day']
    for col in cat_cols:
        if col in df_converted.columns:
            df_converted[col] = df_converted[col].astype('category')
            print(f" {col} → category")
            

    # Преобразование булевых колонок
    if 'Pilot warned of birds or wildlife?' in df_converted.columns:
        df_converted['Pilot warned of birds or wildlife?'] = df_converted['Pilot warned of birds or wildlife?'].map({
            'Yes': True, 'No': False, 'Y': True, 'N': False, 'Unknown': False
        })
        print(f" Pilot warned of birds or wildlife? → {df_converted['Pilot warned of birds or wildlife?'].dtype}")

    return df_converted

def save_data(df, output_dir='data'):
    """Сохраняет обработанные данные в CSV файл и в Parquet."""
    # CSV (основной формат)
    df.to_csv('data/bird_strikes.csv', index=False)
    print("Сохранен CSV")

    # Parquet (эффективный формат)
    df.to_parquet('data/bird_strikes.parquet', index=False)
    print("Сохранен Parquet")


def main():
    """Основная функция для выполнения процесса обработки данных."""
    # Загрузка данных
    raw_data = load_data(file_url)
    print("\nПервые 10 строк датасета:")
    print(raw_data.head(10))
    print("\nИнформация о данных:")
    print(raw_data.info())
    
    # Приведение типов данных
    df_processed = convert_data_types(raw_data)
    
    # Сохранение данных
    save_data(df_processed)
    
    # Вывод финальной информации
    print("\nТипы данных после преобразования:")
    print(df_processed.info())
    print(f"\nОбработано {len(df_processed)} записей")
    print(f"Файлы сохранены в папку 'data/'")

if __name__ == "__main__":
    main()
