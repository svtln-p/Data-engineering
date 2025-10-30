import argparse
from etl.extract import read_data
from etl.transform import transform_data_types
from etl.load import save_to_parquet, load_to_db


def etl_process(file_url: str):
    """Основной ETL-процесс."""
    print("Запуск ETL")

    # Извлечение
    df_raw = read_data(file_url)

    # Преобразование
    df_transformed = transform_data_types(df_raw)

    # Загрузка
    output_path = "data/processed/bird_strikes.parquet"
    save_to_parquet(df_transformed, output_path)       # Сохраняем обработанные данные
    load_to_db(output_path)  # Загружаем первые 50 строк в БД

    print("ETL процесс завершён успешно!")


if __name__ == "__main__":
    # CLI-интерфейс
    parser = argparse.ArgumentParser(
        description="ETL pipeline для обработки данных о столкновениях с птицами"
    )
    parser.add_argument(
        "--url",
        required=True,
        help="Ссылка на CSV-файл в Google Drive"
    )
    args = parser.parse_args()

    etl_process(args.url)