from pulp import *
import time

print("ТРАНСПОРТНАЯ ЗАДАЧА - ВАРИАНТ 12")


demand = [20, 20, 40, 10, 30]  # потребности потребителей
supply = [20, 10, 20, 30, 10]  # запасы поставщиков 

# матрица тарифов
cost_matrix = [
    [1, 1, 3, 4, 5],  
    [2, 3, 4, 2, 6],  
    [1, 1, 4, 7, 8],  
    [5, 6, 3, 4, 7],  
    [4, 5, 7, 6, 4]   
]

print("Дано:")
print(f"Запасы поставщиков: {supply} (сумма = {sum(supply)})")
print(f"Потребности потребителей: {demand} (сумма = {sum(demand)})")

#сбалансированность
total_supply = sum(supply)
total_demand = sum(demand)

if total_supply != total_demand:
    print(f"\n Задача несбалансированная! Разница: {abs(total_supply - total_demand)}")
    if total_supply < total_demand: #нужен доп. поставщик
        supply.append(total_demand - total_supply)
        cost_matrix.append([0, 0, 0, 0, 0]) #добавление поставщика с запасом
        print("Добавлен фиктивный поставщик")
    else:
        demand.append(total_supply - total_demand)
        for row in cost_matrix:
            row.append(0)
        print("Добавлен фиктивный потребитель")

m = len(supply)
n = len(demand)

print(f"\nРазмерность задачи: {m} поставщиков × {n} потребителей")

#решение
print("Решение методом PULP")

start_time = time.time()

#создание переменных
variables = []
for i in range(m):
    for j in range(n):
        variables.append(LpVariable(f"x_{i+1}_{j+1}", lowBound=0))  #lowBound то, что перевозки положительные

#создание задачи
problem = LpProblem("Transport_Problem", LpMinimize)

#целевая функция
cost_coeffs = []
for i in range(m):
    for j in range(n):
        cost_coeffs.append(cost_matrix[i][j]) #из i в j ставится цена

problem += lpDot(cost_coeffs, variables), "Total_Cost" #вычисление скалярного произведения списков

#поставщики
for i in range(m):
    constraint_vars = variables[i*n : (i+1)*n] #выбирает блок переменных для поставщика i
     # первый индекс блока: первый индекс след. блока
    problem += lpSum(constraint_vars) == supply[i], f"Supply_{i+1}" #короче мы складываем все переменные x_1_1 и тд и присваиваем макс. запасам

#огр потребителей
for j in range(n):
    constraint_vars = [variables[i*n + j] for i in range(m)]
    problem += lpSum(constraint_vars) == demand[j], f"Demand_{j+1}"




problem.solve(PULP_CBC_CMD(msg=0)) #pulp сам выбирает подходящий алгоритм решения, CBC решатель для лин. прог, CMD-запуск как консольной прог.
#msg убираем подробный вывод
pulp_time = time.time() - start_time

# ВЫВОД РЕЗУЛЬТАТОВ
print("оптимальный план перевозок:")


total_cost = 0
for variable in problem.variables():
    if variable.varValue > 0.001: #если перевозка не нулевая
        #парсим имя переменной (формат: "x_1_2") на отдельные
        parts = variable.name.split('_')
        supplier = int(parts[1])  
        consumer = int(parts[2])  
        amount = variable.varValue
        cost = amount * cost_matrix[supplier-1][consumer-1] #кол-во на цену
        total_cost += cost
        print(f"поставщик{supplier} → потребитель{consumer}: {amount:.1f} ед. × {cost_matrix[supplier-1][consumer-1]} = {cost:.1f}")


print(f"минимальная стоимость: {total_cost:.1f}")
print(f"время выполнения: {pulp_time:.4f} сек")

