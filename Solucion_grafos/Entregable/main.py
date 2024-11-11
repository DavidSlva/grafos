# Código en Python que utiliza CPLEX (docplex) para resolver el problema de replanificación de atraques
# Adaptado para incluir funciones de ploteo y visualizar el cronograma y otros gráficos

from docplex.mp.model import Model
import ast
import matplotlib.pyplot as plt
import numpy as np
import sys

# ============================
# Lectura de datos desde archivo .txt
# ============================

def leer_datos_desde_txt(ruta_archivo):
    with open(ruta_archivo, 'r') as f:
        lines = f.readlines()

    datos = {}
    buffer = ""
    key = None

    for line in lines:
        line = line.strip()
        if line == '' or line.startswith('#'):
            continue  # Ignorar líneas vacías o comentarios

        # Si estamos acumulando para una entrada multilineal
        if buffer:
            buffer += " " + line
            if line.endswith('}'):
                # Evaluar el buffer acumulado y limpiar para la siguiente entrada
                try:
                    datos[key] = ast.literal_eval(buffer)
                except Exception as e:
                    print(f"Error evaluando {key} con valor {buffer}")
                    print(e)
                    break
                buffer = ""
                key = None
            continue

        # Nueva entrada
        try:
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            if value.startswith('{'):
                buffer = value  # Inicia acumulación para una estructura multilineal
            else:
                datos[key] = ast.literal_eval(value)
        except Exception as e:
            print(f"Error en la línea: {line}")
            print(e)
            break

    return datos

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python script.py <ruta_archivo_datos>")
        sys.exit(1)

    ruta_datos = sys.argv[1]
    datos = leer_datos_desde_txt(ruta_datos)



# ============================
# Definición de conjuntos y parámetros a partir de los datos leídos
# ============================

# Conjuntos de buques y sitios de atraque
N = datos['N']  # Lista de buques
M = datos['M']  # Lista de sitios de atraque

# Parámetros del modelo
a_i = datos['a_i']         # Tiempo de llegada de cada buque i
A_i = datos['A_i']         # Tiempo de llegada planificado de cada buque i
e_i = datos['e_i']         # Tiempo de salida planificado de cada buque i
H_ik = datos['H_ik']       # Tiempo mínimo de manipulación de buque i en sitio k
h_ik = datos['h_ik']       # Tiempo estimado de manipulación de buque i en sitio k
L_i = datos['L_i']         # Longitud de cada buque i
g_k = datos['g_k']         # Posición del sitio de atraque k
c1 = datos['c1']           # Costo por cambio de posición de atraque
c2 = datos['c2']           # Costo por retraso en salida respecto al cronograma base
c3 = datos['c3']           # Costo de retraso adicional
mu_i = datos['mu_i']       # Prioridad asignada a cada buque i
b_ik = datos['b_ik']       # Posición planeada de atraque para buque i en el cronograma base
M_i = datos['M_i']         # Conjunto de sitios de atraque factibles para buque i
B = datos['B']             # Constante grande

# ============================
# Creación del modelo
# ============================

mdl = Model(name='Replanificación_de_Atraques')

# ============================
# Definición de variables de decisión
# ============================

# Variables de tiempo y posición de atraque
m_prime = mdl.continuous_var_dict(N, name='m_prime')    # Tiempo de atraque actualizado
e_prime = mdl.continuous_var_dict(N, name='e_prime')    # Tiempo de salida actualizado
w_prime = mdl.continuous_var_dict(N, name='w_prime')    # Diferencia en tiempo de servicio

# Variables binarias para ubicación y precedencia
b_prime = mdl.binary_var_matrix(N, M, name='b_prime')   # Asignación de buques a sitios de atraque
delta_e = mdl.continuous_var_dict(N, name='delta_e')    # Variable auxiliar para valor absoluto de (e'_i - e_i)
d_bik = mdl.continuous_var_matrix(N, M, name='d_bik')   # Variable auxiliar para |b'_{ik} - b_{ik}|

# Variables binarias para orden y posición
pairs_ij = [(i, j) for i in N for j in N if i != j]
z = mdl.binary_var_dict(pairs_ij, name='z')             # Indica si e'_i <= m'_j (i sale antes de que j entre)

