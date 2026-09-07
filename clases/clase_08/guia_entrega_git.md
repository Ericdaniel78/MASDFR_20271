# Guía de entrega — fork + Pull Request

**Matemáticas Actuariales para Seguro de Daños, Fianzas y Reaseguro** · Facultad de Ciencias, UNAM

Cada equipo trabaja sobre **su propia copia** (un *fork*) del repositorio del curso y entrega con **un Pull Request (PR)**. Nunca escriben en el repo del curso: lo dejan intacto y su entrega queda con registro y sello de tiempo.

> Repositorio del curso: `https://github.com/Ericdaniel78/MASDFR_20271`

---

## Referencia rápida: comandos que vas a usar

Se escriben en el **Anaconda Prompt** o en la **terminal integrada de VS Code**.

| Comando | Qué hace | Cuándo |
|---|---|---|
| `git clone <url>` | descarga un repositorio a tu computadora | una vez, para bajar tu fork |
| `git status` | muestra qué cambió y en qué rama estás | siempre, para ubicarte |
| `git add .` | marca tus cambios para el próximo commit | antes de `commit` |
| `git commit -m "..."` | guarda un punto en la historia | después de `add` |
| `git push` | sube tus commits a tu fork | después de `commit` |
| `git pull` | trae lo último del remoto | antes de trabajar / para traer lo de tus compañeros |
| `git checkout -b <rama>` | crea una rama nueva y te mueve a ella | al empezar cada práctica |
| `git checkout <rama>` | te cambia a una rama existente | para moverte entre ramas |
| `git remote -v` | muestra los remotos (`origin`, `upstream`) | para verificar conexiones |

**La idea en una frase:** editas → `add` → `commit` → `push`. Y `pull` para traer lo de los demás.

> **`origin` vs `upstream` (en 3 líneas)**
> - `origin` = **tu fork** (tuyo). Aquí **subes** con `push`.
> - `upstream` = **el repo del curso** (del profe). De aquí solo **bajas** con `pull`.
> - Regla: *bajo del profe con `pull upstream`, subo a lo mío con `push origin`.*

---

## Antes de empezar (una sola vez)

- Tener **Git** instalado y una **cuenta de GitHub**.
- Cuando GitHub pida contraseña al clonar o subir, usa un **Personal Access Token** (GitHub → *Settings → Developer settings → Personal access tokens*), **no** tu contraseña.

## Paso 1 — Fork del repo del curso *(una persona del equipo)*

En `https://github.com/Ericdaniel78/MASDFR_20271`, clic en **Fork**. Se crea tu copia: `https://github.com/TU_USUARIO/MASDFR_20271`. Esa persona es el **dueño del fork**.

## Paso 2 — Agrega a tu equipo como colaboradores *(una vez)*

El dueño del fork: en su fork → **Settings → Collaborators → Add people** → agrega el usuario de GitHub de cada compañero. Cada compañero **acepta la invitación** y clona el **fork del equipo**:

```bash
cd Documentos
git clone https://github.com/DUEÑO_DEL_FORK/MASDFR_20271.git
cd MASDFR_20271
```

Así **todo el equipo** trabaja sobre el mismo fork.

## Paso 3 — Conecta el repo del curso como `upstream` *(una vez)*

```bash
git remote add upstream https://github.com/Ericdaniel78/MASDFR_20271.git
git remote -v
```

Deben ver `origin` (tu fork) y `upstream` (el repo del curso).

---

## Cómo está organizado el repo

El repo ya trae una carpeta por equipo:

```
entregas/equipo_XX/inputs/     ← aquí el profe deja TUS datos (cartera .parquet)
```

- Tus **datos** llegan en `entregas/equipo_XX/inputs/` con `git pull upstream main`.
- Tu **trabajo** va en `entregas/equipo_XX/practica1/`, `practica2/`, … (esas subcarpetas las creas tú).
- **Solo tocas la carpeta de tu equipo.**

---

## En cada práctica: trabajan mucho, entregan una vez

> **La regla de oro:** el equipo hace **muchos `push`** mientras trabaja, pero **un solo Pull Request por práctica**, y lo abre **una sola persona** del equipo. El PR es "ya terminamos, revísennos" — **no** se hace a cada rato ni uno por integrante.

