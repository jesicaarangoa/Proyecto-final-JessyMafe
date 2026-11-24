# ============================================================
# crear_graficos.py
# Dibuja los gráficos con Matplotlib (nada de pantallas).
# Cada gráfico se convierte en una imagen PNG que la pantalla muestra.
# ============================================================
import io                                                           # para guardar imágenes en memoria
import matplotlib                                                   # para los gráficos
matplotlib.use("Agg")                                               # dibuja en memoria, sin abrir ventanas aparte
import matplotlib.pyplot as plt

from colores import PALETAS                                         # las paletas Azul y Dorado


def figura_a_png(fig):                                              # convierte una figura de Matplotlib en imagen PNG
    memoria = io.BytesIO()                                          # un "archivo" que vive en la memoria
    fig.tight_layout()                                              # acomoda márgenes para que nada se corte
    fig.savefig(memoria, format="png", dpi=100)                     # guarda la figura como PNG
    plt.close(fig)                                                  # libera la memoria de la figura
    return memoria.getvalue()                                       # devuelve los bytes de la imagen


def crear_graficos(tabla, paleta="Azul"):                           # devuelve las 3 imágenes: dispersión, caja, histograma
    fuerte, suave = PALETAS[paleta]

    # 1. Dispersión: nota según el año
    fig, ax = plt.subplots(figsize=(5.2, 3.8))
    ax.scatter(tabla["Año"], tabla["Nota"], color=fuerte, alpha=0.6, edgecolors="white", linewidths=0.5)
    ax.set_title("Nota según el año de estreno")
    ax.set_xlabel("Año")
    ax.set_ylabel("Nota IMDb")
    ax.grid(alpha=0.3)
    dispersion = figura_a_png(fig)

    # 2. Caja: nota por género (los 5 géneros con más películas)
    top = tabla["Genero"].value_counts().head(5).index             # los 5 géneros más comunes
    grupos = [tabla[tabla["Genero"] == g]["Nota"] for g in top]     # las notas de cada género
    fig, ax = plt.subplots(figsize=(5.2, 3.8))
    ax.boxplot(grupos, patch_artist=True,
               boxprops=dict(facecolor=suave, edgecolor=fuerte),    # cajas con relleno suave y borde fuerte
               medianprops=dict(color="#1E1C24", linewidth=2),      # mediana en negro
               whiskerprops=dict(color=fuerte), capprops=dict(color=fuerte),
               flierprops=dict(markeredgecolor=fuerte))
    ax.set_xticks(range(1, len(top) + 1), list(top))                # nombre de cada género debajo de su caja
    ax.set_title("Nota por género (5 más comunes)")
    ax.set_xlabel("Género")
    ax.set_ylabel("Nota IMDb")
    ax.grid(axis="y", alpha=0.3)
    caja = figura_a_png(fig)

    # 3. Histograma: distribución de la duración
    fig, ax = plt.subplots(figsize=(5.2, 3.8))
    ax.hist(tabla["Duracion"], bins=12, color=fuerte, edgecolor="white")
    ax.set_title("Distribución de la duración")
    ax.set_xlabel("Duración (minutos)")
    ax.set_ylabel("Número de películas")
    ax.grid(axis="y", alpha=0.3)
    histograma = figura_a_png(fig)

    return [dispersion, caja, histograma]