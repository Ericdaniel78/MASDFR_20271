# Práctica 1 — Modelo de pérdidas de tu ramo

**Matemáticas Actuariales para Seguro de Daños, Fianzas y Reaseguro** · Facultad de Ciencias, UNAM

Primer entregable del proyecto. Con la cartera de su ramo, van a **modelar la severidad y la frecuencia**, **simular la pérdida agregada S** y sacar de ahí la **prima pura preliminar** de su producto. Es todo lo que vimos en las Sesiones 2 a 7, aplicado a *sus* datos.

---

## 1. Contexto y objetivo

Su equipo es el área actuarial que va a lanzar un producto en su ramo. Para tarificarlo, lo primero es entender cuánto cuestan los siniestros (**severidad**), cuántos ocurren (**frecuencia**) y cuánto suman en total (**pérdida agregada S**).

Al terminar esta práctica tendrán, para su ramo:

- una distribución de severidad ajustada y justificada,
- una distribución de frecuencia ajustada y justificada,
- la distribución simulada de S y su **prima pura** (E[S]),
- y una lectura de si su cartera es consistente con el perfil de mercado del ramo.

Esto es el primer bloque de la **nota técnica** del producto.

> **Alcance (importante):** en esta práctica modelan la cartera de forma **agregada** (una sola severidad y una sola frecuencia para todos). Los datos traen **más información** de la que usan aquí (factores de riesgo por póliza): esa información **no se toca todavía**. En la **Práctica 2** la aprovecharán con GLM, y el modelo dejará de ser único para todos.

---

## 2. Los datos

Su cartera está en su carpeta del repo, en formato **parquet**:

```
entregas/equipo_XX/inputs/cartera.parquet
```

La leen con `pandas`:

```python
import pandas as pd
df = pd.read_parquet("entregas/equipo_XX/inputs/cartera.parquet")
```

La cartera tiene **muchas columnas**, pero **para esta práctica solo les importan unas cuantas**. Parte del ejercicio es que **identifiquen cuáles sí necesitan** y dejen el resto:

| Necesitas para… | Variable | Qué es |
|---|---|---|
| ... | Numero de siniestros | número de siniestros de la póliza en el periodo |
| ... | Exposición | años-póliza (cuánto tiempo estuvo expuesta) |
| ... | Monto de sinietro | monto **ground-up** (el daño real) de cada siniestro |
| ... | Deducible etc. | condiciones de la póliza, para pasar de la severidad real a la que paga la aseguradora |

El resto de columnas (factores de riesgo, fechas, etc.) **existen pero no se usan aquí**. En su notebook, digan explícitamente **qué variables eligieron y por qué**.

---

## 3. Lo que deben hacer

### a) Exploración de las variables de interés
Describan su ramo y exploren **solo** las variables que importan: la distribución de número de sinsitrsos, exposición y monto de siniestro. Reporten los descriptivos básicos (media, mediana, forma de la cola). No hagan un tour por todo el dataset: enfóquense.

### b) Severidad
- Ajusten varias distribuciones (lognormal, gamma, Weibull, Pareto…) y **elijan una con criterio**: AIC **y** el comportamiento de la **cola** (no solo el número).
- Consideren las **transformaciones** de la póliza: distingan la severidad **ground-up** (el daño real) de la que **paga la aseguradora** tras aplicar deducible etc. Recuerden lo de la Sesión 3: ajustar sobre datos ya transformados sesga.

### c) Frecuencia
- Ajusten **todas** las opciones que vimos —Poisson y binomial negativa— y **diagnostiquen**: índice de dispersión, sobredispersión, exceso de ceros (quasi-Poisson/ZIP a nivel diagnóstico).
- **Ustedes deciden** cuál queda mejor con base en el diagnóstico; no asuman Poisson de entrada.
- Usen correctamente la **exposición**: la tasa es total de siniestros entre total de exposición, no un promedio simple.

### d) Simulación de la pérdida agregada S
Con la severidad y la frecuencia que eligieron, simulen S (el algoritmo de la Sesión 7), en **dos versiones**:
- **S ground-up:** con la severidad del daño real.
- **S transformada:** aplicando deducible y suma asegurada (lo que realmente paga la aseguradora).

Para cada versión reporten la **distribución de S**, la **prima pura** E[S] y los cuantiles **VaR y TVaR** al 99%. Comparen las dos: **¿cuánto de la pérdida absorbe la póliza?** ¿Cuál es la que sirve para la prima del producto y por qué?

### e) Validación contra la guía de ramos *(obligatoria)*
Comparen lo que **les salió** con el perfil de mercado de su ramo de la **guía de ramos (Sesión 6)**: rango y cola de la severidad, nivel de frecuencia, distribución sugerida. ¿Su cartera cuadra con el perfil del ramo o hay diferencias? Analicen a qué se deben. Este apartado es parte de la calificación.

### f) Dos preguntas de introducción
Respondan en el notebook: **¿por qué les interesó este ramo?** y **¿qué coberturas van a trabajar en su producto?**

---

## 4. Entregable y formato

- Un notebook: `entregas/equipo_XX/practica1/practica1_equipoXX.ipynb`.
- Debe **correr de principio a fin** sin errores, ordenado y comentado, con **conclusiones** claras en cada apartado.
- Se entrega por **Pull Request**, siguiendo la *Guía de entrega* (fork → rama `entrega-practica1` → commit → push → PR titulado `Equipo XX — Práctica 1`).

## 5. Cómo se evalúa

Con la **rúbrica de prácticas** (correctitud técnica, justificación, código reproducible, entrega correcta, orden y presentación). Revísenla antes de entregar: buena parte de la nota está en **justificar** sus decisiones, no solo en correr código.

## 6. Lo que viene (para que lo tengan en el radar)

Esta cartera tiene factores de riesgo que aquí no usaron. En la **Práctica 2** los aprovecharán con **GLM**: en vez de una sola severidad y una sola frecuencia para todos, tendrán una **por perfil de riesgo**. Lo que entregan hoy es la base sobre la que se construye eso.