### A) Trabajo del equipo *(se repite cuantas veces haga falta)*

> **¿Dónde me paro?** Basta estar **dentro** de la carpeta del repo `MASDFR_20271` (cualquier subcarpeta sirve; la rama es de todo el repo). Verifícalo con `git status`.

Una vez, para arrancar la práctica:

```bash
git checkout main
git pull upstream main               # traer material y datos más recientes
git checkout -b entrega-practica1    # crear la rama del equipo
```

Después, cada integrante, sobre esa misma rama, cuantas veces quiera:

```bash
git checkout entrega-practica1       # (si no estás ya en ella)
git pull                             # traer lo que subieron tus compañeros
# ...trabajas en entregas/equipo_XX/practica1/ ...
git add .
git commit -m "Avance: ajuste de severidad"
git push                             # sube tu avance  (esto NO es la entrega)
```

> **Rama ≠ carpeta:** la **rama** (`entrega-practica1`) es una línea de trabajo interna de Git; la **carpeta** (`entregas/equipo_XX/practica1/`) es donde guardas el archivo. En una práctica usas las dos.

### B) Entrega *(una sola vez, cuando ya terminaron)*

**Una** persona del equipo abre **el** Pull Request:

1. En el fork, botón **Compare & pull request** (o la liga que GitHub muestra tras el push).
2. **Revisa las cajas de arriba** — deben quedar así:
   - `base repository: Ericdaniel78/MASDFR_20271` · `base: main`  ← **el repo del curso, no tu fork**
   - `head repository: TU_FORK` · `compare: entrega-practica1`
3. Título: `Equipo XX — Práctica 1`. Descripción: ramo, qué hicieron y dónde está el notebook.
4. **Create pull request.** Eso es la entrega.

> **Dos avisos que confunden a todos:**
> - El `push` **no crea** el Pull Request. Subir la rama solo sube el trabajo; el PR hay que **abrirlo** a mano.
> - Al abrirlo, si `base repository` apunta a tu fork, **cámbialo al repo del curso** (`Ericdaniel78/MASDFR_20271`); si no, el profesor no verá la entrega.

### C) Correcciones *(si el profesor comenta)*

**No abran otro PR.** Corrigen y hacen más push a la **misma rama**; el PR se actualiza solo:

```bash
git add .
git commit -m "Correcciones de la revisión"
git push
```

---

## `.gitignore` recomendado

Los datos oficiales vienen en `.parquet` y **sí** se versionan; no suban CSV pesados propios.

```
__pycache__/
.ipynb_checkpoints/
.venv/
*.pyc
.DS_Store
*.csv
```

---

## Problemas frecuentes

- **`permission denied` al hacer push** → te estás autenticando con una cuenta que **no** es dueña ni colaboradora del fork. Usa el Personal Access Token de la **cuenta correcta** (la del fork). En Windows, borra la credencial vieja en *Administrador de credenciales → Credenciales de Windows → git:https://github.com* y vuelve a hacer push.
- **Subí la rama pero no aparece mi entrega** → el push no crea el PR; falta **abrirlo** (sección B).
- **El profesor no ve el PR** → al abrirlo, `base repository` debe ser `Ericdaniel78/MASDFR_20271`, no tu fork.
- **Un compañero no puede hacer push** → falta que el dueño lo agregue como colaborador (Paso 2) y que acepte la invitación.
- **`git status` dice "not a git repository"** → estás fuera del repo; entra a la carpeta `MASDFR_20271`.
- **Hiciste commits en `main`** → crea la rama: `git checkout -b entrega-practica1` (tus commits se van contigo). `main` debe quedar siempre igual al del curso.

## Resumen

```bash
# Arranque de la práctica (una vez):
git checkout main && git pull upstream main
git checkout -b entrega-practicaN

# Trabajo (todo el equipo, muchas veces):
git pull ; git add . ; git commit -m "..." ; git push

# Entrega (una persona, una vez):
#   Compare & pull request  →  base: Ericdaniel78/MASDFR_20271 : main
```
