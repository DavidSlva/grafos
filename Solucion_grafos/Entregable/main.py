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
        print("Uso: python main.py <ruta_archivo_datos>")
        sys.exit(1)

    ruta_datos = sys.argv[1]
    datos = leer_datos_desde_txt(ruta_datos)

    # ============================
    # Definición de conjuntos y parámetros a partir de los datos leídos
    # ============================
    N = datos['N'] 
    M = datos['M'] 
    a_i = datos['a_i']
    A_i = datos['A_i']
    e_i = datos['e_i']
    h_ik = datos['h_ik']
    c1, c2, c3 = datos['c1'], datos['c2'], datos['c3']
    mu_i = datos['mu_i']
    b_ik = datos['b_ik']
    M_i = datos['M_i']
    B = datos['B']

    # ============================
    # CONSTANTE (diccionario) de ventanas de bloqueo
    # ============================
    # Cada llave es (buque, muelle), con una lista de intervalos (T_start, T_end)
    ventanas_bloqueo = {
        (1,1): [(0, 100)],  # Bloquear [0..100] a buque 1 en muelle 1
        (1,2): [(0, 100)],
        (1,3): [(7,11)],
        (2,1): [],
        (2,2): [],
        (2,3): [],
        (3,1): [],
        (3,2): [],
        (3,3): [],
        (4,1): [],
        (4,2): [],
        (4,3): [],
        (5,1): [],
        (5,2): [],
        (5,3): [],
        (6,1): [],
        (6,2): [],
        (6,3): []
    }

    # ============================
    # Creación del modelo
    # ============================
    mdl = Model(name='Replanificación_de_Atraques')

    # ============================
    # Definición de variables
    # ============================
    m_prime = mdl.continuous_var_dict(N, name='m_prime')
    e_prime = mdl.continuous_var_dict(N, name='e_prime')
    w_prime = mdl.continuous_var_dict(N, name='w_prime')
    b_prime = mdl.binary_var_matrix(N, M, name='b_prime')
    delta_e = mdl.continuous_var_dict(N, name='delta_e')
    d_bik   = mdl.continuous_var_matrix(N, M, name='d_bik')

    pairs_ij = [(i, j) for i in N for j in N if i != j]
    z = mdl.binary_var_dict(pairs_ij, name='z')
    s = mdl.binary_var_dict(pairs_ij, name='s')

    # ============================
    # Función objetivo
    # ============================
    Z1 = mdl.sum(e_prime[i] - a_i[i] for i in N)

    # Restricción para |e'_i - e_i|
    for i in N:
        mdl.add_constraint(delta_e[i] >= e_prime[i] - e_i[i], ctname=f"abs_del_pos_{i}")
        mdl.add_constraint(delta_e[i] >= e_i[i] - e_prime[i], ctname=f"abs_del_neg_{i}")

    # Restricción para |b'_{i,k} - b_{ik}|
    for i in N:
        for k in M:
            mdl.add_constraint(d_bik[i, k] >= b_prime[i, k] - b_ik.get((i, k), 0),
                               ctname=f"abs_bik_pos_{i}_{k}")
            mdl.add_constraint(d_bik[i, k] >= b_ik.get((i, k), 0) - b_prime[i, k],
                               ctname=f"abs_bik_neg_{i}_{k}")

    Z2 = mdl.sum(
        c1 * mdl.sum(d_bik[i, k] for k in M) +
        c2 * mu_i[i] * delta_e[i]
        for i in N
    )
    Z3 = mdl.sum(c3 * w_prime[i] for i in N)
    mdl.minimize(Z1 + Z2 + Z3)

    # ============================
    # Restricciones base
    # ============================
    # 1. Llegada
    for i in N:
        mdl.add_constraint(m_prime[i] >= a_i[i], ctname=f"llegada_{i}")

    # 2. Salida
    for i in N:
        mdl.add_constraint(
            e_prime[i] == m_prime[i] + mdl.sum(h_ik[(i, k)] * b_prime[i, k] for k in M),
            ctname=f"salida_{i}"
        )

    # 3. w_prime
    for i in N:
        mdl.add_constraint(w_prime[i] >= (e_prime[i] - a_i[i]) - (e_i[i] - A_i[i]),
                           ctname=f"wprime_pos_{i}")
        mdl.add_constraint(w_prime[i] >= 0, ctname=f"wprime_nonneg_{i}")

    # 4. s_{ij}
    for (i, j) in pairs_ij:
        for k in M:
            mdl.add_constraint(s[i, j] >= b_prime[i, k] + b_prime[j, k] - 1,
                               ctname=f"s_{i}_{j}_{k}")

    # 5. No superposición temporal
    for (i, j) in pairs_ij:
        mdl.add_constraint(m_prime[j] >= e_prime[i] - B*(1 - z[i, j] + 1 - s[i, j]),
                           ctname=f"noover1_{i}_{j}")
        mdl.add_constraint(m_prime[i] >= e_prime[j] - B*(z[i, j] + 1 - s[i, j]),
                           ctname=f"noover2_{i}_{j}")

    # 6. Factibilidad de muelle
    for i in N:
        mdl.add_constraint(mdl.sum(b_prime[i, k] for k in M_i[i]) == 1, ctname=f"fact_{i}")

    # ============================
    # Restricciones de ventanas de bloqueo (Corregidas)
    # ============================
    # Se fuerza u_block[i,k,idx] == b_prime[i,k] con dos inequalities (>= y <=).
    bigM = 10000  # o B=1000, algo suficientemente grande

    u_block = {}
    v_block = {}

    for (i, k), lista_ventanas in ventanas_bloqueo.items():
        for idx, (t_init, t_end) in enumerate(lista_ventanas):
            u_name = f"u_block_{i}_{k}_{idx}"
            v_name = f"v_block_{i}_{k}_{idx}"
            u_block[i, k, idx] = mdl.binary_var(name=u_name)
            v_block[i, k, idx] = mdl.binary_var(name=v_name)

            # (1) e'_i <= t_init + bigM*(1 - u_{i,k,idx})
            mdl.add_constraint(
                e_prime[i] <= t_init + bigM * (1 - u_block[i, k, idx]),
                ctname=f"block_e_before_{i}_{k}_{idx}"
            )
            # (2) m'_i >= t_end - bigM*(1 - v_block[i, k, idx})
            mdl.add_constraint(
                m_prime[i] >= t_end - bigM * (1 - v_block[i, k, idx]),
                ctname=f"block_m_after_{i}_{k}_{idx}"
            )
            # (3) Disyunción si b_prime[i,k] = 1 => al menos una de u_block o v_block = 1
            mdl.add_constraint(
                u_block[i, k, idx] + v_block[i, k, idx] >= b_prime[i, k],
                ctname=f"block_or_{i}_{k}_{idx}"
            )

            # (4) (Opcional) Para forzar que u_block o v_block sean 0 si b_prime[i,k]=0
            mdl.add_constraint(u_block[i, k, idx] <= b_prime[i, k],
                            ctname=f"link_u_{i}_{k}_{idx}")
            mdl.add_constraint(v_block[i, k, idx] <= b_prime[i, k],
                            ctname=f"link_v_{i}_{k}_{idx}")

    # ============================
    # Resolución
    # ============================
    solution = mdl.solve(log_output=True)
    mdl.print_information()

    if not solution:
        print("No se encontró una solución factible.")
    else:
        print("Solución óptima encontrada.")
        total_Z1 = Z1.solution_value
        total_Z2 = Z2.solution_value
        total_Z3 = Z3.solution_value
        print(f"Z1: {total_Z1}, Z2: {total_Z2}, Z3: {total_Z3}")

        # ============================
        # Armado del "schedule"
        # ============================
        schedule = []
        for i in N:
            m_val = m_prime[i].solution_value
            e_val = e_prime[i].solution_value
            w_val = w_prime[i].solution_value
            delta_e_val = delta_e[i].solution_value
            assigned_berth = None
            for k in M:
                if b_prime[i, k].solution_value > 0.5:
                    assigned_berth = k
                    break

            # Identificar el sitio original
            original_berth = None
            for k in M:
                if b_ik.get((i, k), 0) == 1:
                    original_berth = k
                    break

            print(f"Buque {i}: m'_i={m_val}, e'_i={e_val}, w'_i={w_val}, muelle={assigned_berth}, original muelle={original_berth}")

            schedule.append({
                'Buque': i,
                'Sitio': assigned_berth,
                'Inicio': m_val,
                'Fin': e_val,
                'Inicio Planificado': A_i[i],
                'Fin Planificado': e_i[i],
                'Retraso': delta_e_val,
                'w_i': w_val,
                'Prioridad': mu_i[i],
                'Cambio de Sitio': int(b_ik.get((i, assigned_berth), 0) == 0),
                'Sitio Original': original_berth  # Añadido
            })

        # Mostrar el schedule final
        print("\n=== Schedule Final ===")
        for entry in schedule:
            print(entry)

