# Sistema de Replanificación en Tiempo Real para Atraques Portuarios

## Requisitos de Instalación

### Python y Dependencias

1. Asegúrate de contar con **Python 3.10**.

2. Las dependencias del proyecto están listadas en el archivo `requirements.txt`:
   ```text
   requests
   pynomo
   matplotlib
   ```
   Puedes instalar todas las dependencias ejecutando:
   ```bash
   pip install -r requirements.txt
   ```

### Instalación de CPLEX Community Edition

1. Descarga e instala **CPLEX Community Edition** desde el sitio oficial de IBM:  
   [Descargar CPLEX Community Edition](https://www.ibm.com/account/reg/es-es/signup?formid=urx-20028)

2. Durante la instalación, se te solicitará instalar un _wrapper_ de Python para **CPLEX**. Este paso es obligatorio para integrar **CPLEX** en el entorno de Python. Utiliza el siguiente comando para realizar esta instalación, ajustando la ruta según la ubicación de tu instalación:
   ```bash
   python "C:\Program Files\IBM\ILOG\CPLEX_Studio_Community2211\python\setup.py" install
   ```

> **Nota**: Todos los requisitos anteriores son necesarios y obligatorios para la ejecución del programa.

## Ejecución del Código

El programa se ejecuta desde la terminal y permite dos configuraciones de casos:

1. **Caso sin retraso**: Es la instancia que no considera un cierre operativo pero si actualiza la planificación en base a datos actualizados de tiempos de llegada y salida.

   ```bash
   python main.py sin_retraso.txt
   ```

2. **Caso con retraso**: Es la instancia que considera un retraso de cinco horas y los datos actualizados de tiempos de llegada y salida.
   ```bash
   python main.py con_retraso.txt
   ```

Cada archivo (`sin_retraso.txt` o `con_retraso.txt`) contiene los datos del modelo, incluyendo horarios planificados de llegada y salida, sitios de atraque disponibles, y otros parámetros de planificación y costos.

## Descripción de los Parámetros y Conjuntos del Modelo de Replanificación de Atraques

A continuación, se describe detalladamente cada uno de los parámetros y conjuntos utilizados en un caso de prueba en el modelo de replanificación de atraques.

### Conjuntos

- **N = [1, 2, 3]**  
  _Lista de buques que deben ser programados para atraque._

  - En este caso, hay tres buques identificados con los números 1, 2 y 3.

- **M = [1, 2]**  
  _Lista de sitios de atraque disponibles en el muelle._
  - Hay dos sitios de atraque disponibles, identificados como 1 y 2.

### Parámetros de Tiempo

- **a_i = {1: 2, 2: 5, 3: 7}**  
  _Tiempo de llegada real al puerto del buque_ **i**.

- **A_i = {1: 2, 2: 5, 3: 7}**  
  _Tiempo de llegada planificado (cronograma base) del buque_ **i**.

- **e_i = {1: 6, 2: 9, 3: 11}**  
  _Tiempo de salida planificado (cronograma base) del buque_ **i**.

### Tiempos de Manipulación

- **H_ik = { (1,1): 4, (1,2): 5, (2,1): 3, (2,2): 4, (3,1): 2, (3,2): 3 }**  
  _Tiempo mínimo de manipulación (servicio) del buque_ **i** _en el sitio de atraque_ **k**.

- **h_ik = { (1,1): 4.5, (1,2): 5.5, (2,1): 3.5, (2,2): 4.5, (3,1): 2.5, (3,2): 3.5 }**  
  _Tiempo estimado de manipulación (incluye posibles variaciones) del buque_ **i** _en el sitio de atraque_ **k**.

### Parámetros de Ubicación y Tamaño

- **L_i = {1: 100, 2: 150, 3: 120}**  
  _Longitud del buque_ **i** _(en metros)_.

- **g_k = {1: 0, 2: 200}**  
  _Posición inicial del sitio de atraque_ **k** _(en metros)_.

- **b_ik = { (1,1): 1, (1,2): 0, (2,1): 0, (2,2): 1, (3,1): 1, (3,2): 0 }**  
  _Asignación planificada del buque_ **i** _al sitio de atraque_ **k** en el cronograma base.

### Parámetros de Costos

- **c1 = 10**  
  _Costo por cambiar el sitio de atraque de un buque respecto al cronograma base._

- **c2 = 20**  
  _Costo por retraso en la salida del buque_ **i** _respecto al cronograma base, ponderado por la prioridad_ **μ_i**.

- **c3 = 30**  
  _Costo de retraso adicional para buques que llegaron a tiempo._

- **μ_i = {1: 1, 2: 2, 3: 1}**  
  _Prioridad asignada al buque_ **i**.

### Conjuntos de Sitios Factibles

- **M_i = {1: [1, 2], 2: [1, 2], 3: [1, 2]}**  
  _Conjunto de sitios de atraque factibles para el buque_ **i**.

### Constante Grande

- **B = 1000**
