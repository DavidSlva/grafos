# Código en Python que utiliza CPLEX (docplex) para resolver el problema de replanificación de atraques
# Incluye un conjunto de datos más variado y funciones de ploteo mejoradas

from docplex.mp.model import Model
import matplotlib.pyplot as plt
import numpy as np

# ============================
# Datos de entrada mejorados
# ============================

# Conjuntos de buques y muelles
N = [i for i in range(1, 16)]  # Buques 1 a 15
M = [1, 2, 3, 4]

# Tiempos de llegada planificados (A_i) y reales (a_i)
A_i = {
    1: 1, 2: 2, 3: 3, 4: 4, 5: 5,
    6: 6, 7: 7, 8: 8, 9: 9, 10: 10,
    11: 11, 12: 12, 13: 13, 14: 14, 15: 15
}

# Tiempos de llegada reales (a_i) con variaciones respecto al plan
a_i = {
    1: 1, 2: 2, 3: 4, 4: 4, 5: 6,
    6: 5, 7: 8, 8: 9, 9: 9, 10: 11,
    11: 11, 12: 13, 13: 13, 14: 15, 15: 16
}

# Tiempos de salida planificados (e_i)
e_i = {}
for i in N:
    e_i[i] = A_i[i] + 3  # Asumimos tiempo de servicio planificado de 3 unidades

# Tiempos de manipulación estimados (h_ik)
h_ik = {}
for i in N:
    for k in M:
        h_ik[(i, k)] = np.random.choice([2.5, 3, 3.5, 4])  # Tiempos de manipulación variados

# Costos
c1 = 5    # Costo por cambio de muelle
c2 = 10   # Costo por retraso en salida
mu_i = {}
for i in N:
    mu_i[i] = np.random.randint(1, 6)  # Prioridades entre 1 y 5
c3 = 15   # Costo por retraso adicional en tiempo de servicio
B = 10000  # Constante grande

# Asignación planeada de buques a muelles (b_ik)
b_ik = {}
for i in N:
    for k in M:
        if k == ((i - 1) % len(M)) + 1:
            b_ik[(i, k)] = 1  # Asignar buques cíclicamente a los muelles
        else:
            b_ik[(i, k)] = 0

# Muelles factibles para cada buque (algunos buques no pueden usar ciertos muelles)
M_i = {}
for i in N:
    M_i[i] = M.copy()
    # Supongamos que algunos buques no pueden usar el muelle 4
    if i % 5 == 0:
        M_i[i].remove(4)

# Indisponibilidad de muelles
Indisponibilidad_k = {
    1: [(7, 10), (14, 16)],  # Muelle 1 no disponible de tiempo 7 a 10 y 14 a 16
    2: [(5, 6), (12, 13)],   # Muelle 2 no disponible de tiempo 5 a 6 y 12 a 13
    3: [(9, 11)],            # Muelle 3 no disponible de tiempo 9 a 11
    4: [(15, 17)],           # Muelle 4 no disponible de tiempo 15 a 17
}

# ============================
# Creación del modelo
# ============================

mdl = Model(name='Replanificacion_de_Atraques')

# Variables de decisión
m_prime = mdl.continuous_var_dict(N, name='m_prime')  # Tiempo de atraque actualizado
e_prime = mdl.continuous_var_dict(N, name='e_prime')  # Tiempo de salida actualizado
delta_e = mdl.continuous_var_dict(N, name='delta_e')  # Retraso en salida
w_prime = mdl.continuous_var_dict(N, name='w_prime')  # Retraso adicional en tiempo de servicio
b_prime = mdl.binary_var_matrix(N, M, name='b_prime') # Asignación de muelles
d_bik = mdl.continuous_var_matrix(N, M, name='d_bik') # Cambio de muelle

# Variables binarias para la no superposición temporal
z = mdl.binary_var_dict([(i, j) for i in N for j in N if i != j], name='z')

# Función objetivo (sin cambios)

# [El resto de la función objetivo permanece igual]

# Restricciones

# 1. Restricción de llegada dinámica
for i in N:
    mdl.add_constraint(m_prime[i] >= a_i[i])

# 2. Restricción de salida
for i in N:
    mdl.add_constraint(e_prime[i] == m_prime[i] + mdl.sum(h_ik[i, k] * b_prime[i, k] for k in M))

# 3. Cálculo del retraso en salida
for i in N:
    mdl.add_constraint(delta_e[i] >= e_prime[i] - e_i[i])
    mdl.add_constraint(delta_e[i] >= e_i[i] - e_prime[i])

