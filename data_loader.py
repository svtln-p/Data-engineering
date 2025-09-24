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

# Даты
if 'FlightDate' in df.columns:
    df['FlightDate'] = pd.to_datetime(df['FlightDate'], errors='coerce')

# Числовые колонки (затраты, высота, скорость)
cost_cols = ['Cost: Total $', 'Cost: Repair (inflation adj)', 'Cost: Other (inflation adj)']
num_cols = ['Altitude bin', 'Speed (IAS) in knots', 'Feet above ground', 'Miles from airport']

for col in cost_cols + num_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Категориальные колонки
cat_cols = ['Airport: Name', 'Wildlife: Species', 'When: Phase of flight', 'Effect: Indicated Damage']
for col in cat_cols:
    if col in df.columns and df[col].nunique() < 50:
        df[col] = df[col].astype('category')

print("Типы преобразованы")

# Сохранение в CSV
df.to_csv('data/bird_strikes.csv', index=False)
print("Сохранен CSV")

# Результаты
print(f"Файлы сохранены в папку 'data/'")
print(f"Обработано {len(df)} записей")
