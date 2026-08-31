# ============================================================================
#  Soluciones — Sesión 5 (Frecuencia: sobredispersión y modelo colectivo)
#  Matemáticas Actuariales para Seguro de Daños, Fianzas y Reaseguro · UNAM
#
#  Cada bloque es EXACTAMENTE el código que va en la celda del ejercicio.
#  Usa las variables que ya existen en el notebook
#  (conteos, ceros_obs, ceros_pois, phi, obs, e_po, e_nb, EN, EX, VarX, VarN_nb).
# ============================================================================


# --- Ejercicio 1 — confirma la sobredispersión -----------------------------
idx = conteos.var() / conteos.mean()
print(f"índice de dispersión = {idx:.3f}")
# Es claramente mayor que 1: hay sobredispersión. Usar Poisson tal cual subestimaría
# la varianza de N (y con ella el capital y el margen de riesgo del producto).


# --- Ejercicio 2 — mide el exceso de ceros ---------------------------------
razon = ceros_obs / ceros_pois
print(f"ceros observados : {ceros_obs:.3f}")
print(f"ceros esperados  : {ceros_pois:.3f}")
print(f"razón obs/esp    : {razon:.2f}  → hay {razon-1:.0%} más ceros de los que la Poisson espera")
# Ese exceso de ceros es una señal típica de seguros (la mayoría no reclama).
# Cuando es fuerte, el modelo indicado es un ZIP o un hurdle.


# --- Ejercicio 3 — el precio de la dispersión ------------------------------
inflacion = np.sqrt(phi) - 1
print(f"√φ = {np.sqrt(phi):.3f}")
print(f"Los errores estándar crecen {inflacion:.1%}")
# La estimación de la media no cambia, pero la incertidumbre sobre ella es ~26% mayor.
# Ignorar la dispersión daría intervalos de confianza demasiado optimistas.


# --- Ejercicio 4 — ¿quién ajusta mejor los ceros? --------------------------
print(f"observado en k=0 : {obs[0]:.3f}")
print(f"Poisson  en k=0  : {e_po[0]:.3f}")
print(f"NB       en k=0  : {e_nb[0]:.3f}")
print(f"error Poisson: {abs(obs[0]-e_po[0]):.3f}   error NB: {abs(obs[0]-e_nb[0]):.3f}")
# La binomial negativa se acerca más al observado en k=0: al permitir Var>media,
# reproduce mejor el exceso de ceros que la Poisson.


# --- Ejercicio 5 — la varianza tiene dos fuentes ---------------------------
term_conteo = VarN_nb * EX**2       # Var[N]·E[X]²  (variabilidad del NÚMERO de siniestros)
term_sev    = EN * VarX             # E[N]·Var[X]   (variabilidad de los MONTOS)
total = term_conteo + term_sev

print(f"aporte del conteo   (Var[N]·E[X]²): {term_conteo/total:.1%}")
print(f"aporte de severidad (E[N]·Var[X]) : {term_sev/total:.1%}")
# En esta cartera el término del conteo domina: la variabilidad del número de siniestros
# aporta la mayor parte de Var[S]. Por eso elegir bien la frecuencia (Poisson vs. NB)
# mueve tanto el riesgo agregado.
