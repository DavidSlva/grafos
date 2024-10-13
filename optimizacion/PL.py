import pulp

# Se crea el problema de optimización
prob = pulp.LpProblem("Peoblema de opti", pulp.LpMaximize)

# Definir variables de restricción.
x1 = pulp.LpVariable("x1", lowBound=0, cat='Continuous')
x2 = pulp.LpVariable("x2", lowBound=0, cat='Continuous')

# Se define la función objetivo
prob += 3*x1 + 5*x2, "Función objetivo"

# Se definen las restricciones

prob += 2*x1 + 3*x2 <= 12, "Restricción 1"
prob += -x1 + 2*x2 <= 4, "Restricción 2"

# Se resuelve el problema

prob.solve()

# Mostrar el estado del solver. O sea, si encontró solución optima o no.
print(f"Status: {prob.status}")
print(f"Valor optimo x1: {x1.varValue}")
print(f"Valor optimo x2: {x2.varValue}")

print(f"Valor de la función objetivo: {prob.objective.value()}")