# ============================================================
# piezas_comunes.py
# Piezas que se repiten en varias pantallas: pastillas, tarjetas,
# barra superior, botones, avisos y el formulario de películas
# (con su validación). Se escriben UNA vez y se usan en todas partes.
# ============================================================
import flet as ft                                                   # librería para la interfaz

from colores import (CIRUELA, LILA_PALIDO, MALVA, LILA_BORDE, GRIS_MALVA,
                     LILA_CLARO, BLANCO)                            # colores de la app
import manejo_datos as datos                                        # los datos (apodo corto, como "pd" para pandas)


# ---------- Piezas visuales ----------
def chip(texto):                                                    # pastillita con un dato (ej. "398 películas")
    return ft.Container(
        content=ft.Text(texto, size=13, color=LILA_PALIDO),
        border=ft.Border.all(1, "#5A5462"),
        border_radius=16,
        padding=ft.Padding.symmetric(vertical=6, horizontal=14),
    )


def tarjeta_opcion(icono, titulo, subtitulo, al_hacer_clic):        # cada botón grande del menú de inicio
    return ft.Container(
        width=320,
        padding=18,
        bgcolor=BLANCO,
        border=ft.Border.all(1, LILA_BORDE),
        border_radius=12,
        ink=True,                                                   # efecto de onda al hacer clic
        on_click=al_hacer_clic,                                     # qué hace al hacer clic
        content=ft.Row(spacing=16, controls=[
            ft.Container(                                           # cuadrito lila con el ícono
                width=48, height=48, border_radius=10, bgcolor=LILA_PALIDO,
                alignment=ft.Alignment.CENTER,
                content=ft.Icon(icono, color=MALVA, size=24),
            ),
            ft.Column(spacing=2, controls=[                         # título y subtítulo
                ft.Text(titulo, size=16, weight=ft.FontWeight.W_500, color=CIRUELA),
                ft.Text(subtitulo, size=13, color=GRIS_MALVA),
            ]),
        ]),
    )


def barra_superior(titulo, subtitulo, navegar):                     # franja oscura de arriba con el botón Inicio
    return ft.Container(
        bgcolor=CIRUELA,
        padding=ft.Padding.symmetric(vertical=18, horizontal=28),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,           # título a la izquierda, botón a la derecha
            controls=[
                ft.Column(spacing=2, controls=[
                    ft.Text(titulo, size=22, weight=ft.FontWeight.W_500, color=BLANCO),
                    ft.Text(subtitulo, size=14, color=LILA_CLARO),
                ]),
                ft.OutlinedButton("Inicio", icon=ft.Icons.HOME_OUTLINED,
                                  style=ft.ButtonStyle(color=BLANCO),
                                  on_click=lambda e: navegar("inicio")),   # vuelve al inicio
            ],
        ),
    )


def boton_principal(texto, icono, accion):                          # botón oscuro (Guardar, Buscar, Aplicar…)
    return ft.FilledButton(texto, icon=icono, style=ft.ButtonStyle(bgcolor=CIRUELA, color=BLANCO),
                           on_click=accion)


def avisar(page, texto):                                            # mensaje que aparece abajo unos segundos
    page.show_dialog(ft.SnackBar(ft.Text(texto)))


def opcion_clasificacion(codigo):                                   # opción de lista: guarda el código, muestra el significado
    return ft.DropdownOption(key=codigo, text=f"{datos.significado(codigo)} ({codigo})")


def grupo(titulo, controles):                                       # recuadro blanco con título (como en el diseño)
    return ft.Container(
        bgcolor=BLANCO,
        border=ft.Border.all(1, LILA_BORDE),
        border_radius=10,
        padding=20,
        content=ft.Column(spacing=14, controls=[
            ft.Text(titulo, size=14, weight=ft.FontWeight.W_500, color=MALVA),
            ft.Row(wrap=True, spacing=16, run_spacing=16, controls=controles),
        ]),
    )


