# Sistema de Replanificación en Tiempo Real para Atraques Portuarios

Este proyecto implementa un modelo de **Replanificación de Atraques** usando _IBM CPLEX_ (vía la wrapper `docplex`) en Python.

## Estructura de Archivos

- **`main.py`**: Archivo principal que contiene la construcción y resolución del modelo.  
  Se ejecuta con:

  ```bash
  python main.py <archivo_datos.py>
  ```

  donde `<archivo_datos.py>` es un script Python que define las variables y parámetros (por ejemplo `datos.py`).

- **`datos.py`**: Archivo que contiene la definición de:

  - Conjuntos (`N`, `M`, `M_i`)
  - Parámetros (`a_i`, `A_i`, `e_i`, `h_ik`, `b_ik`, etc.)
  - Costos (`c1`, `c2`, `c3`) y la constante grande `B`
  - El diccionario `ventanas_bloqueo`, que detalla los intervalos de bloqueo para cada (buque, muelle).

- **Funciones de Ploteo**: Incluidas en `main.py` (o en módulos asociados) para mostrar Gantt y otros gráficos de retrasos, costos, etc.

---

## Requisitos de Instalación

### Python y Dependencias

1. Asegúrate de contar con **Python 3.10**.

2. Instala las dependencias listadas en `requirements.txt`. Por ejemplo:
   ```bash
   pip install -r requirements.txt
   ```
   donde `requirements.txt` podría contener:
   ```text
   docplex
   matplotlib
   numpy
   ```

### Instalación de CPLEX (IBM ILOG CPLEX)

1. Descarga e instala **CPLEX Community Edition** desde el sitio oficial de IBM:
   [Descargar CPLEX Community Edition](https://www.ibm.com/account/reg/es-es/signup?formid=urx-20028)
2. Asegúrate de instalar el _wrapper_ de Python que provee IBM. Por ejemplo, corriendo:
   ```bash
   python "C:\Program Files\IBM\ILOG\CPLEX_Studio_Community2211\python\setup.py" install
   ```
   _(La ruta puede variar según la versión y carpeta de instalación.)_

---

## Ejecución

Para **ejecutar** el modelo, basta con llamar:

```bash
python main.py datos.py
```

Donde `datos.py` (o cualquier otro nombre) es un archivo Python que define los parámetros del modelo en formato de estructuras Python nativas (listas, diccionarios, etc.).

El solver se ejecutará y producirá:

- **Solución Óptima** (o mensaje de inviabilidad).
- **Gráficos** de cronograma, retrasos, distribución de costos, y demás.

---

## Descripción de los Parámetros y Conjuntos

En el archivo `datos.py`, se definen:

1. **Conjuntos**:

   ```python
   N = [1, 2, 3, 4, 5, 6]  # Buques
   M = [1, 2, 3]           # Sitios de atraque
   M_i = {
       1: [2,3],
       2: [1,2],
       3: [1,2,3],
       4: [1,2,3],
       5: [1,3],
       6: [1,2,3]
   }
   ```

   - `N` y `M` son listas con la numeración de buques y muelles.
   - `M_i[i]` lista los muelles factibles para cada buque `i`.

2. **Parámetros Base**:

   ```python
   a_i = {1:5, 2:3, 3:5, 4:5, 5:6, 6:11}  # Llegada real
   A_i = {1:5, 2:3, 3:1, 4:7, 5:9, 6:12}  # Llegada planificada
   e_i = {1:9, 2:5, 3:5, 4:9, 5:10, 6:14} # Salida planificada
   h_ik = {
     (1,1):3.5, (1,2):2.0, (1,3):3.0,
     ...
   }
   b_ik = {
     (1,1):1, (1,2):0, (1,3):0,
     ...
   }
   mu_i = {1:12, 2:6, 3:2, 4:1, 5:9, 6:12}
   c1 = 18
   c2 = 30
   c3 = 30
   B  = 1000  # Big M
   ```

   - `a_i`, `A_i`, `e_i`: Tiempos de llegada y salida (real vs planificado).
   - `h_ik`: Tiempo de manipulación estimado si el buque `i` usa muelle `k`.
   - `b_ik`: Asignación base; 1 si el buque `i` estaba originalmente asignado al muelle `k`.
   - `mu_i`: Prioridad de cada buque.
   - `c1`, `c2`, `c3`: Coeficientes de costo para cambios de muelle y retrasos.
   - `B`: Constante grande usada en las restricciones de no superposición.

3. **Ventanas de Bloqueo**:
   ```python
   ventanas_bloqueo = {
       (1,1): [(0, 100)],
       (1,2): [(0, 100)],
       (1,3): [(7,11)],
       (2,1): [],
       (2,2): [],
       (2,3): [],
       (3,1): [],
       ...
   }
   ```
   - Este diccionario define, **para cada par (buque, muelle)**, una lista de intervalos `(t_start, t_end)` donde ese buque **no puede** permanecer atracado si se asigna a ese muelle.
   - Por ejemplo, `(1,1): [(0, 100)]` indica que el buque 1 **no** puede atracar en el muelle 1 dentro del intervalo [0..100].
   - **La lógica de bloqueo** en el modelo se implementa como una **disyunción linealizada**: si el buque `i` está asignado a muelle `k`, entonces su intervalo de atraque no puede solaparse con ninguno de los intervalos de `ventanas_bloqueo[i,k]`.

---

## Ventanas de Bloqueo (Resumen)

- En el modelo actual, **ignoramos** la simulación antigua de “cierre operativo genérico” y, en su lugar, utilizamos estas **ventanas de bloqueo** específicas por buque-muelle.
- Cada ventana `(t_init, t_end)` para `(i,k)` se interpreta así:

  > “Si el buque `i` se asigna al muelle `k`, deberá atracar **antes** de `t_init` **o** después de `t_end`.”

  En el **código** (ver `main.py`), esto se modela con **dos** binarias auxiliares (`u_block`, `v_block`) por ventana y la restricción disyuntiva:

  ```python
  e_prime[i] <= t_init + BigM*(1 - u_block[i,k,idx])
  m_prime[i] >= t_end  - BigM*(1 - v_block[i,k,idx])
  u_block[i,k,idx] + v_block[i,k,idx] >= b_prime[i,k]
  ```

  Esto garantiza que, si `b_prime[i,k] = 1`, el buque no coincida temporalmente con el intervalo bloqueado.

---

## Gráficos y Resultados

Luego de la optimización, `main.py` produce:

1. **Schedule Final**: Imprime en consola un resumen con la asignación real y planificada.
2. **Gráficos** de cronograma (`plot_schedule`), retrasos (`plot_delays`), costos (`plot_costs`), entre otros.

Para verlos, basta con ejecutar:

```bash
python main.py datos.py
```
