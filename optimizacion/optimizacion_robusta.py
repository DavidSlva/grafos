# Importar Pyomo
from pyomo.environ import *
from pyomo.core import *

# Crear el modelo
model = ConcreteModel()

# Definir las variables de decisión (x1 y x2)
model.x1 = Var(bounds=(0, None))  # x1 >= 0
model.x2 = Var(bounds=(0, None))  # x2 >= 0

# Definir la función objetivo
model.obj = Objective(expr=2 * model.x1 + 3 * model.x2, sense=maximize)

# Conjuntos de incertidumbre (rangos para los coeficientes)
a1_range = [0.9, 1.1]
a2_range = [2.8, 3.0]
b1_range = [3.0, 3.2]
b2_range = [3.9, 4.1]

# Definir las restricciones con los valores más conservadores (valores "peores" para cada coeficiente)
# Restricción 1 robusta
model.con1 = Constraint(expr=(a1_range[1] * model.x1 + a2_range[1] * model.x2 <= 4))
# Restricción 2 robusta
model.con2 = Constraint(expr=(b1_range[1] * model.x1 + b2_range[1] * model.x2 <= 6))

# Crear un solver (usamos GLPK)
solver = SolverFactory('cbc')

# Resolver el problema
solver.solve(model)

# Mostrar los resultados
print("Valor óptimo de x1:", model.x1())
print("Valor óptimo de x2:", model.x2())
print("Valor óptimo de la función objetivo:", model.obj())
