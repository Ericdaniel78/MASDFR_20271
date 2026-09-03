# Diccionario de datos — carteras del proyecto

**Matemáticas Actuariales para Seguro de Daños, Fianzas y Reaseguro** · Facultad de Ciencias, UNAM

Cada equipo tiene su cartera en `entregas/equipo_XX/inputs/cartera.parquet` (30,000 pólizas, una fila por póliza). Se lee con:

```python
import pandas as pd
df = pd.read_parquet("entregas/equipo_XX/inputs/cartera.parquet")
```

## Ramo asignado por equipo

| Equipo | Ramo | | Equipo | Ramo |
|---:|---|---|---:|---|
| 01 | Incendio | | 07 | Automóviles |
| 02 | Automóviles | | 08 | Incendio |
| 03 | Marítimo/transportes | | 09 | Automóviles |
| 04 | Crédito | | 10 | Automóviles |
| 05 | Responsabilidad civil | | 11 | Hogar |
| 06 | Crédito | | | |

---

## Columnas comunes (todos los ramos)

| Columna | Tipo | Descripción |
|---|---|---|
| `id_poliza` | texto | identificador único de la póliza |
| `exposicion` | float (0–1] | años-póliza: fracción del año que la póliza estuvo expuesta. **Úsala para la frecuencia** (tasa = Σ siniestros / Σ exposición) |
| *(factores de riesgo)* | varios | propios de cada ramo (ver abajo). **No se usan en la Práctica 1**; son para el GLM de la Práctica 2 |
| `suma_asegurada` | float | máximo que paga la aseguradora por la póliza |
| `deducible` | float | monto que absorbe el asegurado antes de que pague la aseguradora |
| `coaseguro` | float [0–1) | proporción del siniestro a cargo del asegurado |
| `num_siniestros` | int | número de siniestros de la póliza en el periodo |
| `monto_total_siniestros` | float | suma **ground-up** (daño real) de todos los siniestros de la póliza; 0 si no tuvo |
| `monto_promedio_siniestro` | float | costo medio por siniestro (`monto_total / num_siniestros`), **ground-up**. **Es la variable de severidad que modelan**. Es `NaN` si la póliza no tuvo siniestros |

> **Montos ground-up:** `monto_total_siniestros` y `monto_promedio_siniestro` son el **daño real**, antes de aplicar la póliza. Para obtener lo que **paga la aseguradora**, apliquen `deducible`, `suma_asegurada` (límite) y `coaseguro` (Sesión 3).

---

## Factores de riesgo por ramo (para el GLM — Práctica 2)

**Automóviles** — `edad_conductor`, `sexo`, `antiguedad_vehiculo`, `tipo_vehiculo` (compacto/sedan/suv/pickup/lujo), `uso` (particular/comercial), `zona`.

**Incendio** — `tipo_inmueble` (casa/departamento/comercio/industria), `material_construccion`, `uso_inmueble`, `giro`, `medidas_proteccion`, `antiguedad_inmueble`, `zona`.

**Marítimo/transportes** — `tipo_cobertura` (mercancía/casco), `tipo_bien`, `medio_transporte`, `ruta` (nacional/internacional).

**Crédito** — `monto_credito`, `plazo_meses`, `calificacion_deudor` (A/B/C/D), `sector`, `tipo_credito`.

**Responsabilidad civil** — `giro_actividad`, `tamano_empresa`, `limite_contratado`, `num_empleados`, `historial_reclamos`.

**Hogar** — `tipo_vivienda`, `valor_vivienda`, `zona`, `antiguedad_vivienda`, `num_habitantes`.

---

## Notas

- **Frecuencia:** `num_siniestros` con `exposicion` como offset. Las carteras traen **sobredispersión** (heterogeneidad de riesgo), así que diagnostiquen antes de asumir Poisson.
- **Severidad:** modelen `monto_promedio_siniestro` (filtren `num_siniestros > 0`).
- **Reservas (Track B / más adelante):** esta tabla **no** trae fechas ni pagos por siniestro. El detalle a nivel siniestro (`fecha_ocurrencia`, `fecha_reporte`, `fecha_pago`, `monto_pagado`, `monto_incurrido`, `estatus`) se libera cuando se necesite (o por *data request*).