# 4. Cálculo del retraso adicional en tiempo de servicio
for i in N:
    mdl.add_constraint(w_prime[i] >= (e_prime[i] - a_i[i]) - (e_i[i] - A_i[i]))
    mdl.add_constraint(w_prime[i] >= 0)

# 5. Asignación de muelles
for i in N:
    mdl.add_constraint(mdl.sum(b_prime[i, k] for k in M_i[i]) == 1)

# 6. Restricciones de no superposición temporal
for i in N:
    for j in N:
        if i != j:
            for k in M:
                mdl.add_constraint(m_prime[i] + mdl.sum(h_ik[i, k] * b_prime[i, k]) <= m_prime[j] + B * (1 - b_prime[i, k] * b_prime[j, k] + z[i, j]))
                mdl.add_constraint(m_prime[j] + mdl.sum(h_ik[j, k] * b_prime[j, k]) <= m_prime[i] + B * (2 - b_prime[i, k] * b_prime[j, k] - z[i, j]))

# 7. Cálculo de d_bik
for i in N:
    for k in M:
        mdl.add_constraint(d_bik[i, k] >= b_prime[i, k] - b_ik.get((i, k), 0))
        mdl.add_constraint(d_bik[i, k] >= b_ik.get((i, k), 0) - b_prime[i, k])

# 8. Restricciones de disponibilidad de muelles
for i in N:
    for k in M_i[i]:
        for (t_inicio, t_fin) in Indisponibilidad_k.get(k, []):
            mdl.add_constraint(m_prime[i] >= t_fin - B * (1 - b_prime[i, k]))
            mdl.add_constraint(e_prime[i] <= t_inicio + B * (1 - b_prime[i, k]))


# ============================
# Resolución del modelo
# ============================

solution = mdl.solve(log_output=True)

# ============================
# Presentación de resultados
# ============================

if solution:
    print("Solución óptima encontrada:")
    # Almacenaremos los datos para el ploteo
    schedule = []
    total_cost = Z.solution_value
    for i in N:
        m_i = m_prime[i].solution_value
        e_i_prime = e_prime[i].solution_value
        delta_e_i = delta_e[i].solution_value
        w_i = w_prime[i].solution_value
        assigned_berth = None
        for k in M:
            if b_prime[i, k].solution_value > 0.5:
                assigned_berth = k
                break  # Solo hay un muelle asignado
        print(f"Buque {i}:")
        print(f"  Tiempo de llegada real (a_i): {a_i[i]}")
        print(f"  Tiempo de atraque (m'_i): {m_i}")
        print(f"  Tiempo de salida planificado (e_i): {e_i[i]}")
        print(f"  Tiempo de salida (e'_i): {e_i_prime}")
        print(f"  Retraso en salida (delta_e_i): {delta_e_i}")
        print(f"  Retraso adicional en servicio (w_i): {w_i}")
        print(f"  Asignado al muelle: {assigned_berth}")
        print(f"  Prioridad: {mu_i[i]}")
        print()
        # Agregar datos al cronograma
        schedule.append({
            'Buque': i,
            'Muelle': assigned_berth,
            'Inicio': m_i,
            'Fin': e_i_prime,
            'Inicio Planificado': A_i[i],
            'Fin Planificado': e_i[i],
            'Llegada Real': a_i[i],
            'Retraso en Salida': delta_e_i,
            'Retraso Adicional': w_i,
            'Prioridad': mu_i[i],
            'Cambio de Muelle': int(b_ik.get((i, assigned_berth), 0) == 0)
        })
else:
    print("No se encontró una solución óptima.")

# ============================
# Generación de gráficos
# ============================

def plot_schedule(schedule):
    fig, ax = plt.subplots(figsize=(12, 8))

    colors = plt.cm.Set3.colors

    for task in schedule:
        berth = task['Muelle']
        color = colors[(berth - 1) % len(colors)]
        # Cronograma replanificado
        ax.barh(task['Buque'], task['Fin'] - task['Inicio'], left=task['Inicio'], color=color, edgecolor='black', label=f'Muelle {berth}' if f'Muelle {berth}' not in ax.get_legend_handles_labels()[1] else "")
        # Cronograma planificado (transparente)
        ax.barh(task['Buque'], task['Fin Planificado'] - task['Inicio Planificado'], left=task['Inicio Planificado'], color='none', edgecolor='red', linestyle='--', label='Planificado' if 'Planificado' not in ax.get_legend_handles_labels()[1] else "")
        # Línea de llegada real
        ax.plot([task['Llegada Real'], task['Llegada Real']], [task['Buque'] - 0.4, task['Buque'] + 0.4], color='blue', linestyle=':', label='Llegada Real' if 'Llegada Real' not in ax.get_legend_handles_labels()[1] else "")

    ax.set_xlabel('Tiempo')
    ax.set_ylabel('Buque')
    ax.set_title('Cronograma de Buques (Planificado vs. Replanificado)')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

