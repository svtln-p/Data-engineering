import pandas as pd

FILE_ID = "13FZ-XuVwak49XF5225IGnt5QfMR6fVjo" # ID файла на Google Drive
file_url = f"https://drive.google.com/uc?id={FILE_ID}"


# Читаем CSV-файл с Google Диска
raw_data = pd.read_csv(file_url)
print("\nПервые 10 строк датасета:")
print(raw_data.head(10))

print("\n Информация о данных:")
print(raw_data.info())

# Копируем данные
df = raw_data.copy()

# 1. Даты
if 'FlightDate' in df.columns:
    df['FlightDate'] = pd.to_datetime(df['FlightDate'], errors='coerce')
    print(f"FlightDate → {df['FlightDate'].dtype}")

# 2. Числовые значения
cost_cols = ['Cost: Total $', 'Cost: Repair (inflation adj)', 'Cost: Other (inflation adj)']
num_cols = ['Speed (IAS) in knots', 'Feet above ground', 'Miles from airport']

for col in cost_cols + num_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        print(f"{col} → {df[col].dtype}")

# 3. Категориальные
cat_cols = ['Airport: Name', 'Wildlife: Species', 'When: Phase of flight', 'Effect: Indicated Damage']
for col in cat_cols:
    if col in df.columns:
        if df[col].nunique() < 50:
            df[col] = df[col].astype('category')
            print(f" {col} → category ({df[col].nunique()} уникальных)")
        else:
            print(f" {col} → object (сохранен, {df[col].nunique()} уникальных)")


# Количество двигателей - преобразуем в число
if 'Aircraft: Number of engines?' in df.columns:
    df['Aircraft: Number of engines?'] = pd.to_numeric(df['Aircraft: Number of engines?'], errors='coerce')
    print(f" Aircraft: Number of engines? → {df['Aircraft: Number of engines?'].dtype}")

# Время суток - категория
if 'When: Time of day' in df.columns and df['When: Time of day'].nunique() < 10:
    df['When: Time of day'] = df['When: Time of day'].astype('category')
    print(f" When: Time of day → category")

# Предупреждение пилота - булево значение
if 'Pilot warned of birds or wildlife?' in df.columns:
    df['Pilot warned of birds or wildlife?'] = df['Pilot warned of birds or wildlife?'].map({
        'Yes': True, 'No': False, 'Y': True, 'N': False, 'Unknown': False
    })
    print(f" Pilot warned of birds or wildlife? → {df['Pilot warned of birds or wildlife?'].dtype}")

# Часы простоя самолета - число
if 'Cost: Aircraft time out of service (hours)' in df.columns:
    df['Cost: Aircraft time out of service (hours)'] = pd.to_numeric(
        df['Cost: Aircraft time out of service (hours)'], errors='coerce'
    )
    print(f" Cost: Aircraft time out of service (hours) → {df['Cost: Aircraft time out of service (hours)'].dtype}")



# Вывод финальных типов
print("\n Типы данных после преобразования:")
print(df.info())
#print(df.dtypes)

#print("\n Распредление типов данных:")
#print(df.dtypes.value_counts())

# Сохранение в CSV
df.to_csv('data/bird_strikes.csv', index=False)
print("\n Сохранен CSV")

# Результаты

print(f"Файлы сохранены в папку 'data/'")
print(f"Обработано {len(df)} записей")


