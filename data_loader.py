import pandas as pd

FILE_ID = "13FZ-XuVwak49XF5225IGnt5QfMR6fVjo" # ID файла на Google Drive
file_url = f"https://drive.google.com/uc?id={FILE_ID}"


# Читаем CSV-файл с Google Диска
raw_data = pd.read_csv(file_url)
print("\nПервые 10 строк датасета:")
print(raw_data.head(10))

