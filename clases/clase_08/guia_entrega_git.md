# Guía de entrega — fork + Pull Request

**Matemáticas Actuariales para Seguro de Daños, Fianzas y Reaseguro** · Facultad de Ciencias, UNAM

Así entregan las prácticas del curso: cada equipo trabaja sobre **su propia copia** (un *fork*) del repositorio del curso y me manda su trabajo con un **Pull Request (PR)**. Nunca escriben en el repo del curso: lo dejan intacto y su entrega queda con registro y sello de tiempo.

> Repositorio del curso: `https://github.com/Ericdaniel78/MASDFR_20271`

---

## Referencia rápida: comandos que vas a usar

Todos se escriben en el **Anaconda Prompt** o en la **terminal integrada de VS Code**.

| Comando | Qué hace | Cuándo lo usas |
|---|---|---|
| `git clone <url>` | descarga un repositorio a tu computadora | una vez, para bajar tu fork |
| `git status` | muestra qué cambió y en qué rama estás | siempre, para ubicarte |
| `git add .` | marca tus cambios para el próximo commit | antes de `commit` |
| `git commit -m "..."` | guarda un punto en la historia | después de `add` |
| `git push` | sube tus commits a tu fork | después de `commit` |
| `git pull` | trae lo último del remoto | antes de empezar a trabajar |
| `git checkout -b <rama>` | crea una rama nueva y te mueve a ella | al empezar cada práctica |
| `git checkout <rama>` | te cambia a una rama existente | para moverte entre ramas |
| `git branch` | lista tus ramas y marca en cuál estás | para ubicarte |
| `git remote -v` | muestra los remotos (`origin`, `upstream`) | para verificar conexiones |
| `git log --oneline` | historial resumido de commits | para ver qué se ha hecho |

**La idea en una frase:** editas → `add` (marcas) → `commit` (guardas) → `push` (subes). Y `pull` para traer lo de los demás.

> **`origin` vs `upstream` (en 3 líneas)**
> - `origin` = **tu fork** (tuyo). Aquí **subes** con `push`.
> - `upstream` = **el repo del curso** (del profe). De aquí solo **bajas** con `pull`.
> - Regla: *bajo del profe con `pull upstream`, subo a lo mío con `push origin`.* Si un `push` falla por permisos, seguramente estás empujando a `upstream` por error.

---

## Antes de empezar (una sola vez)

- Tener **Git** instalado y una **cuenta de GitHub** (lo montamos en la Sesión 1).
- Cuando GitHub les pida contraseña al clonar o subir, usan un **Personal Access Token** (GitHub → *Settings → Developer settings → Personal access tokens*), **no** su contraseña.

---

## Paso 1 — Haz un fork del repo del curso *(una vez, una persona del equipo)*

1. Entra a `https://github.com/Ericdaniel78/MASDFR_20271`.
2. Arriba a la derecha, clic en **Fork**.
3. GitHub crea una copia en tu cuenta: `https://github.com/TU_USUARIO/MASDFR_20271`.

Solo **una persona por equipo** hace el fork (el **dueño del fork**); ese será el fork del equipo.

## Paso 2 — Agrega a tu equipo como colaboradores *(una vez)*

El resto del equipo necesita permiso para subir. El **dueño del fork**:

1. Entra a su fork en GitHub (`TU_USUARIO/MASDFR_20271`).
2. Va a **Settings → Collaborators → Add people** y escribe el **usuario de GitHub** de cada compañero.

Cada compañero **acepta la invitación** (le llega por correo/GitHub) y luego clona el **fork del equipo**:

```bash
cd Documentos
git clone https://github.com/DUEÑO_DEL_FORK/MASDFR_20271.git
cd MASDFR_20271
```

Así **todo el equipo** trabaja sobre el mismo fork.

## Paso 3 — Conecta el repo del curso como `upstream` *(una vez, recomendado)*

```bash
git remote add upstream https://github.com/Ericdaniel78/MASDFR_20271.git
git remote -v
```

Debes ver `origin` (tu fork) y `upstream` (el repo del curso).

---

## Cómo está organizado el repo (dónde va tu trabajo)

El repo del curso **ya trae** una carpeta para cada equipo:

```
entregas/
  equipo_01/
    inputs/        ← aquí el profe te deja TUS datos (la cartera de tu ramo, en .parquet)
  equipo_02/
    inputs/
  ...
  equipo_11/
```

