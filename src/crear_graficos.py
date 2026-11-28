# ============================================================
# crear_graficos.py
# Dibuja los gráficos con Matplotlib (nada de pantallas).
# Cada gráfico se convierte en una imagen PNG que la pantalla muestra.
# ============================================================
import io                                                           # para guardar imágenes en memoria
import matplotlib                                                   # para los gráficos
matplotlib.use("Agg")                                               # dibuja en memoria, sin abrir ventanas aparte
import matplotlib.pyplot as plt

from colores import PALETAS                                         # las paletas Rosado y Dorado


def figura_a_png(fig):                                              # convierte una figura de Matplotlib en imagen PNG
    memoria = io.BytesIO()                                          # un "archivo" que vive en la memoria
    fig.tight_layout()                                              # acomoda márgenes para que nada se corte
    fig.savefig(memoria, format="png", dpi=100)                     # guarda la figura como PNG
    plt.close(fig)                                                  # libera la memoria de la figura
    return memoria.getvalue()                                       # devuelve los bytes de la imagen


def crear_graficos(tabla, paleta="Rosado"):                         # devuelve las 3 imágenes: dispersión, barras, histograma
    fuerte, _ = PALETAS.get(paleta, PALETAS["Rosado"])              # si el nombre no existe, usa Rosado

    # 1. Dispersión: nota según el año
    fig, ax = plt.subplots(figsize=(5.2, 3.8))
    ax.scatter(tabla["Año"], tabla["Nota"], color=fuerte, alpha=0.6, edgecolors="white", linewidths=0.5)
    ax.set_title("Nota según el año de estreno")
    ax.set_xlabel("Año")
    ax.set_ylabel("Nota IMDb")
    ax.grid(alpha=0.3)
    dispersion = figura_a_png(fig)

    # 2. Barras: promedio de nota por género (los 5 géneros con más películas)
    top = tabla["Genero"].value_counts().head(5).index             # los 5 géneros más comunes
    promedios = (tabla[tabla["Genero"].isin(top)]                   # solo esas películas
                 .groupby("Genero")["Nota"].mean()                  # promedio de nota de cada género
                 .sort_values(ascending=False))                     # de mayor a menor
    fig, ax = plt.subplots(figsize=(5.2, 3.8))
    dibujo = ax.bar(list(promedios.index), promedios.values, color=fuerte)
    ax.bar_label(dibujo, fmt="%.2f", padding=3)                     # escribe el promedio sobre cada barra
    ax.set_ylim(0, 10)                                              # escala completa de IMDb, desde cero
    ax.set_title("Promedio de nota por género (5 más comunes)", fontsize=11)
    ax.set_xlabel("Género")
    ax.set_ylabel("Nota IMDb promedio")
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)                                          # la cuadrícula queda detrás de las barras
    barras = figura_a_png(fig)

    # 3. Histograma: distribución de la duración
    fig, ax = plt.subplots(figsize=(5.2, 3.8))
    ax.hist(tabla["Duracion"], bins=12, color=fuerte, edgecolor="white")
    ax.set_title("Distribución de la duración")
    ax.set_xlabel("Duración (minutos)")
    ax.set_ylabel("Número de películas")
    ax.grid(axis="y", alpha=0.3)
    histograma = figura_a_png(fig)

    return [dispersion, barras, histograma]