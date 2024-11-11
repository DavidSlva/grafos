# Descripción de los Parámetros y Conjuntos del Modelo de Replanificación de Atraques

El objetivo de este README es proporcionar una descripción detallada de los parámetros y conjuntos del modelo de replanificación de atraques.

---

## Conjuntos

- **N = [1, 2, 3]**  
  _Lista de buques que deben ser programados para atraque._  
  En este caso, hay tres buques identificados con los números 1, 2 y 3.

- **M = [1, 2]**  
  _Lista de sitios de atraque disponibles en el muelle._  
  Hay dos sitios de atraque disponibles, identificados como 1 y 2.

---

## Parámetros de Tiempo

- **a_i = {1: 2, 2: 5, 3: 7}**  
  _Tiempo de llegada real al puerto del buque_ **i**.

  - Buque 1: llega al tiempo 2.
  - Buque 2: llega al tiempo 5.
  - Buque 3: llega al tiempo 7.

- **A_i = {1: 2, 2: 5, 3: 7}**  
  _Tiempo de llegada planificado (cronograma base) del buque_ **i**.

  - Coincide con el tiempo de llegada real en este caso.

- **e_i = {1: 6, 2: 9, 3: 11}**  
  _Tiempo de salida planificado (cronograma base) del buque_ **i**.
  - Buque 1: planificado para salir al tiempo 6.
  - Buque 2: planificado para salir al tiempo 9.
  - Buque 3: planificado para salir al tiempo 11.

---

## Tiempos de Manipulación

- **H_ik = { (1,1): 4, (1,2): 5, (2,1): 3, (2,2): 4, (3,1): 2, (3,2): 3 }**  
  _Tiempo mínimo de manipulación (servicio) del buque_ **i** _en el sitio de atraque_ **k**.

  - Buque 1:
    - Sitio 1: 4 unidades de tiempo.
    - Sitio 2: 5 unidades de tiempo.
  - Buque 2:
    - Sitio 1: 3 unidades de tiempo.
    - Sitio 2: 4 unidades de tiempo.
  - Buque 3:
    - Sitio 1: 2 unidades de tiempo.
    - Sitio 2: 3 unidades de tiempo.

- **h_ik = { (1,1): 4.5, (1,2): 5.5, (2,1): 3.5, (2,2): 4.5, (3,1): 2.5, (3,2): 3.5 }**  
  _Tiempo estimado de manipulación (incluyendo posibles variaciones) del buque_ **i** _en el sitio de atraque_ **k**.
  - Representa el tiempo que se espera que tome la manipulación del buque en cada sitio, considerando incertidumbres.

---

## Parámetros de Ubicación y Tamaño

- **L_i = {1: 100, 2: 150, 3: 120}**  
  _Longitud del buque_ **i** _(en metros)_.

  - Buque 1: 100 metros.
  - Buque 2: 150 metros.
  - Buque 3: 120 metros.

- **g_k = {1: 0, 2: 200}**  
  _Posición inicial del sitio de atraque_ **k** _en el muelle (en metros)_.

  - Sitio 1: inicia en el metro 0 del muelle.
  - Sitio 2: inicia en el metro 200 del muelle.

- **b_ik = { (1,1): 1, (1,2): 0, (2,1): 0, (2,2): 1, (3,1): 1, (3,2): 0 }**  
  _Asignación planificada del buque_ **i** _al sitio de atraque_ **k** _en el cronograma base_.
  - Buque 1:
    - Asignado al sitio 1.
  - Buque 2:
    - Asignado al sitio 2.
  - Buque 3:
    - Asignado al sitio 1.

---

## Parámetros de Costos

- **c1 = 10**  
  _Costo por cambiar el sitio de atraque de un buque respecto al cronograma base._

  - Penaliza la reasignación de un buque a un sitio de atraque diferente al planificado.

- **c2 = 20**  
  _Costo por retraso en la salida del buque_ **i** _respecto al cronograma base, ponderado por la prioridad_ **μ_i**.

  - Penaliza los retrasos en la salida de los buques, considerando su prioridad.

- **c3 = 30**  
  _Costo de retraso adicional para buques que llegaron a tiempo._

  - Aplica a buques que, aunque llegaron puntualmente, experimentan retrasos en su servicio.

- **μ_i = {1: 1, 2: 2, 3: 1}**  
  _Prioridad asignada al buque_ **i**.
  - Buque 1: prioridad 1.
  - Buque 2: prioridad 2 (mayor prioridad).
  - Buque 3: prioridad 1.

---

## Conjuntos de Sitios Factibles

- **M_i = {1: [1, 2], 2: [1, 2], 3: [1, 2]}**  
  _Conjunto de sitios de atraque factibles para el buque_ **i**.
  - Todos los buques pueden atracar en ambos sitios (1 y 2) en este ejemplo.

---

## Constante Grande

- **B = 1000**  
  _Constante grande utilizada en las restricciones del modelo (por ejemplo, en restricciones de no superposición y precedencia)._
  - Se asegura de que ciertas condiciones solo se activen cuando es necesario, evitando solapamientos en tiempo y espacio.

---

## Resumen del Uso de los Parámetros

Estos parámetros y conjuntos se utilizan en el modelo matemático para:

- **Determinar las asignaciones óptimas** de buques a sitios de atraque, considerando las limitaciones físicas y temporales.
- **Minimizar el costo total**, que incluye:
  - Costos de servicio adicionales debido a retrasos.
  - Costos asociados a la reasignación de buques a sitios diferentes a los planificados.
  - Costos por retrasos adicionales para buques que llegaron a tiempo.
- **Respetar las restricciones operativas**, como:
  - Los buques no pueden atracar antes de su tiempo de llegada.
  - No superposición en el uso de los sitios de atraque (espacio y tiempo).
  - Asignación de buques a sitios donde pueden ser atendidos (considerando su tamaño y calado).

---

python "C:\Program Files\IBM\ILOG\CPLEX_Studio_Community2211\python\setup.py" install
