# ============================================================================
#  Soluciones — Sesión 4 (Frecuencia: el conteo, de la binomial a la Poisson)
#  Matemáticas Actuariales para Seguro de Daños, Fianzas y Reaseguro · UNAM
#
#  Cada bloque es EXACTAMENTE el código que va en la celda del ejercicio.
#  Usa las variables que ya existen en el notebook (conteos, obs, esp, stats, np).
# ============================================================================


# --- Ejercicio 1 — media, varianza y dispersión ----------------------------
media = conteos.mean()
var   = conteos.var()
print(f"media    = {media:.4f}")
print(f"varianza = {var:.4f}")
print(f"índice de dispersión = var/media = {var/media:.3f}")
# El índice está muy cerca de 1: la varianza ≈ la media. Eso es exactamente lo
# que cumple la Poisson (equidispersión), así que sugiere modelar con Poisson.


# --- Ejercicio 2 — la convergencia, compruébala ----------------------------
ks = np.arange(0, 12)
for nn in [8, 500]:
    diff = np.max(np.abs(stats.binom(nn, 2/nn).pmf(ks) - stats.poisson(2).pmf(ks)))
    print(f"n = {nn:>4}:  max|Bin − Poisson| = {diff:.5f}")
# Con n = 500 se parecen muchísimo más. Al crecer n y bajar p (manteniendo np = 2),
# la binomial se acerca a la Poisson(2): es su límite.


# --- Ejercicio 3 — ¿ajusta bien? -------------------------------------------
for k in [0, 1]:
    err = abs(obs[k] - esp[k]) / obs[k]
    print(f"k = {k}:  observado={obs[k]:.0f}  esperado={esp[k]:.0f}  error relativo={err:.2%}")
# Los errores son pequeños: la Poisson describe bien estos conteos. Es de esperarse,
# porque los generamos de una Poisson; con datos reales habría que revisar la cola.


# --- Ejercicio 4 — la tasa correcta ----------------------------------------
expos = np.array([1, 1, 0.5, 0.5, 1.0])
sinis = np.array([1, 0, 1,   0,   2  ])
lam = sinis.sum() / expos.sum()
print(f"λ̂ = ΣN/Σe = {sinis.sum():.0f}/{expos.sum():.1f} = {lam:.3f}")
print(f"media simple = ΣN/n = {sinis.mean():.3f}")
# La tasa por exposición (1.00) es mayor que la media simple (0.80): hay pólizas de
# medio año que aun así tuvieron siniestros. Al normalizar por años-póliza, el riesgo
# por unidad de tiempo sube. Usar la media simple lo subestima.


# --- Ejercicio 5 — detecta la sobredispersión ------------------------------
mezcla2 = np.concatenate([stats.poisson(0.2).rvs(6000), stats.poisson(2.0).rvs(4000)])
idx = mezcla2.var() / mezcla2.mean()
print(f"índice de dispersión = {idx:.3f}")
# Es mayor que 1: la mezcla de dos grupos de riesgo distinto genera sobredispersión.
# La Poisson (que exige var = media) subestimaría la variabilidad; el modelo adecuado
# es la binomial negativa (mezcla Poisson–Gamma), que sí permite var > media.
