# Descripción de los Parámetros y Conjuntos del Modelo de Replanificación de Atraques

Este documento proporciona una explicación detallada de cada uno de los parámetros y conjuntos utilizados en el modelo de optimización para la replanificación de atraques en un puerto marítimo. El objetivo es facilitar la comprensión de cómo se modela el problema y cómo se utilizan estos datos en el código.

---

## Conjuntos

- **N = [1, 2, 3]**  
  *Lista de buques que deben ser programados para atraque.*  
  En este caso, hay tres buques identificados con los números 1, 2 y 3.

- **M = [1, 2]**  
  *Lista de sitios de atraque disponibles en el muelle.*  
  Hay dos sitios de atraque disponibles, identificados como 1 y 2.

---

## Parámetros de Tiempo

- **a_i = {1: 2, 2: 5, 3: 7}**  
  *Tiempo de llegada real al puerto del buque* **i**.  
  - Buque 1: llega al tiempo 2.
  - Buque 2: llega al tiempo 5.
  - Buque 3: llega al tiempo 7.

- **A_i = {1: 2, 2: 5, 3: 7}**  
  *Tiempo de llegada planificado (cronograma base) del buque* **i**.  
  - Coincide con el tiempo de llegada real en este caso.

- **e_i = {1: 6, 2: 9, 3: 11}**  
  *Tiempo de salida planificado (cronograma base) del buque* **i**.  
  - Buque 1: planificado para salir al tiempo 6.
  - Buque 2: planificado para salir al tiempo 9.
  - Buque 3: planificado para salir al tiempo 11.

---

## Tiempos de Manipulación

- **H_ik = { (1,1): 4, (1,2): 5, (2,1): 3, (2,2): 4, (3,1): 2, (3,2): 3 }**  
  *Tiempo mínimo de manipulación (servicio) del buque* **i** *en el sitio de atraque* **k**.  
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
  *Tiempo estimado de manipulación (incluyendo posibles variaciones) del buque* **i** *en el sitio de atraque* **k**.  
  - Representa el tiempo que se espera que tome la manipulación del buque en cada sitio, considerando incertidumbres.

---

## Parámetros de Ubicación y Tamaño

- **L_i = {1: 100, 2: 150, 3: 120}**  
  *Longitud del buque* **i** *(en metros)*.  
  - Buque 1: 100 metros.
  - Buque 2: 150 metros.
  - Buque 3: 120 metros.

- **g_k = {1: 0, 2: 200}**  
  *Posición inicial del sitio de atraque* **k** *en el muelle (en metros)*.  
  - Sitio 1: inicia en el metro 0 del muelle.
  - Sitio 2: inicia en el metro 200 del muelle.

- **b_ik = { (1,1): 1, (1,2): 0, (2,1): 0, (2,2): 1, (3,1): 1, (3,2): 0 }**  
  *Asignación planificada del buque* **i** *al sitio de atraque* **k** *en el cronograma base*.  
  - Buque 1:
    - Asignado al sitio 1.
  - Buque 2:
    - Asignado al sitio 2.
  - Buque 3:
    - Asignado al sitio 1.

---

## Parámetros de Costos

- **c1 = 10**  
  *Costo por cambiar el sitio de atraque de un buque respecto al cronograma base.*  
  - Penaliza la reasignación de un buque a un sitio de atraque diferente al planificado.

- **c2 = 20**  
  *Costo por retraso en la salida del buque* **i** *respecto al cronograma base, ponderado por la prioridad* **μ_i**.  
  - Penaliza los retrasos en la salida de los buques, considerando su prioridad.

- **c3 = 30**  
  *Costo de retraso adicional para buques que llegaron a tiempo.*  
  - Aplica a buques que, aunque llegaron puntualmente, experimentan retrasos en su servicio.

- **μ_i = {1: 1, 2: 2, 3: 1}**  
  *Prioridad asignada al buque* **i**.  
  - Buque 1: prioridad 1.
  - Buque 2: prioridad 2 (mayor prioridad).
  - Buque 3: prioridad 1.

---

## Conjuntos de Sitios Factibles

- **M_i = {1: [1, 2], 2: [1, 2], 3: [1, 2]}**  
  *Conjunto de sitios de atraque factibles para el buque* **i**.  
  - Todos los buques pueden atracar en ambos sitios (1 y 2) en este ejemplo.

---

## Constante Grande

- **B = 1000**  
  *Constante grande utilizada en las restricciones del modelo (por ejemplo, en restricciones de no superposición y precedencia).*  
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