# Variables binarias para indicar si dos buques están en el mismo sitio
s = mdl.binary_var_dict(pairs_ij, name='s')             # Indica si i y j están asignados al mismo sitio

# ============================
# Definición de la función objetivo
# ============================

# Costo de servicio de los buques (Z1)
Z1 = mdl.sum(e_prime[i] - a_i[i] for i in N)

# Agregar restricciones para delta_e_i (valor absoluto de e'_i - e_i)
for i in N:
    mdl.add_constraint(delta_e[i] >= e_prime[i] - e_i[i])
    mdl.add_constraint(delta_e[i] >= e_i[i] - e_prime[i])

# Agregar restricciones para d_bik (valor absoluto de b'_{ik} - b_{ik})
for i in N:
    for k in M:
        mdl.add_constraint(d_bik[i, k] >= b_prime[i, k] - b_ik.get((i, k), 0))
        mdl.add_constraint(d_bik[i, k] >= b_ik.get((i, k), 0) - b_prime[i, k])

# Costo de reasignación (Z2)
Z2 = mdl.sum(
    c1 * mdl.sum(d_bik[i, k] for k in M) +
    c2 * mu_i[i] * delta_e[i]
    for i in N
)

# Costo de retraso adicional para buques a tiempo (Z3)
Z3 = mdl.sum(c3 * w_prime[i] for i in N)

# Función objetivo total
mdl.minimize(Z1 + Z2 + Z3)

# ============================
# Definición de restricciones
# ============================

# 1. Restricción de llegada dinámica
for i in N:
    mdl.add_constraint(m_prime[i] - a_i[i] >= 0)

# 2. Restricción de salida
for i in N:
    mdl.add_constraint(e_prime[i] == m_prime[i] + mdl.sum(h_ik[(i, k)] * b_prime[i, k] for k in M))

# 3. Restricciones de diferencia de tiempo de servicio
for i in N:
    mdl.add_constraint(w_prime[i] >= (e_prime[i] - a_i[i]) - (e_i[i] - A_i[i]))
    mdl.add_constraint(w_prime[i] >= 0)  # Asegurar que w'_i sea no negativa

# 4. Restricciones para s_{ij} (indica si i y j están en el mismo sitio)
for (i, j) in pairs_ij:
    for k in M:
        mdl.add_constraint(s[i, j] >= b_prime[i, k] + b_prime[j, k] - 1)

# 5. Restricciones de no superposición temporal para buques en el mismo sitio
for (i, j) in pairs_ij:
    # Solo aplicamos la restricción si s_{ij} = 1 (mismo sitio)
    # Aseguramos que e'_i <= m'_j o e'_j <= m'_i
    mdl.add_constraint(m_prime[j] >= e_prime[i] - B * (1 - z[i, j] + (1 - s[i, j])))
    mdl.add_constraint(m_prime[i] >= e_prime[j] - B * (z[i, j] + (1 - s[i, j])))

# 6. Restricciones de factibilidad de sitio de atraque
for i in N:
    mdl.add_constraint(mdl.sum(b_prime[i, k] for k in M_i[i]) == 1)

# ============================
# Resolución del modelo
# ============================

solution = mdl.solve(log_output=True)

# ============================
# Presentación de resultados
# ============================

if solution:
    print("Solución óptima encontrada:")
    schedule = []
    total_Z1 = Z1.solution_value
    total_Z2 = Z2.solution_value
    total_Z3 = Z3.solution_value
    for i in N:
        m_i = m_prime[i].solution_value
        e_i_prime = e_prime[i].solution_value
        w_i = w_prime[i].solution_value
        delta_e_i = delta_e[i].solution_value
        assigned_berth = None
        for k in M:
            if b_prime[i, k].solution_value > 0.5:
                assigned_berth = k
                break  # Solo hay un sitio asignado
        print(f"Buque {i}:")
        print(f"  Tiempo de atraque (m'_i): {m_i}")
        print(f"  Tiempo de salida (e'_i): {e_i_prime}")
        print(f"  Diferencia en tiempo de servicio (w'_i): {w_i}")
        print(f"  Retraso en salida (delta_e_i): {delta_e_i}")
        print(f"  Asignado al sitio de atraque: {assigned_berth}")
        print()
        # Agregar datos al cronograma
        schedule.append({
            'Buque': i,
            'Sitio': assigned_berth,
            'Inicio': m_i,
            'Fin': e_i_prime,
            'Inicio Planificado': A_i[i],
            'Fin Planificado': e_i[i],
            'Retraso': delta_e_i,
            'w_i': w_i,
            'Prioridad': mu_i[i],
            'Cambio de Sitio': int(b_ik.get((i, assigned_berth), 0) == 0)
        })
