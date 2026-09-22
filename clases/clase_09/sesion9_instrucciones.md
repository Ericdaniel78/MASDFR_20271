# Sesión 9 (asincrónica) — Instrucciones

**Matemáticas Actuariales para Seguro de Daños, Fianzas y Reaseguro** · Facultad de Ciencias, UNAM

Esta semana la **Sesión 9 es asincrónica**: la revisan por su cuenta con el material de abajo y entregan una **tarea por equipo**. Todo lo que necesitan está aquí; cualquier duda, la dejan en el grupo y la resolvemos por ahí.

> **Entrega:** por equipo · por Pull Request · **fecha límite: sábado 26 de septiembre, 23:59**
> **Esta tarea es obligatoria y cuenta** dentro del rubro de **prácticas/tareas (20%)** del curso.

---

## 1. Qué ver y correr *(a su ritmo)*

1. **Slides:** `sesion9_prima_tarifa_slides.pptx` — de la prima pura a la prima de tarifa: inflación, devaluación, y por qué cada supuesto se documenta.
2. **Notebook:** `sesion9_inflacion_notebook.ipynb` — ábranlo en VS Code con el kernel **MASDFR** y córranlo de principio a fin. Van a ver el ajuste por inflación y su efecto en la prima pura.

## 2. Qué tienen que resolver *(la tarea)*

En el notebook, completen las **cuatro celdas de ejercicio (✏️)**:

1. **Ejercicio 1** — el factor de ajuste de un año.
2. **Ejercicio 2** — el costo de no ajustar por inflación con otra frecuencia.
3. **Ejercicio 3** — sensibilidad al tipo de cambio (devaluación).
4. **Ejercicio 4** — **su tabla de supuestos**: agreguen una fila con un ajuste que aplique a **su ramo** (el que eligieron para el proyecto), con su **valor** y su **fuente**. Esta parte es la que conecta con su nota técnica: un supuesto sin fuente ni justificación no vale.

El notebook debe **correr completo sin errores** antes de entregar.

## 3. Dónde va su trabajo

Dentro de la carpeta de su equipo, **creen una carpeta `tarea_01`** y guarden ahí su notebook resuelto:

```
entregas/equipo_XX/tarea_01/tarea1_equipoXX.ipynb
```

(Sustituyan `XX` por el número de su equipo. Solo tocan la carpeta de su equipo.)

## 4. Cómo entregar por Pull Request *(paso a paso)*

Es el mismo flujo de las prácticas (detalle completo en la *Guía de entrega — fork + Pull Request*). Aquí, resumido:

**a) Trabajen sobre una rama nueva.** Párense dentro de la carpeta del repo `MASDFR_20271` y corran:

```bash
git checkout main
git pull upstream main            # traen lo último del curso
git checkout -b tarea1            # crean la rama de esta tarea
```

**b) Guarden su notebook** en `entregas/equipo_XX/tarea_01/` y súbanlo:

```bash
git add .
git commit -m "Equipo XX — Tarea 1 (Sesión 9)"
git push -u origin tarea1
```

**c) Abran el Pull Request (en la web).** Esto es la entrega — el `push` **no** la crea:

1. Entren a su fork en GitHub; aparece el botón **Compare & pull request** (o pestaña *Pull requests → New pull request*).
2. Revisen las cajas de arriba: **`base repository` debe ser `Ericdaniel78/MASDFR_20271`** y `base: main` (¡no su fork!); `compare` debe ser su rama `tarea1`.
3. Título: **`Equipo XX — Tarea 1 (Sesión 9)`**. En la descripción, digan su ramo.
4. Clic en **Create pull request**.

> **Un solo PR por equipo.** Pueden hacer varios `push` mientras trabajan, pero abren **un** Pull Request. Si corrigen algo después, hacen más `push` a la misma rama `tarea1` y el PR se actualiza solo.

**d) Confirmen su entrega en Classroom:** peguen el **link de su Pull Request** en la tarea de Classroom.

## 5. Cómo se califica

Con la **rúbrica de prácticas** (correctitud, justificación, código reproducible, entrega correcta, orden y presentación), dentro del **20% de prácticas/tareas**. Lo esencial: que el notebook corra, que los ejercicios estén bien resueltos y **justificados**, y que el supuesto del Ejercicio 4 sea de su ramo, con fuente.

## 6. Checklist antes de entregar

- [ ] Vieron las slides y corrieron el notebook.
- [ ] Resolvieron los 4 ejercicios; el notebook corre de principio a fin sin errores.
- [ ] El notebook está en `entregas/equipo_XX/tarea_01/`.
- [ ] El Ejercicio 4 tiene un supuesto **de su ramo**, con valor y fuente.
- [ ] Abrieron **un** Pull Request `Equipo XX — Tarea 1 (Sesión 9)` hacia el repo del curso.
- [ ] Pegaron el link del PR en Classroom, antes del **sábado 26, 23:59**.

---

*Cualquier problema con Git o con el notebook, escríbanlo en el grupo y lo vemos. La idea de esta clase es que el ajuste por inflación deje de ser teoría y lo apliquen a los supuestos de su propio producto.*
