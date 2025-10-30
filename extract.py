import pandas as pd
from pathlib import Path


def read_data(file_url: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_url)
        Path("data/raw").mkdir(parents=True, exist_ok=True)
        df.to_csv("data/raw/bird_strikes_raw.csv", index=False)
        print(f"Данные загружены")
        print("\nПервые 10 строк датасета:")
        print(df.head(10))
        print("\nИнформация о данных:")
        print(df.info())
        return df
    except Exception as e:
        print(f"Ошибка")
        raise