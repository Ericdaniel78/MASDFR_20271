#!/usr/bin/env python3
"""
Revisión automática de entregas por Pull Request — MASDFR · Facultad de Ciencias, UNAM

Revisa lo MECÁNICO de una entrega (no califica el contenido):
  1. Título del PR con el formato  "Equipo XX — Práctica N"  (o "Tarea N").
  2. Que el PR solo toque la carpeta de su equipo:  entregas/equipo_XX/
  3. Que exista el notebook de entrega (y si tiene el nombre/carpeta pedidos).
  4. Que no haya archivos basura (.DS_Store, checkpoints, CSV) ni archivos pesados.
  5. Que el notebook corra de principio a fin en el ambiente del curso.

Uso en GitHub Actions: ver .github/workflows/revisar_entrega.yml
Uso local (profesor):
  python revisar_entrega.py --base <sha_base> --head <sha_head> --titulo "Equipo 04 — Práctica 1"
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

LIMITE_MB = 10            # tamaño máximo por archivo
TIMEOUT_CELDA = 600       # segundos por celda
BASURA = re.compile(r"(^|/)(\.DS_Store|__pycache__/|\.ipynb_checkpoints/|\.venv/)|\.pyc$", re.I)
PERMITIDAS = {".ipynb", ".md", ".py", ".txt"}

RE_TITULO = re.compile(
    r"equipo\s*_?0*(?P<eq>\d{1,2})\s*[—–\-:|]+\s*(?P<tipo>pr[aá]ctica|tarea)\s*_?0*(?P<n>\d+)",
    re.I,
)

PISTAS = {
    "FileNotFoundError": "No encontró un archivo. Lean los datos con una ruta relativa a la carpeta "
                         "del notebook, por ejemplo `pd.read_parquet(\"../inputs/cartera.parquet\")`; "
                         "no usen rutas de su computadora (`C:\\Users\\...`, `/Users/...`).",
    "ModuleNotFoundError": "Usaron un paquete que no está en el ambiente del curso (`environment.yml`). "
                           "Quítenlo o usen uno equivalente del ambiente.",
    "ImportError": "Usaron un paquete que no está en el ambiente del curso (`environment.yml`), "
                   "por ejemplo `tabulate`. Quítenlo o usen uno equivalente del ambiente.",
    "NameError": "Usan una variable que no se definió antes. Probablemente el notebook solo corría "
                 "ejecutando celdas en otro orden: prueben *Restart & Run All*.",
    "CellTimeoutError": f"Una celda tardó más de {TIMEOUT_CELDA // 60} minutos. Reduzcan el número "
                        "de simulaciones o optimicen el código.",
}


# ─── utilidades ──────────────────────────────────────────────────────────────
def git(*args: str) -> str:
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout


def archivos_cambiados(base: str, head: str) -> list[tuple[str, str]]:
    """[(estado, ruta)] de lo que cambia el PR respecto a main."""
    salida = git("diff", "--name-status", "--no-renames", f"{base}...{head}")
    filas = []
    for linea in salida.strip().splitlines():
        estado, ruta = linea.split("\t", 1)
        filas.append((estado[0], ruta))
    return filas


class Resultado:
    def __init__(self):
        self.checks: list[dict] = []
        self.detalles: list[str] = []

    def add(self, estado: str, nombre: str, detalle: str = ""):
        self.checks.append({"estado": estado, "check": nombre, "detalle": detalle})

    @property
    def hay_errores(self) -> bool:
        return any(c["estado"] == "error" for c in self.checks)

    @property
    def hay_avisos(self) -> bool:
        return any(c["estado"] == "aviso" for c in self.checks)


# ─── checks ──────────────────────────────────────────────────────────────────
def revisar_titulo(titulo: str, r: Resultado):
    m = RE_TITULO.search(titulo or "")
    if not m:
        r.add("aviso", "Título del PR",
              f"«{titulo}» no sigue el formato `Equipo XX — Práctica N`. Pueden editarlo en GitHub.")
        return None
    info = {"equipo": int(m["eq"]), "tipo": "tarea" if m["tipo"].lower().startswith("t") else "practica",
            "n": int(m["n"])}
    r.add("ok", "Título del PR", f"«{titulo}»")
    return info


def equipo_desde_rutas(rutas: list[str]) -> set[int]:
    eqs = set()
    for p in rutas:
        m = re.match(r"entregas/equipo_0*(\d+)/", p)
        if m:
            eqs.add(int(m[1]))
    return eqs


def es_basura(p: str) -> bool:
    return bool(BASURA.search(p)) or p.lower().endswith(".csv")


def igual_que_main(p: str, base_tip: str) -> bool:
    """True si el archivo es idéntico al que ya está en main (p. ej. volvieron a subir su cartera)."""
    try:
        return git("rev-parse", f"{base_tip}:{p}").strip() == git("hash-object", p).strip()
    except subprocess.CalledProcessError:
        return False


def revisar_alcance(cambios, equipo: int | None, base_tip: str, r: Resultado) -> int | None:
    rutas = [p for _, p in cambios]
    eqs = equipo_desde_rutas(rutas)
    if equipo is None:
        equipo = next(iter(eqs)) if len(eqs) == 1 else None
    if equipo is None:
        r.add("error", "Carpeta del equipo",
              "No se pudo identificar el equipo: el PR no trae archivos en `entregas/equipo_XX/` "
              "o trae de varios equipos.")
        return None

    carpeta = f"entregas/equipo_{equipo:02d}/"
    fuera = [f"`{e}` {p}" for e, p in cambios
             if not p.startswith(carpeta) and not es_basura(p) and Path(p).name != ".gitignore"]
    if fuera:
        r.add("error", "Solo tocan su carpeta",
              f"El PR modifica {len(fuera)} archivo(s) fuera de `{carpeta}`. "
              "Esos cambios no deben ir en la entrega (restáurenlos o quítenlos del PR).")
        r.detalles.append("**Archivos fuera de su carpeta** (A = agregado, M = modificado, D = borrado):\n\n"
                          + "\n".join(f"- {x}" for x in fuera))
    else:
        r.add("ok", "Solo tocan su carpeta", f"Todo dentro de `{carpeta}`")

    inputs = [p for e, p in cambios if p.startswith(carpeta + "inputs/") and not igual_que_main(p, base_tip)]
    if inputs:
        r.add("aviso", "Datos intactos",
              "Modificaron/agregaron archivos en `inputs/` (ahí solo van los datos que deja el profesor): "
              + ", ".join(f"`{Path(p).name}`" for p in inputs))
    return equipo


def revisar_basura(cambios, r: Resultado):
    basura, pesados, extra = [], [], []
    for e, p in cambios:
        if e == "D":
            continue
        if es_basura(p):
            basura.append(p)
        elif (Path(p).suffix.lower() not in PERMITIDAS and "/inputs/" not in p
              and Path(p).name != ".gitignore"):
            extra.append(p)
        if Path(p).exists() and Path(p).stat().st_size > LIMITE_MB * 1024 ** 2:
            pesados.append(f"{p} ({Path(p).stat().st_size / 1024 ** 2:.1f} MB)")
    if pesados:
        r.add("error", "Archivos pesados", f"Archivos de más de {LIMITE_MB} MB: " + ", ".join(pesados))
    if basura or extra:
        partes = []
        if basura:
            partes.append("archivos basura " + ", ".join(f"`{p}`" for p in basura)
                          + " (quítenlos y agreguen un `.gitignore` para que no vuelvan a subirse)")
        if extra:
            partes.append("archivos que no forman parte de la entrega " + ", ".join(f"`{p}`" for p in extra))
        r.add("aviso", "Sin archivos de más", "; ".join(partes) + ".")
    elif not pesados:
        r.add("ok", "Sin archivos de más")


def elegir_notebook(cambios, equipo: int, info: dict | None, r: Resultado) -> Path | None:
    carpeta = f"entregas/equipo_{equipo:02d}/"
    nbs = [p for e, p in cambios if e != "D" and p.startswith(carpeta) and p.endswith(".ipynb")
           and ".ipynb_checkpoints" not in p]
    if not nbs:
        r.add("error", "Notebook de entrega", f"No hay ningún `.ipynb` nuevo o modificado en `{carpeta}`.")
        return None

    esperado = None
    if info:
        t, n = info["tipo"], info["n"]
        sub = f"practica{n}" if t == "practica" else f"tarea_{n:02d}"
        esperado = f"{carpeta}{sub}/{t}{n}_equipo{equipo:02d}.ipynb"
        if esperado in nbs:
            r.add("ok", "Notebook de entrega", f"`{esperado}`")
            return Path(esperado)

    # no está con el nombre exacto: tomamos el más probable
    clave = (info or {}).get("tipo", "practica")[:5]
    def nombre(p):
        return Path(p).name.lower().replace("á", "a")
    candidatos = sorted(nbs, key=lambda p: (clave not in nombre(p), -Path(p).stat().st_size))
    elegido = candidatos[0]
    msg = f"Se revisó `{elegido}`."
    if esperado:
        msg += f" El nombre/carpeta pedidos eran `{esperado}`."
    if len(nbs) > 1:
        msg += f" (El PR trae {len(nbs)} notebooks.)"
    r.add("aviso", "Notebook de entrega", msg)
    return Path(elegido)


def ejecutar_notebook(ruta: Path, raiz: Path, r: Resultado) -> dict:
    import nbformat
    from nbclient import NotebookClient
    from nbclient.exceptions import CellExecutionError, CellTimeoutError

    def correr(cwd: Path):
        nb = nbformat.read(ruta, as_version=4)
        cliente = NotebookClient(nb, timeout=TIMEOUT_CELDA, kernel_name="python3",
                                 resources={"metadata": {"path": str(cwd)}})
        t0 = time.time()
        try:
            cliente.execute()
            return None, time.time() - t0, nb
        except CellTimeoutError as ex:
            return ("CellTimeoutError", str(ex)[:300], _celda_con_error(nb)), time.time() - t0, nb
        except CellExecutionError as ex:
            return (ex.ename, ex.evalue, _celda_con_error(nb)), time.time() - t0, nb

    fallo, seg, nb = correr(ruta.parent.resolve())
    if fallo and fallo[0] == "FileNotFoundError":          # segundo intento desde la raíz del repo
        fallo2, seg2, nb2 = correr(raiz)
        if not fallo2:
            fallo, seg, nb = None, seg2, nb2

    n_code = sum(c.cell_type == "code" for c in nb.cells)
    if not fallo:
        r.add("ok", "Corre de principio a fin", f"{n_code} celdas de código en {seg:.0f} s")
        return {"corre": True, "segundos": round(seg), "celdas": n_code}

    ename, evalue, (idx, fuente) = fallo
    r.add("error", "Corre de principio a fin", f"Falla en la celda {idx} con `{ename}`")
    pista = PISTAS.get(ename, "Prueben *Restart & Run All* en su computadora antes de hacer push.")
    r.detalles.append(
        f"**Error al ejecutar** — celda {idx}, `{ename}: {str(evalue).strip()[:300]}`\n\n"
        f"```python\n{fuente[:800]}\n```\n\n💡 {pista}"
    )
    return {"corre": False, "error": ename, "celda": idx, "segundos": round(seg), "celdas": n_code}


def _celda_con_error(nb):
    """(número de celda de código 1-based, fuente) de la celda que falló."""
    k = 0
    for c in nb.cells:
        if c.cell_type != "code":
            continue
        k += 1
        for o in c.get("outputs", []):
            if o.get("output_type") == "error":
                return k, c.source
    # timeout: la última con ejecución iniciada
    return k, ""


# ─── reporte ─────────────────────────────────────────────────────────────────
ICONO = {"ok": "✅", "aviso": "⚠️", "error": "❌"}


def reporte_md(r: Resultado, titulo: str) -> str:
    if r.hay_errores:
        cab = "## ❌ Entrega con problemas\nHay puntos que corregir antes de la fecha límite."
    elif r.hay_avisos:
        cab = "## ⚠️ Entrega recibida con observaciones\nEl notebook corre; revisen los avisos de forma."
    else:
        cab = "## ✅ Entrega en orden\nTodo lo mecánico está bien. La revisión de contenido la hace el profesor."
    tabla = "| | Revisión | Detalle |\n|---|---|---|\n" + "\n".join(
        f"| {ICONO[c['estado']]} | {c['check']} | {c['detalle']} |" for c in r.checks)
    partes = [cab, tabla]
    if r.detalles:
        partes.append("### Detalles\n\n" + "\n\n".join(r.detalles))
    partes.append("---\n*Revisión automática: solo checa forma y ejecución, **no** es la calificación. "
                  "Para corregir, hagan push a la misma rama; esta revisión se vuelve a correr sola.*")
    return "\n\n".join(partes)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--head", required=True)
    ap.add_argument("--titulo", default=os.environ.get("PR_TITLE", ""))
    ap.add_argument("--base-tip", help="punta de main para comparar datos (por defecto = --base)")
    ap.add_argument("--json", help="guardar resultado en JSON (uso local)")
    ap.add_argument("--no-ejecutar", action="store_true")
    a = ap.parse_args()

    raiz = Path(git("rev-parse", "--show-toplevel").strip())
    os.chdir(raiz)
    r = Resultado()
    cambios = archivos_cambiados(a.base, a.head)

    info = revisar_titulo(a.titulo, r)
    equipo = revisar_alcance(cambios, info["equipo"] if info else None, a.base_tip or a.base, r)
    revisar_basura(cambios, r)
    ejec = {}
    nb = None
    if equipo is not None:
        nb = elegir_notebook(cambios, equipo, info, r)
        if nb and not a.no_ejecutar:
            ejec = ejecutar_notebook(nb, raiz, r)

    md = reporte_md(r, a.titulo)
    print(md)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(md + "\n")
    if a.json:
        Path(a.json).write_text(json.dumps({
            "titulo": a.titulo, "equipo": equipo, "notebook": str(nb) if nb else None,
            "checks": r.checks, "ejecucion": ejec, "reporte_md": md}, ensure_ascii=False, indent=2))
    sys.exit(1 if r.hay_errores else 0)


if __name__ == "__main__":
    main()
