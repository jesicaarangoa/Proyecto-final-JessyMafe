# ============================================================
# pantallas/p4_filtros.py
# Pantalla de filtros: panel con los 6 filtros a la izquierda
# y la tabla de resultados a la derecha.
# ============================================================
import flet as ft                                                   # librería para la interfaz

from colores import CIRUELA, MALVA, LILA_BORDE, GRIS_MALVA, BLANCO
import manejo_datos as datos                                        # datos.df, datos.filtrado, aplicar_filtros
from piezas_comunes import barra_superior, boton_principal, opcion_clasificacion

MAX_FILAS = 100                                                     # máximo de filas que se dibujan (para que sea rápido)


def mostrar(page, navegar):
    df = datos.df                                                   # la versión más nueva de los datos
    promedio = df["Nota"].mean()                                    # promedio actual de las notas

    # --- Controles del panel izquierdo ---
    chk_nota = ft.Checkbox(label=f"Nota mayor al promedio ({promedio:.2f})")
    chk_cortas = ft.Checkbox(label="Cortas (menos de 100 min)")
    chk_populares = ft.Checkbox(label="Popularidad alta y +120 min")
    dd_genero = ft.Dropdown(label="Género", value="Todos", width=270,
                            options=[ft.DropdownOption(g) for g in ["Todos"] + sorted(df["Genero"].unique())])
    txt_desde = ft.TextField(label="Desde (año)", width=127, keyboard_type=ft.KeyboardType.NUMBER)
    txt_hasta = ft.TextField(label="Hasta (año)", width=127, keyboard_type=ft.KeyboardType.NUMBER)
    dd_clasif = ft.Dropdown(label="Clasificación", value="Todas", width=270,
                            options=[ft.DropdownOption("Todas")] +
                                    [opcion_clasificacion(c) for c in sorted(df["Clasificacion"].unique())])

    # --- Zona de resultados (derecha) ---
    conteo = ft.Text("", size=18, weight=ft.FontWeight.W_500, color=CIRUELA)
    nota_limite = ft.Text("", size=13, color=GRIS_MALVA)
    tabla = ft.DataTable(
        columns=[ft.DataColumn(ft.Text(t)) for t in
                 ["Código", "Título", "Género", "Nota", "Min", "Popularidad", "Año", "Clasificación"]],
        rows=[],
        heading_row_color="#F4F3F0",                                # encabezado gris claro
        border=ft.Border.all(1, LILA_BORDE),
        border_radius=8,
        column_spacing=18,
        data_row_max_height=56,
    )

    def mostrar_resultado(tabla_datos):                             # llena la tabla con un DataFrame
        tabla.rows = [
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(f["Codigo"])),
                ft.DataCell(ft.Container(width=200, content=ft.Text(f["Titulo"], max_lines=2))),   # título en máx. 2 líneas
                *[ft.DataCell(ft.Text(str(v))) for v in
                  [f["Genero"], f["Nota"], f["Duracion"], f["Popularidad"], f["Año"]]],
                ft.DataCell(ft.Container(width=170,                 # el significado de la clasificación
                                         content=ft.Text(datos.significado(f["Clasificacion"]), max_lines=2))),
            ])
            for _, f in tabla_datos.head(MAX_FILAS).iterrows()      # recorre fila por fila
        ]
        conteo.value = f"{len(tabla_datos)} de {len(df)} películas"
        nota_limite.value = (f"Se muestran las primeras {MAX_FILAS}." if len(tabla_datos) > MAX_FILAS
                             else ("Ninguna película cumple esos filtros. Prueba quitando alguno."
                                   if len(tabla_datos) == 0 else ""))

    def leer_anio(campo):                                           # lee un año opcional; "error" si es inválido
        campo.error = None
        texto = campo.value.strip()
        if texto == "":
            return None
        if not texto.isdigit():
            campo.error = "Solo números"
            return "error"
        return int(texto)

    def aplicar(e):
        desde, hasta = leer_anio(txt_desde), leer_anio(txt_hasta)
        if "error" in [desde, hasta]:                               # si un año está mal, no filtra
            page.update()
            return
        datos.filtrado = datos.aplicar_filtros(df, chk_nota.value, chk_cortas.value, chk_populares.value,
                                               dd_genero.value, desde, hasta, dd_clasif.value)   # se guarda para los gráficos
        mostrar_resultado(datos.filtrado)
        page.update()

    def limpiar(e):
        chk_nota.value = chk_cortas.value = chk_populares.value = False
        dd_genero.value, dd_clasif.value = "Todos", "Todas"
        txt_desde.value = txt_hasta.value = ""
        txt_desde.error = txt_hasta.error = None
        datos.filtrado = None                                       # sin filtros = todas
        mostrar_resultado(df)
        page.update()

    mostrar_resultado(df)                                           # al abrir, muestra todas

    titulo_seccion = lambda t: ft.Text(t, size=13, weight=ft.FontWeight.W_500, color=MALVA)
    panel = ft.Container(                                           # panel izquierdo con los filtros
        width=310,
        bgcolor=BLANCO,
        border=ft.Border.all(1, LILA_BORDE),
        border_radius=10,
        padding=18,
        content=ft.Column(spacing=12, controls=[
            titulo_seccion("FILTROS BÁSICOS"),
            chk_nota, chk_cortas, chk_populares, dd_genero,
            ft.Container(height=4),
            titulo_seccion("FILTROS ADICIONALES"),
            ft.Row(spacing=16, controls=[txt_desde, txt_hasta]),
            dd_clasif,
            ft.Row(spacing=10, controls=[
                boton_principal("Aplicar", ft.Icons.FILTER_ALT_OUTLINED, aplicar),
                ft.OutlinedButton("Limpiar", on_click=limpiar),
            ]),
        ]),
    )
    zona_resultados = ft.Container(                                 # derecha: conteo + tabla
        expand=True,
        content=ft.Column(spacing=10, controls=[
            ft.Row(wrap=True, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                conteo,
                ft.TextButton("Ver gráficos de estos resultados", icon=ft.Icons.SCATTER_PLOT_OUTLINED,
                              on_click=lambda e: navegar("graficos")),   # abre los gráficos con lo filtrado
            ]),
            nota_limite,
            ft.Row(scroll=ft.ScrollMode.AUTO, controls=[tabla]),       # si la tabla es ancha, se desliza
        ]),
    )

    page.add(
        barra_superior("Aplicar filtros", "Marca los filtros y presiona Aplicar", navegar),
        ft.Container(
            padding=28,
            content=ft.Row(spacing=24, vertical_alignment=ft.CrossAxisAlignment.START,
                           controls=[panel, zona_resultados]),
        ),
    )