else:
    print("No se encontró una solución óptima.")

# ============================
# Generación de gráficos
# ============================

def plot_schedule(schedule):
    fig, ax = plt.subplots(figsize=(14, 8))

    # Colores para diferenciar los sitios de atraque
    colors = plt.cm.Paired.colors

    for task in schedule:
        berth = task['Sitio']
        color = colors[(berth - 1) % len(colors)]
        # Cronograma replanificado
        ax.barh(task['Buque'], task['Fin'] - task['Inicio'], left=task['Inicio'], color=color, edgecolor='black', label=f'Sitio {berth}' if f'Sitio {berth}' not in ax.get_legend_handles_labels()[1] else "")
        # Cronograma planificado (transparente)
        ax.barh(task['Buque'], task['Fin Planificado'] - task['Inicio Planificado'], left=task['Inicio Planificado'], color='none', edgecolor='red', linestyle='--', label='Planificado' if 'Planificado' not in ax.get_legend_handles_labels()[1] else "")

    ax.set_xlabel('Tiempo')
    ax.set_ylabel('Buque')
    ax.set_title('Cronograma de Buques (Planificado vs. Replanificado)')
    ax.legend()
    plt.tight_layout()
    plt.show()

def plot_delays(schedule):
    buques = [task['Buque'] for task in schedule]
    retrasos = [task['Retraso'] for task in schedule]
    w_i_values = [task['w_i'] for task in schedule]

    fig, ax = plt.subplots(figsize=(12, 6))
    width = 0.4
    x = np.arange(len(buques))  # Posición en el eje X

    ax.bar(x - width/2, retrasos, width, label='Retraso en salida (delta_e_i)')
    ax.bar(x + width/2, w_i_values, width, label='Retraso adicional (w_i)')
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

def plot_berth_assignments(schedule):
    buques = [task['Buque'] for task in schedule]
    sitios = [task['Sitio'] for task in schedule]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.scatter(buques, sitios, c=sitios, cmap='viridis', s=100, edgecolor='black')
    ax.set_xlabel('Buque')
    ax.set_ylabel('Sitio de Atraque')
    ax.set_title('Asignación de Buques a Sitios de Atraque')
    plt.colorbar(ax.collections[0], label='Sitio de Atraque')
    plt.tight_layout()
    plt.show()

def plot_priority_vs_delay(schedule):
    prioridades = [task['Prioridad'] for task in schedule]
    retrasos = [task['Retraso'] for task in schedule]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(prioridades, retrasos, c='blue', s=100, alpha=0.6, edgecolor='black')
    for i, txt in enumerate([task['Buque'] for task in schedule]):
        ax.annotate(txt, (prioridades[i], retrasos[i]), textcoords="offset points", xytext=(5,-5))
    ax.set_xlabel('Prioridad del Buque')
    ax.set_ylabel('Retraso en salida (delta_e_i)')
    ax.set_title('Prioridad vs. Retraso en Salida')
    plt.tight_layout()
    plt.show()

def plot_site_changes_pie(schedule):
    cambios = [task['Cambio de Sitio'] for task in schedule]
    cambios_si = sum(cambios)  # Número de buques que cambiaron de sitio
    cambios_no = len(cambios) - cambios_si  # Número de buques que no cambiaron de sitio

    # Datos para el gráfico de pastel
    labels = ['Cambio de Sitio (Sí)', 'Cambio de Sitio (No)']
    sizes = [cambios_si, cambios_no]
    colors = ['#4CAF50', '#FF5722']
    explode = (0.1, 0) 

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, explode=explode, wedgeprops={'edgecolor': 'black'})
    ax.set_title('Proporción de Cambios de Sitio de Atraque')
    plt.show()