# ---------- Formulario de películas (lo usan AGREGAR y CONSULTAR) ----------
def crear_campos():                                                 # crea todos los campos vacíos
    numero = ft.KeyboardType.NUMBER
    return {
        "Titulo": ft.TextField(label="Título", width=300),
        "Genero": ft.Dropdown(label="Género principal", width=220,
                              options=[ft.DropdownOption(g) for g in sorted(datos.df["Genero"].unique())]),
        "Director": ft.TextField(label="Director", width=260),
        "Nota": ft.TextField(label="Nota IMDb (0 a 10)", width=200, keyboard_type=numero),
        "Duracion": ft.TextField(label="Duración (min)", width=170, keyboard_type=numero),
        "Año": ft.TextField(label="Año", width=160, keyboard_type=numero),
        "Clasificacion": ft.Dropdown(label="Clasificación", width=300,
                                     options=[opcion_clasificacion(c) for c in sorted(datos.df["Clasificacion"].unique())]),
        "Metascore": ft.TextField(label="Metascore (opcional)", width=220, keyboard_type=numero),
        "Votos": ft.TextField(label="Votos", width=170, keyboard_type=numero),
        "Recaudacion": ft.TextField(label="Recaudación en millones USD (opcional)", width=360, keyboard_type=numero),
        "Popularidad": ft.Dropdown(label="Popularidad", width=170,
                                   options=[ft.DropdownOption(p) for p in ["Alta", "Media", "Baja"]]),
    }


def armar_grupos(campos, codigo):                                   # acomoda los campos en los 3 recuadros
    return [
        grupo("Datos principales", [codigo, campos["Titulo"], campos["Genero"], campos["Director"]]),
        grupo("Calificación y duración", [campos["Nota"], campos["Duracion"], campos["Año"],
                                          campos["Clasificacion"], campos["Metascore"]]),
        grupo("Público y taquilla", [campos["Votos"], campos["Recaudacion"], campos["Popularidad"]]),
    ]


def leer_numero(campo, minimo, maximo, entero=False, opcional=False):
    texto = campo.value.strip().replace(",", ".")                    # acepta 8,5 o 8.5
    if texto == "":                                                  # si está vacío…
        if opcional:                                                 # …y es opcional → sin dato
            return None
        campo.error = "Campo obligatorio"                            # …y es obligatorio → error
        return "error"
    try:
        valor = int(float(texto)) if entero else float(texto)        # intenta convertirlo en número
        if entero and float(texto) != valor:                         # ej. 102.5 no es entero
            raise ValueError
    except ValueError:                                               # si no es número…
        campo.error = "Solo enteros" if entero else "Solo números"
        return "error"
    if not (minimo <= valor <= maximo):                              # fuera de rango
        campo.error = f"Entre {minimo} y {maximo}"
        return "error"
    return valor


def validar(campos):                                                # revisa todo; devuelve los valores o None si hay error
    for c in campos.values():                                        # borra los errores anteriores
        if isinstance(c, ft.Dropdown):
            c.error_text = None
        else:
            c.error = None
    hay_error = False
    for clave in ["Titulo", "Director"]:                             # textos obligatorios
        if campos[clave].value.strip() == "":
            campos[clave].error = "Campo obligatorio"
            hay_error = True
    for clave in ["Genero", "Clasificacion", "Popularidad"]:         # listas obligatorias
        if campos[clave].value is None:
            campos[clave].error_text = "Elige una opción"
            hay_error = True
    valores = {
        "Nota": leer_numero(campos["Nota"], 0, 10),
        "Duracion": leer_numero(campos["Duracion"], 1, 600, entero=True),
        "Año": leer_numero(campos["Año"], 1888, 2030, entero=True),
        "Metascore": leer_numero(campos["Metascore"], 0, 100, opcional=True),
        "Votos": leer_numero(campos["Votos"], 0, 10_000_000, entero=True),
        "Recaudacion": leer_numero(campos["Recaudacion"], 0, 10_000, opcional=True),
    }
    if "error" in valores.values() or hay_error:
        return None
    for clave in ["Titulo", "Director"]:
        valores[clave] = campos[clave].value.strip()
    for clave in ["Genero", "Clasificacion", "Popularidad"]:
        valores[clave] = campos[clave].value
    return valores