# ============================
# Generación de gráficos
# ============================

def plot_schedule(schedule):
    fig, ax = plt.subplots(figsize=(14, 8))

    # Obtener todos los sitios únicos para asignar colores
    unique_berths = sorted(set(task['Sitio'] for task in schedule) | set(task['Sitio Original'] for task in schedule))
    berth_colors = {berth: color for berth, color in zip(unique_berths, plt.cm.Paired.colors)}

    # Para mantener la consistencia en la leyenda
    handled_berths = set()

    for task in schedule:
        buque = task['Buque']
        # Sitio Original
        original_berth = task['Sitio Original']
        original_color = berth_colors.get(original_berth, 'grey')  # Color por defecto si no se encuentra
        ax.barh(buque, task['Fin Planificado'] - task['Inicio Planificado'],
                left=task['Inicio Planificado'],
                color=original_color,
                edgecolor='black',
                alpha=0.3,  # Transparencia para distinguir del replanificado
                label=f'Sitio Original {original_berth}' if original_berth not in handled_berths else "")
        handled_berths.add(original_berth)

        # Sitio Replanificado
        new_berth = task['Sitio']
        new_color = berth_colors.get(new_berth, 'grey')
        ax.barh(buque, task['Fin'] - task['Inicio'],
                left=task['Inicio'],
                color=new_color,
                edgecolor='black',
                label=f'Sitio Replanificado {new_berth}' if new_berth not in handled_berths else "")
        handled_berths.add(new_berth)

    ax.set_xlabel('Tiempo')
    ax.set_ylabel('Buque')
    ax.set_title('Cronograma de Buques (Planificado vs. Replanificado)')

    # Crear una leyenda personalizada para evitar duplicados
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), bbox_to_anchor=(1.05, 1), loc='upper left')

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
