# ============================================================================
#  Soluciones — Sesión 7 (Simulación de la pérdida agregada S)
#  Matemáticas Actuariales para Seguro de Daños, Fianzas y Reaseguro · UNAM
#
#  Cada bloque es EXACTAMENTE el código que va en la celda del ejercicio.
#  Usa las variables que ya existen en el notebook
#  (simular_S, sev, S, ES_teo, VarS_teo, var_tvar, np, stats).
# ============================================================================


# --- Ejercicio 1 — cambia la escala de la cartera --------------------------
S5 = simular_S(stats.poisson(5), M=20_000, seed=3)
print(f"media simulada = {S5.mean():,.1f}")
print(f"E[N]·E[X] = 5 · {sev.mean():,.1f} = {5 * sev.mean():,.1f}")
# La media simulada se acerca a 5·E[X]: la mitad de la frecuencia da la mitad de
# la prima esperada. La media de S escala directo con E[N].


# --- Ejercicio 2 — mide el error de la validación --------------------------
err_media = abs(S.mean() - ES_teo) / ES_teo
err_var   = abs(S.var()  - VarS_teo) / VarS_teo
print(f"error relativo en la media    = {err_media:.2%}")
print(f"error relativo en la varianza = {err_var:.2%}")
# Ambos están por debajo del ~1–2%: la simulación reproduce bien los DOS momentos.
# Si alguno saliera grande, habría un error en el código o en los supuestos.


# --- Ejercicio 3 — otro nivel de confianza ---------------------------------
v95, t95 = var_tvar(S, p=0.95)
v99, t99 = var_tvar(S, p=0.99)
print(f"VaR95 = {v95:,.0f}   TVaR95 = {t95:,.0f}")
print(f"TVaR99 es {t99 / v99 - 1:.0%} mayor que VaR99")
# El VaR es el umbral del percentil; el TVaR es el promedio de lo que hay MÁS ALLÁ
# de ese umbral, así que siempre es mayor: mide qué tan cara es la cola, no solo
# dónde empieza.


# --- Ejercicio 4 — la cola necesita más ------------------------------------
v_1000 = np.percentile(S[:1000], 99)
v_full = np.percentile(S, 99)
print(f"VaR99 con  1,000 simulaciones: {v_1000:,.0f}")
print(f"VaR99 con 50,000 simulaciones: {v_full:,.0f}")
# El de 50,000 es el estable. El VaR99 se apoya solo en el 1% más extremo:
# con 1,000 simulaciones apenas ~10 valores caen arriba del percentil 99, así que
# la estimación es ruidosa. La cola necesita muchas más simulaciones que la media.