def plot_delays(schedule):
    buques = [task['Buque'] for task in schedule]
    retrasos_salida = [task['Retraso en Salida'] for task in schedule]
    retrasos_adicionales = [task['Retraso Adicional'] for task in schedule]

    fig, ax = plt.subplots(figsize=(12, 6))
    width = 0.35
    x = np.arange(len(buques))  # Posición en el eje X

    ax.bar(x - width/2, retrasos_salida, width, label='Retraso en Salida')
    ax.bar(x + width/2, retrasos_adicionales, width, label='Retraso Adicional en Servicio')
    ax.set_xlabel('Buque')
    ax.set_ylabel('Tiempo')
    ax.set_title('Retrasos por Buque')
    ax.set_xticks(x)
    ax.set_xticklabels(buques)
    ax.legend()
    plt.tight_layout()
    plt.show()

def plot_costs(total_Z1, total_Z2, total_Z3):
    labels = ['Costo de Servicio (Z1)', 'Costo de Reasignación y Retrasos (Z2)', 'Costo de Retrasos Adicionales (Z3)']
    costs = [total_Z1, total_Z2, total_Z3]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(costs, labels=labels, autopct='%1.1f%%', startangle=140, wedgeprops={'edgecolor': 'black'})
    ax.set_title('Distribución de Costos Totales')
    plt.show()

def plot_priority_vs_delay(schedule):
    prioridades = [task['Prioridad'] for task in schedule]
    retrasos = [task['Retraso en Salida'] for task in schedule]
    buques = [task['Buque'] for task in schedule]

    fig, ax = plt.subplots(figsize=(8, 6))
    scatter = ax.scatter(prioridades, retrasos, c=retrasos, cmap='coolwarm', s=100, edgecolor='black')
    for i, txt in enumerate(buques):
        ax.annotate(txt, (prioridades[i], retrasos[i]), textcoords="offset points", xytext=(5,5))
    ax.set_xlabel('Prioridad del Buque')
    ax.set_ylabel('Retraso en Salida')
    ax.set_title('Prioridad vs. Retraso en Salida')
    cbar = plt.colorbar(scatter)
    cbar.set_label('Retraso en Salida')
    plt.tight_layout()
    plt.show()

def plot_berth_utilization(schedule):
    muelle_tiempos = {k: [] for k in M}
    for task in schedule:
        muelle = task['Muelle']
        muelle_tiempos[muelle].append((task['Inicio'], task['Fin']))

    fig, ax = plt.subplots(figsize=(12, 6))
    colors = plt.cm.Pastel1.colors

    for muelle in M:
        intervals = muelle_tiempos[muelle]
        for interval in intervals:
            ax.barh(f'Muelle {muelle}', interval[1] - interval[0], left=interval[0], color=colors[(muelle - 1) % len(colors)], edgecolor='black')

    ax.set_xlabel('Tiempo')
    ax.set_ylabel('Muelle')
    ax.set_title('Utilización de Muelles')
    plt.tight_layout()
    plt.show()

def plot_gantt_chart(schedule):
    fig, gnt = plt.subplots(figsize=(14, 8))

    # Colores para los buques
    colors = plt.cm.tab20.colors

    # Definir límites
    gnt.set_xlim(0, max(task['Fin'] for task in schedule) + 2)
    gnt.set_ylim(0, len(M) + 1)

    # Etiquetas de ejes
    gnt.set_xlabel('Tiempo')
    gnt.set_ylabel('Muelles')

    # Etiquetas de muelles
    gnt.set_yticks([i + 0.5 for i in range(1, len(M) + 1)])
    gnt.set_yticklabels([f'Muelle {i}' for i in M])

    # Grid
    gnt.grid(True)

    for task in schedule:
        muelle = task['Muelle']
        color = colors[(task['Buque'] - 1) % len(colors)]
        gnt.broken_barh([(task['Inicio'], task['Fin'] - task['Inicio'])], (muelle - 0.4, 0.8), facecolors=(color), edgecolor='black')
        gnt.text(task['Inicio'] + (task['Fin'] - task['Inicio']) / 2, muelle, f'Buque {task["Buque"]}', ha='center', va='center', color='black')

    plt.title('Diagrama de Gantt de Atraques')
    plt.tight_layout()
    plt.show()

# Llamar a las funciones para generar los gráficos mejorados
plot_schedule(schedule)
plot_delays(schedule)
plot_priority_vs_delay(schedule)
plot_berth_utilization(schedule)
plot_gantt_chart(schedule)
