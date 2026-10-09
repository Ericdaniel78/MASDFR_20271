"""
app_final.py — Cotizador de prima (Tema 2) · MASDFR · FC UNAM
================================================================================
Sesión 13. App de Streamlit que junta TODO el Tema 2 sobre la cartera del equipo:
  · Pestaña UNIVARIADO    → una prima para toda la cartera, sin importar el perfil.
  · Pestaña MULTIVARIADO  → prima por perfil (empírica), y por qué todavía no alcanza.

Cómo se corre (NO desde un notebook):
    conda activate MASDFR
    streamlit run app_final.py

Idea de Streamlit: el script corre de arriba a abajo y se RE-EJECUTA completo en cada
interacción. Por eso cacheamos la carga de datos (@st.cache_data).
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# 0 · Configuración y paleta del curso
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Cotizador — MASDFR", page_icon="🛡️", layout="wide")
TEAL, ORANGE, BLUE2, SLATE, GRID = "#17A69B", "#E8873C", "#4C7FD1", "#8FA0C8", "#C7D0E6"

# Recargos de tarifa (rango investigado en la Sesión 12 — caso autos / Quálitas).
# Cada equipo pone AQUÍ el rango que obtuvo en su tarea de investigación.
RECARGOS = {
    "comisiones": (0.219, 0.231),   # índice de adquisición (min, max)
    "gastos":     (0.040, 0.053),   # índice de operación   (min, max)
    "margen":     (0.059, 0.059),   # margen técnico (≈ 100% − combinado)
}

BANDAS_EDAD = [17, 30, 40, 50, 60, 95]
BANDAS_ANT  = [-1, 2, 5, 10, 50]


# ─────────────────────────────────────────────────────────────────────────────
# 1 · Carga de datos (cacheada) — la fuente de verdad es la cartera del equipo
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def cargar_datos(ruta):
    df = pd.read_parquet(ruta)
    df["edad_cat"] = pd.cut(df["edad_conductor"], bins=BANDAS_EDAD).astype(str)
    df["ant_cat"]  = pd.cut(df["antiguedad_vehiculo"], bins=BANDAS_ANT).astype(str)
    return df

st.sidebar.header("Datos")
archivo = st.sidebar.file_uploader("Cartera (.parquet) de tu equipo", type=["parquet"])
RUTA = archivo if archivo is not None else "../../entregas/0_profesor/inputs/cartera_ejemplo_autos.parquet"
datos = cargar_datos(RUTA)
st.sidebar.caption(f"Pólizas: {len(datos):,}" +
                   ("  ·  cartera del profesor (ejemplo)" if archivo is None else "  ·  tu cartera"))


# ─────────────────────────────────────────────────────────────────────────────
# 2 · Funciones — las MISMAS que usaron en los notebooks (aquí solo se reúsan)
# ─────────────────────────────────────────────────────────────────────────────
def kpis(df):
    expo = df["exposicion"].sum()
    N    = int(df["num_siniestros"].sum())
    monto = df["monto_total_siniestros"].sum()
    freq = N / expo if expo > 0 else np.nan
    sev  = monto / N if N > 0 else np.nan     # severidad media POR siniestro
    return dict(expo=expo, N=N, monto=monto, freq=freq, sev=sev)

def prima_pura_empirica(df):
    expo = df["exposicion"].sum()
    return df["monto_total_siniestros"].sum() / expo if expo > 0 else np.nan

def prima_pura_producto(df):
    k = kpis(df)
    return k["freq"] * k["sev"]              # = Σmonto/Σexpo (misma cuenta, descompuesta)

def ajuste_frecuencia(df):
    """Poisson a los conteos; devuelve lambda y si hay sobredispersión."""
    N = df["num_siniestros"]
    lam = N.mean()
    sobredisp = N.var() > N.mean()
    return lam, sobredisp

def ajuste_severidad(df):
    """Lognormal a la severidad ground-up; devuelve mu, sigma, E[X]."""
    X = df["monto_promedio_siniestro"].dropna().values
    mu, sigma = np.log(X).mean(), np.log(X).std()
    return mu, sigma, float(np.exp(mu + sigma**2 / 2))

def prima_ajustada(df, deducible=0.0, coaseguro=0.0, limite=np.inf):
    """Prima pura tras aplicar condiciones de cobertura (Sesión 11)."""
    X = df["monto_promedio_siniestro"].dropna().values
    k = kpis(df)
    pago = (1 - coaseguro) * (np.minimum(X, limite) - np.minimum(X, deducible))
    return k["freq"] * np.maximum(pago, 0.0).mean()

def rango_tarifa(prima_pura):
    """Prima técnica = prima pura / (1 − g − m), con el rango de recargos (S12)."""
    g_lo = RECARGOS["comisiones"][0] + RECARGOS["gastos"][0] + RECARGOS["margen"][0]
    g_hi = RECARGOS["comisiones"][1] + RECARGOS["gastos"][1] + RECARGOS["margen"][1]
    return prima_pura / (1 - g_lo), prima_pura / (1 - g_hi)

def fig_estilo(ax, titulo):
    for sp in ax.spines.values(): sp.set_color(SLATE)
    ax.tick_params(colors=SLATE, labelsize=9)
    ax.set_title(titulo, color="#1C2E56", fontsize=11)
    ax.grid(alpha=.25)


# ─────────────────────────────────────────────────────────────────────────────
# 3 · Cuerpo
# ─────────────────────────────────────────────────────────────────────────────
st.title("🛡️ Cotizador de prima — Tema 2")
st.caption("De la cartera a la prima de tarifa. Univariado: una prima para todos. "
           "Multivariado: la prima que cambia con el perfil.")

tab_uni, tab_multi = st.tabs(["① Univariado (toda la cartera)", "② Multivariado (por perfil)"])

# ============================ PESTAÑA UNIVARIADO =============================
with tab_uni:
    k = kpis(datos)

    st.subheader("Métricas generales de la cartera")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Exposición (años-póliza)", f"{k['expo']:,.0f}")
    c2.metric("N.º de siniestros", f"{k['N']:,}")
    c3.metric("Frecuencia", f"{k['freq']:.4f}")
    c4.metric("Severidad media", f"${k['sev']:,.0f}")

    st.divider()
    st.subheader("Los ajustes de frecuencia y severidad")
    lam, sobredisp = ajuste_frecuencia(datos)
    mu, sigma, E_sev = ajuste_severidad(datos)
    g1, g2 = st.columns(2)

    with g1:
        st.markdown("**Frecuencia** — conteos vs. Poisson ajustada")
        N = datos["num_siniestros"]
        ks = np.arange(0, N.max() + 1)
        fig, ax = plt.subplots(figsize=(5.4, 3.3))
        ax.hist(N, bins=np.arange(-.5, N.max() + 1.5), density=True, color=TEAL, alpha=.6, label="observado")
        ax.plot(ks, stats.poisson(lam).pmf(ks), "o-", color=ORANGE, label=f"Poisson(λ={lam:.3f})")
        fig_estilo(ax, "¿Cuántos siniestros por póliza?"); ax.legend(fontsize=8)
        st.pyplot(fig)
        if sobredisp:
            st.caption("⚠️ Var > media: hay **sobredispersión**. La Poisson se queda corta; "
                       "la binomial negativa ajustaría mejor.")

    with g2:
        st.markdown("**Severidad** — montos vs. lognormal ajustada")
        X = datos["monto_promedio_siniestro"].dropna().values
        xs = np.linspace(0, np.percentile(X, 99), 200)
        fig, ax = plt.subplots(figsize=(5.4, 3.3))
        ax.hist(X, bins=60, range=(0, np.percentile(X, 99)), density=True, color=TEAL, alpha=.6, label="observado")
        ax.plot(xs, stats.lognorm(s=sigma, scale=np.exp(mu)).pdf(xs), color=ORANGE, lw=2,
                label=f"Lognormal(μ={mu:.2f}, σ={sigma:.2f})")
        fig_estilo(ax, "¿Cuánto cuesta cada siniestro?"); ax.legend(fontsize=8)
        st.pyplot(fig)

    st.divider()
    st.subheader("La prima pura de la cartera — por dos caminos")
    pp_emp = prima_pura_empirica(datos)
    pp_prod = prima_pura_producto(datos)
    pp_modelo = (datos["num_siniestros"].sum() / datos["exposicion"].sum()) * E_sev
    p1, p2, p3 = st.columns(3)
    p1.metric("Empírica (directa)", f"${pp_emp:,.2f}", help="Σ montos ÷ Σ exposición")
    p2.metric("Producto frec × sev", f"${pp_prod:,.2f}", help="(ΣN/Σexpo) × (Σmonto/ΣN)")
    p3.metric("Con las distribuciones", f"${pp_modelo:,.2f}", help="E[freq Poisson] × E[sev lognormal]")
    st.caption("Las dos primeras **coinciden** (es la misma cuenta, descompuesta). La tercera usa las "
               "distribuciones ajustadas: queda muy cerca, y es la que luego permite modelar.")

    st.divider()
    st.subheader("¿Cuánto cambia la prima con deducible y coaseguro?")
    cc1, cc2 = st.columns([1, 2])
    with cc1:
        ded = st.select_slider("Deducible", options=[0, 5000, 10000, 15000, 20000, 30000], value=10000)
        coa = st.select_slider("Coaseguro", options=[0.0, 0.10, 0.20, 0.30], value=0.0)
        pp_aj = prima_ajustada(datos, deducible=ded, coaseguro=coa)
        st.metric("Prima pura ajustada", f"${pp_aj:,.2f}", delta=f"{pp_aj/pp_emp - 1:+.1%} vs sin condiciones")
    with cc2:
        ded_grid = [0, 5000, 10000, 15000, 20000, 30000]
        fig, ax = plt.subplots(figsize=(6.2, 3.2))
        for c, col in [(0.0, TEAL), (0.20, ORANGE)]:
            ys = [prima_ajustada(datos, deducible=d, coaseguro=c) for d in ded_grid]
            ax.plot(ded_grid, ys, "o-", color=col, label=f"coaseguro {c:.0%}")
        ax.set_xlabel("deducible"); ax.set_ylabel("prima pura")
        fig_estilo(ax, "La prima baja de forma convexa"); ax.legend(fontsize=8)
        st.pyplot(fig)

    st.divider()
    st.subheader("La prima de tarifa (con el rango de recargos — Sesión 12)")
    t_lo, t_hi = rango_tarifa(pp_emp)
    tt1, tt2, tt3 = st.columns(3)
    tt1.metric("Prima pura", f"${pp_emp:,.2f}")
    tt2.metric("Tarifa (recargos mínimos)", f"${t_lo:,.2f}")
    tt3.metric("Tarifa (recargos máximos)", f"${t_hi:,.2f}")
    st.caption(f"Banda de tarifa **${t_lo:,.0f} – ${t_hi:,.0f}** usando comisiones "
               f"{RECARGOS['comisiones'][0]:.1%}–{RECARGOS['comisiones'][1]:.1%}, gastos "
               f"{RECARGOS['gastos'][0]:.1%}–{RECARGOS['gastos'][1]:.1%} y margen {RECARGOS['margen'][0]:.1%}. "
               "Cada equipo cambia estos rangos por los de su tarea de investigación.")

# ============================ PESTAÑA MULTIVARIADO ===========================
with tab_multi:
    st.subheader("La prima que depende del perfil")
    st.caption("Mismo cálculo que en univariado, pero sobre el **segmento** que elijas. "
               "Aquí se ve por qué el enfoque empírico todavía no alcanza.")

    f1, f2, f3 = st.columns(3)
    sexo = f1.selectbox("Sexo", ["(todos)"] + sorted(datos["sexo"].unique()))
    uso  = f1.selectbox("Uso", ["(todos)"] + sorted(datos["uso"].unique()))
    tipo = f2.selectbox("Tipo de vehículo", ["(todos)"] + sorted(datos["tipo_vehiculo"].unique()))
    zona = f2.selectbox("Zona", ["(todas)"] + sorted(datos["zona"].unique()))
    edad = f3.selectbox("Edad", ["(todas)"] + sorted(datos["edad_cat"].unique()))
    ant  = f3.selectbox("Antigüedad vehículo", ["(todas)"] + sorted(datos["ant_cat"].unique()))

    seg = datos.copy()
    for col, val, todos in [("sexo", sexo, "(todos)"), ("uso", uso, "(todos)"),
                            ("tipo_vehiculo", tipo, "(todos)"), ("zona", zona, "(todas)"),
                            ("edad_cat", edad, "(todas)"), ("ant_cat", ant, "(todas)")]:
        if val != todos:
            seg = seg[seg[col] == val]

    n = len(seg)
    pp_cartera = prima_pura_empirica(datos)

    if n == 0:
        st.error("🚫 **No hay NINGUNA póliza con ese perfil en los datos.** "
                 "El enfoque empírico no puede cotizar un perfil que no existe en la cartera. "
                 "Un modelo (GLM) sí podría, porque interpola entre características.")
    else:
        pp_seg = prima_pura_empirica(seg)
        m1, m2, m3 = st.columns(3)
        m1.metric("Pólizas en el segmento", f"{n:,}")
        m2.metric("Prima pura del segmento", f"${pp_seg:,.2f}",
                  delta=f"{pp_seg/pp_cartera - 1:+.0%} vs cartera")
        m3.metric("Prima pura de la cartera", f"${pp_cartera:,.2f}")

        if n < 100:
            st.warning(f"⚠️ Solo **{n} pólizas** en este segmento: la prima empírica es **poco creíble** "
                       "(mucho ruido). Al abrir más el perfil, los segmentos se vacían.")

        t_lo, t_hi = rango_tarifa(pp_seg)
        st.caption(f"Tarifa del segmento: **${t_lo:,.0f} – ${t_hi:,.0f}** (mismos recargos).")

    st.divider()
    st.info(
        "**¿Por qué todavía no alcanza?**  El modelo univariado (frecuencia × severidad de toda la "
        "cartera) da **una sola prima**: no distingue perfiles. Y el empírico por segmento **sí** "
        "distingue, pero se vuelve ruido cuando el segmento es chico y **no puede cotizar perfiles nuevos**. "
        "Necesitamos un modelo que diferencie por características sin quedarse sin datos: el **GLM**. "
        "Esa es la siguiente sesión."
    )
