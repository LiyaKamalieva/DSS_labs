import pandas as pd
import numpy as np


data = {
    'product': ['DARLING Wet Kiss', 'Clinique almost lipstick', 'MAC MACximal Matte Lipstick'],
    'price': [1100, 3800, 2990],          # мин
    'weight_gr': [2.8, 1.9, 3.5],         # макс
    'review_score': [4.7, 4.4, 4.8]       # макс
}

df = pd.DataFrame(data)

# шкала 0-1
df_norm = df.copy()

# чем меньше тем ближе к 1
df_norm['price_norm'] = (df['price'].max() - df['price']) / (df['price'].max() - df['price'].min())

df_norm['weight_norm'] = (df['weight_gr'] - df['weight_gr'].min()) / (df['weight_gr'].max() - df['weight_gr'].min())

df_norm['review_norm'] = (df['review_score'] - df['review_score'].min()) / (df['review_score'].max() - df['review_score'].min())

weights = { #расставляем приоритеты середи показателей
    'price_norm': 0.4,    
    'weight_norm': 0.3,   
    'review_norm': 0.3   
}

#умножаем значение (0-1) на приоритетное значение
df_norm['total_score'] = (df_norm['price_norm'] * weights['price_norm'] + 
                          df_norm['weight_norm'] * weights['weight_norm'] + 
                          df_norm['review_norm'] * weights['review_norm'])

print("Нормализованные данные и итоговые оценки:")
print(df_norm[['product', 'price_norm', 'weight_norm', 'review_norm', 'total_score']])

#находим лучший вариант
best_product = df_norm.loc[df_norm['total_score'].idxmax()]
print(f"\nЛучший вариант: {best_product['product']}")
print(f"С интегральной оценкой: {best_product['total_score']}")

result = df_norm[['product', 'total_score']].sort_values('total_score', ascending=False)
print("\nРейтинг помад от лучшей к худшей:")
print(result)