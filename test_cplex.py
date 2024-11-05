from docplex.mp.model import Model
from docplex.mp.context import Context

ctx = Context()
ctx.solver.cplex_path = "C:\\Program Files\\IBM\\ILOG\\CPLEX_Studio_Community2211\\cplex\\bin\\x64_win64\\cplex.exe"

mdl = Model(name="simple_test", context=ctx)
x = mdl.binary_var(name="x")
mdl.maximize(x)

solution = mdl.solve(log_output=True)

if solution:
    print("Solución encontrada:", x.solution_value)
else:
    print("No se encontró solución.")
