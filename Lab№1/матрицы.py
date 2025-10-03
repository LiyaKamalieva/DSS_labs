import numpy as np

# === КОД ИЗ ЛЕКЦИИ (почти дословно) ===

# 1. Поиск седловой точки (как в лекции)
print("1. Находим седло:")
matrix = np.array([
    [1, 5, 11, 12, 6],
    [2, 7, 12, 4, 6],
    [5, 11, 4, 0, 3],
    [3, 6, 4, 4, 7],
    [9, 9, 0, 8, 9]
])

lower_price = max([min(x) for x in matrix])
upper_price = min([max(x) for x in np.rot90(matrix)]) #поворот марицы стори и столбцы меняются местами

print(f"Нижняя цена игры (α): {lower_price}")
print(f"Верхняя цена игры (β): {upper_price}")

if lower_price == upper_price:
    print("седловая точка есть", f"ответ v={lower_price}")
else:
    print("седловой точки нет")
    print()

print("2. Расчет выигрышей:")
    
p = [0.0, 0.47, 0.0, 0.0, 0.53] #подпидывание кубика A
q = [0.63, 0.0, 0.37, 0.0, 0.0]

buff = 0 #подсчет общего выигрыша
for i, pin in zip(matrix, p): #вероятность выбора этой стратегии (из p) zip же объединяет p и a1 a2 и тд
    buff += pin * sum([x * y for x, y in zip(i, q)]) #x*y мат ожидание p(0,47)*sum(A2*q)
answer = {}
answer["H(P,Q)"] = buff

for k, i in enumerate(np.rot90(matrix), 1):
    answer["H(P,B{})".format(k)] = sum([x * y for x, y in zip(i, p)]) #k - номер стратегии b 



for situation, win in answer.items():
    print(f"Ответ выигрыш игрока A в ситуации {situation} = {win}")


print("\n3. АКТИВНЫЕ СТРАТЕГИИ:")
active_A = [f"A{i+1}" for i in range(len(p)) if p[i] > 0.001] #смотрим на p, берем вероятность и сравниваем
active_B = [f"B{i+1}" for i in range(len(q)) if q[i] > 0.001]
print(f"Активные стратегии A: {active_A}")
print(f"Активные стратегии B: {active_B}")

print("\n4. ИТОГ:")
print(f"Цена игры: {answer['H(P,Q)']}")
print(f"P = {p}")
print(f"Q = {q}")