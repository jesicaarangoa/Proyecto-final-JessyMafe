# ============================================================
# manejo_datos.py
# Todo lo que tiene que ver con los DATOS (solo Pandas, nada de pantallas):
# cargar el CSV, guardarlo, buscar, agregar, modificar y filtrar.
#
# IMPORTANTE: las pantallas escriben "import manejo_datos as datos"
# y usan "datos.df", así todas ven siempre la versión más nueva.
# ============================================================
import pandas as pd                                                 # para trabajar con la tabla de películas
from pathlib import Path                                            # para armar rutas de archivos

# ---------- Cargar los datos ----------
RUTA_DATOS = Path(__file__).parent.parent / "data" / "peliculas_limpio.csv"   # src/ → sube a la raíz → data/
df = pd.read_csv(RUTA_DATOS)                                        # carga las películas del CSV limpio
filtrado = None                                                     # último resultado filtrado (None = sin filtros)


# ---------- Significado de cada clasificación ----------
# El CSV guarda el código (PG-13); la pantalla muestra el significado.
CLASIFICACIONES = {
    "G": "Todo público",
    "PG": "Se sugiere compañía de un adulto",
    "PG-13": "Mayores de 13 años",
    "R": "Mayores de 17 (o con un adulto)",
    "NC-17": "Solo mayores de 17",
    "Approved": "Aprobada (sistema clásico)",
    "Passed": "Aprobada (sistema clásico)",
    "Not Rated": "Sin clasificar",
    "Unrated": "Sin clasificar",
    "TV-14": "Mayores de 14 años",
    "TV-MA": "Solo adultos",
    "TV-PG": "Se sugiere compañía de un adulto",
    "TV-G": "Todo público",
    "TV-Y7": "Mayores de 7 años",
}

def significado(codigo):                                            # "PG-13" → "Mayores de 13 años"
    return CLASIFICACIONES.get(str(codigo), str(codigo))            # si no lo conoce, deja el código


# ---------- Guardar ----------
def guardar():
    df.to_csv(RUTA_DATOS, index=False)                              # escribe el DataFrame en el CSV


# ---------- Agregar ----------
def siguiente_codigo():
    return "PEL-" + str(len(df) + 1).zfill(3)                       # ej. 398 películas → "PEL-399"

def agregar_pelicula(fila):
    global df                                                       # vamos a cambiar el df de este archivo
    df = pd.concat([df, pd.DataFrame([fila])], ignore_index=True)   # pega la fila nueva al final
    guardar()


# ---------- Buscar y modificar ----------
def buscar(texto):                                                  # devuelve las posiciones de las películas encontradas
    if texto.isdigit() or texto.upper().startswith("PEL-"):         # parece un CÓDIGO (21 o PEL-021)
        codigo = "PEL-" + texto.zfill(3) if texto.isdigit() else texto.upper()
        return list(df.index[df["Codigo"] == codigo])
    coincide = df["Titulo"].str.contains(texto, case=False, regex=False)   # si no, busca por NOMBRE
    return list(df.index[coincide])

def actualizar_pelicula(indice, valores):
    for columna, valor in valores.items():                          # cambia la fila columna por columna
        df.loc[indice, columna] = valor
    guardar()


# ---------- Filtros ----------
def aplicar_filtros(tabla, nota_alta=False, cortas=False, populares_largas=False,
                    genero="Todos", desde=None, hasta=None, clasificacion="Todas"):
    resultado = tabla                                               # empezamos con todas las películas
    if nota_alta:                                                   # 1. nota mayor al promedio
        resultado = resultado[resultado["Nota"] > tabla["Nota"].mean()]
    if cortas:                                                      # 2. películas cortas (menos de 100 min)
        resultado = resultado[resultado["Duracion"] < 100]
    if populares_largas:                                            # 3. popularidad alta y más de 120 min
        resultado = resultado[(resultado["Popularidad"] == "Alta") & (resultado["Duracion"] > 120)]
    if genero != "Todos":                                           # 4. un género específico
        resultado = resultado[resultado["Genero"] == genero]
    if desde is not None:                                           # 5a. desde un año
        resultado = resultado[resultado["Año"] >= desde]
    if hasta is not None:                                           # 5b. hasta un año
        resultado = resultado[resultado["Año"] <= hasta]
    if clasificacion != "Todas":                                    # 6. una clasificación específica
        resultado = resultado[resultado["Clasificacion"] == clasificacion]
    return resultado