- Tus **datos** llegan en `entregas/equipo_XX/inputs/` cuando haces `git pull upstream main`.
- Tu **trabajo** (los notebooks) lo guardas dentro de tu carpeta: `entregas/equipo_XX/practica1/`, `practica2/`, etc. (esas subcarpetas las creas tú al trabajar).
- **Solo tocas la carpeta de tu equipo.** No metas mano en las de otros.

---

## En cada práctica

### Paso 4 — Ubícate, trae lo último y crea la rama

> **¿Dónde me paro para esto?** Abre la terminal **dentro** de la carpeta del repo `MASDFR_20271` (o ábrela desde VS Code con *File → Open Folder* sobre esa carpeta). La rama aplica a **todo el repo**, así que no importa en qué subcarpeta estés, **siempre que estés dentro del repo**. Verifícalo con `git status`: si responde, estás dentro; si dice *"not a git repository"*, estás afuera.

```bash
git checkout main
git pull upstream main          # trae el material y tus datos más recientes
git checkout -b entrega-practica1
```

Trabaja siempre en una **rama de la práctica**, no en `main`.

> **Rama ≠ carpeta (no las confundas)**
> - Una **rama** (`checkout -b entrega-practica1`) es una línea de trabajo **interna de Git**; no es una carpeta y no la ves en el explorador. Sirve para que cada práctica sea un PR independiente.
> - Una **carpeta** (`entregas/equipo_XX/practica1/`) es una carpeta **de verdad**, donde guardas tus archivos.
> - En una práctica usas **las dos**: te pones en la rama `entrega-practica1` **y** guardas el notebook en la carpeta `entregas/equipo_XX/practica1/`.

### Paso 5 — Trabaja y guarda tus cambios

Crea tu carpeta de la práctica y trabaja ahí; tus datos ya están en `inputs/`:

```
entregas/equipo_XX/practica1/practica1_equipoXX.ipynb
entregas/equipo_XX/inputs/cartera.parquet        (te la dejó el profe)
```

Luego, desde cualquier punto dentro del repo:

```bash
git add .
git commit -m "Equipo XX — Entrega Práctica 1"
```

### Paso 6 — Sube tu rama al fork del equipo

```bash
git push -u origin entrega-practica1
```

### Paso 7 — Abre el Pull Request

1. En el fork, clic en **Compare & pull request**.
2. El PR va **de tu rama** hacia **`Ericdaniel78/MASDFR_20271`, rama `main`**.
3. Título: **`Equipo XX — Práctica 1`**. Descripción: ramo, qué hicieron y dónde está el notebook.
4. **Create pull request**. ¡Esa es tu entrega!

### Paso 8 — Atiende comentarios (si los hay)

Corrige y vuelve a subir a la **misma rama** (el PR se actualiza solo):

```bash
git add .
git commit -m "Correcciones de la revisión"
git push
```

---

## `.gitignore` recomendado

Crea un `.gitignore` en la raíz. Política de datos: los datos **oficiales** del curso vienen en `.parquet` y **sí** se versionan; **no** subas CSV pesados propios.

```
__pycache__/
.ipynb_checkpoints/
.venv/
*.pyc
.DS_Store
# No subas datos pesados en CSV. Los datos oficiales del curso vienen en .parquet.
*.csv
```

## Mantener tu fork al día (entre prácticas)

```bash
git checkout main
git pull upstream main
git push origin main
```

---

## Problemas frecuentes

- **Te pide contraseña y falla** → usa un Personal Access Token de GitHub, no tu contraseña.
- **Un compañero no puede hacer push** → falta que el dueño lo agregue como colaborador (Paso 2) y que él acepte la invitación.
- **`git status` dice "not a git repository"** → estás fuera del repo; entra a la carpeta `MASDFR_20271`.
- **Clonaste el repo del curso por error** (no el fork) → no podrás hacer push. Borra la carpeta y clona el fork del equipo.
- **Hiciste commits en `main`** → crea la rama ahora: `git checkout -b entrega-practica1` (tus commits recientes se van contigo).
- **El PR va hacia el lado equivocado** → debe ser *de tu rama* hacia *`Ericdaniel78/MASDFR_20271:main`*.

## Resumen del ciclo (con el fork ya clonado)

```bash
git checkout main && git pull upstream main
git checkout -b entrega-practicaN
# ...trabajas en entregas/equipo_XX/practicaN/ ...
git add .
git commit -m "Equipo XX — Entrega Práctica N"
git push -u origin entrega-practicaN
# abres el Pull Request en GitHub
```
