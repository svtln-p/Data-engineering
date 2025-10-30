import pandas as pd

def transform_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Приведение типов данных"""
    df_converted = df.copy()
    # Преобразование дат
    if 'FlightDate' in df_converted.columns:
        df_converted['FlightDate'] = pd.to_datetime(df_converted['FlightDate'], errors='coerce')

    # Числовые значения
    cost_cols = ['Cost: Total $', 'Cost: Repair (inflation adj)', 'Cost: Other (inflation adj)']
    num_cols = [
        'Speed (IAS) in knots',
        'Feet above ground',
        'Miles from airport',
        'Aircraft: Number of engines?',
        'Cost: Aircraft time out of service (hours)'
    ]

    for col in cost_cols + num_cols:
        if col in df_converted.columns:
            df_converted[col] = pd.to_numeric(df_converted[col], errors='coerce')

    # Преобразование категориальных колонок
    cat_cols = [
        'Airport: Name',
        'Wildlife: Species',
        'When: Phase of flight',
        'Effect: Indicated Damage',
        'When: Time of day'
    ]
    for col in cat_cols:
        if col in df_converted.columns:
            df_converted[col] = df_converted[col].astype('category')

    # Преобразование булевых колонок
    if 'Pilot warned of birds or wildlife?' in df_converted.columns:
        df_converted['Pilot warned of birds or wildlife?'] = df_converted['Pilot warned of birds or wildlife?'].map({
            'Yes': True, 'No': False, 'Y': True, 'N': False, 'Unknown': False
        })

    print("Типы данных после преобразования:")
    print(df_converted.dtypes)
    return df_converted