def plot_manipulation_times(H_ik, h_ik, N, M):
    fig, ax = plt.subplots(figsize=(14, 8))
    H_values = []
    h_values = []
    labels = []

    for i in N:
        for k in M:
            key = (i, k)
            if key in H_ik:
                H_values.append(H_ik[key])
                h_values.append(h_ik[key])
                labels.append(f"B{i}-S{k}")
            else:
                # Si no hay datos para esta combinación, podemos ignorarla o agregar ceros
                # En este caso, la ignoramos
                pass

    indices = np.arange(len(H_values))
    bar_width = 0.35

    ax.bar(indices - bar_width/2, H_values, bar_width, label='H_ik (Mínimo)')
    ax.bar(indices + bar_width/2, h_values, bar_width, label='h_ik (Estimado)')

    ax.set_xlabel('Buque y Sitio')
    ax.set_ylabel('Tiempo de Manipulación')
    ax.set_title('Comparación de Tiempos de Manipulación por Buque y Sitio')
    ax.set_xticks(indices)
    ax.set_xticklabels(labels, rotation=90)
    ax.legend()
    plt.tight_layout()
    plt.show()


def plot_berth_utilization(schedule):
    fig, ax = plt.subplots(figsize=(14, 8))

    # Colores para los buques
    colors = plt.cm.tab20.colors

    sitios = sorted(set([task['Sitio'] for task in schedule]))
    sitio_labels = [f'Sitio {s}' for s in sitios]
    ax.set_yticks(sitios)
    ax.set_yticklabels(sitio_labels)

    for task in schedule:
        sitio = task['Sitio']
        color = colors[(task['Buque'] - 1) % len(colors)]
        ax.barh(sitio, task['Fin'] - task['Inicio'], left=task['Inicio'], color=color, edgecolor='black')
        ax.text(task['Inicio'] + (task['Fin'] - task['Inicio']) / 2, sitio, f'Buque {task["Buque"]}',
                ha='center', va='center', color='black', fontsize=9)

    ax.set_xlabel('Tiempo')
    ax.set_ylabel('Sitio de Atraque')
    ax.set_title('Utilización de Sitios de Atraque')
    ax.grid(True)
    plt.tight_layout()
    plt.show()

def plot_total_times_in_port(schedule):
    buques = [task['Buque'] for task in schedule]
    tiempos_totales = [task['Fin'] - a_i[task['Buque']] for task in schedule]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(buques, tiempos_totales, color='skyblue', edgecolor='black')
    ax.set_xlabel('Buque')
    ax.set_ylabel('Tiempo Total en Puerto')
    ax.set_title('Tiempo Total en Puerto por Buque')
    ax.set_xticks(buques)
    plt.tight_layout()
    plt.show()

def plot_departure_time_differences(schedule):
    buques = [task['Buque'] for task in schedule]
    salida_planificada = [task['Fin Planificado'] for task in schedule]
    salida_replanificada = [task['Fin'] for task in schedule]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(buques, salida_planificada, marker='o', label='Salida Planificada')
    ax.plot(buques, salida_replanificada, marker='s', label='Salida Replanificada')
    ax.set_xlabel('Buque')
    ax.set_ylabel('Tiempo de Salida')
    ax.set_title('Comparación de Tiempos de Salida Planificados y Replanificados')
    ax.set_xticks(buques)
    ax.legend()
    plt.tight_layout()
    plt.show()

# Llamar a las funciones para generar los gráficos
plot_schedule(schedule)
plot_delays(schedule)
plot_costs(total_Z1, total_Z2, total_Z3)
plot_berth_assignments(schedule)
plot_priority_vs_delay(schedule)
plot_site_changes_pie(schedule)
plot_manipulation_times(H_ik, h_ik, N, M)
plot_berth_utilization(schedule)
plot_total_times_in_port(schedule)
plot_departure_time_differences(schedule)
