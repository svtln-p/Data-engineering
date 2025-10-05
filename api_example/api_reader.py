import requests  
import pandas as pd  


API_URL = "https://www.affirmations.dev/"

def load_affirmations():

    
    affirmations = []
    
    for i in range(10):

        response = requests.get(API_URL)
        
        if response.status_code == 200:
            data = response.json()
            text = data['affirmation']
            
            affirmations.append({
                'id': i + 1,
                'text': text,
                'length': len(text),
            })
            print(f"Загрузка аффирмации {i+1}")
        else:
            print(f"Ошибка {i+1}")
    
    return affirmations

def save_data(affirmations):

    df = pd.DataFrame(affirmations)
    
    # Сохраняем в CSV
    df.to_csv('affirmations.csv', index=False)
    print("Файл affirmations.csv сохранен")
    
    # Сохраняем в текстовый файл
    with open('affirmations.txt', 'w', encoding='utf-8') as f:
        for a in affirmations:
            f.write(f"{a['id']}. {a['text']}\n")
    print("Файл affirmations.txt сохранен")
    
    return df

def main():
    
    # Загружаем данные
    data = load_affirmations()
 
    if data:
        result = save_data(data)
        

        print("\n Информация о данных:")
        print(result.info())
        

        print(f"\nЗагружено: {len(result)} аффирмаций")
        print("\n Примеры аффирмаций:")
        for i, row in result.head(10).iterrows():
            print(f"{row['id']}. {row['text']}")
    else:
        print("Не удалось загрузить данные")


if __name__ == "__main__":
    main()
