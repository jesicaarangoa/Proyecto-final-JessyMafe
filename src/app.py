import flet as ft                                                   # librería para la interfaz
import pandas as pd                                                 # para leer el CSV limpio
from pathlib import Path                                            # para armar rutas de archivos

# ---------- Datos ----------
RUTA_DATOS = Path(__file__).parent.parent / "data" / "peliculas_limpio.csv"   # src/ → sube a la raíz → data/
df = pd.read_csv(RUTA_DATOS)                                        # carga las 398 películas

# ---------- Paleta de colores de CineData ----------
NEGRO = "#1E1C24"                                                   # encabezados y botones principales
DORADO = "#F2B84B"                                                  # ícono de inicio
CREMA = "#F6E7C8"                                                   # fondo de los íconos
CAFE = "#6B4207"                                                    # dibujo de los íconos
GRIS_FONDO = "#EEEDEA"                                              # fondo de la app
GRIS_BORDE = "#E2DFD8"                                              # bordes de las tarjetas
GRIS_TEXTO = "#5B5850"                                              # textos secundarios
GRIS_CLARO = "#D9D6CF"                                              # subtítulos sobre negro
BLANCO = "#FFFFFF"


def main(page: ft.Page):
    page.title = "CineData"                                         # título de la ventana
    page.window.width = 1000                                        # ancho inicial
    page.window.height = 720                                        # alto inicial
    page.window.min_width = 700                                     # no se puede achicar más de esto
    page.window.min_height = 500
    page.bgcolor = GRIS_FONDO                                       # color de fondo
    page.padding = 0                                                # sin margen alrededor
    page.scroll = ft.ScrollMode.AUTO                                # barra de desplazamiento si no cabe
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH       # todo ocupa el ancho completo

    # ---------- Piezas reutilizables ----------
    def chip(texto):                                                # pastillita con un dato (ej. "398 películas")
        return ft.Container(
            content=ft.Text(texto, size=13, color=CREMA),
            border=ft.Border.all(1, "#5A5462"),
            border_radius=16,
            padding=ft.Padding.symmetric(vertical=6, horizontal=14),
        )

    def tarjeta_opcion(icono, titulo, subtitulo, al_hacer_clic):    # cada botón grande del menú
        return ft.Container(
            width=320,
            padding=18,
            bgcolor=BLANCO,
            border=ft.Border.all(1, GRIS_BORDE),
            border_radius=12,
            ink=True,                                               # efecto de onda al hacer clic
            on_click=al_hacer_clic,                                 # qué hace al hacer clic
            content=ft.Row(
                spacing=16,
                controls=[
                    ft.Container(                                   # cuadrito crema con el ícono
                        width=48, height=48, border_radius=10, bgcolor=CREMA,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Icon(icono, color=CAFE, size=24),
                    ),
                    ft.Column(                                      # título y subtítulo
                        spacing=2,
                        controls=[
                            ft.Text(titulo, size=16, weight=ft.FontWeight.W_500, color=NEGRO),
                            ft.Text(subtitulo, size=13, color=GRIS_TEXTO),
                        ],
                    ),
                ],
            ),
        )

    # ---------- Pantalla de INICIO ----------
    def mostrar_inicio(e=None):
        page.clean()                                                # borra lo que haya en pantalla

        encabezado = ft.Container(
            bgcolor=NEGRO,
            padding=ft.Padding.symmetric(vertical=44, horizontal=24),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # todo centrado
                spacing=10,
                controls=[
                    ft.Icon(ft.Icons.MOVIE_FILTER_OUTLINED, size=80, color=DORADO),   # imagen alusiva
                    ft.Text("CineData", size=36, weight=ft.FontWeight.BOLD, color=BLANCO),
                    ft.Text("Gestión y análisis de las películas mejor calificadas de IMDb",
                            size=16, color=GRIS_CLARO, text_align=ft.TextAlign.CENTER),
                    ft.Row(                                         # datos calculados con Pandas
                        alignment=ft.MainAxisAlignment.CENTER,
                        wrap=True,
                        spacing=10,
                        controls=[
                            chip(f"{len(df)} películas"),
                            chip(f"{df['Año'].min()} a {df['Año'].max()}"),
                            chip(f"Nota promedio {df['Nota'].mean():.2f}"),
                        ],
                    ),
                ],
            ),
        )

        opciones = ft.Row(
            wrap=True,                                              # si no caben, bajan a otra fila
            spacing=16,
            run_spacing=16,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                tarjeta_opcion(ft.Icons.ADD, "Agregar película", "Registrar una película nueva",
                               lambda e: mostrar_pantalla("Agregar película")),
                tarjeta_opcion(ft.Icons.SEARCH, "Consultar y modificar", "Buscar por código y editar",
                               lambda e: mostrar_pantalla("Consultar y modificar")),
                tarjeta_opcion(ft.Icons.FILTER_ALT_OUTLINED, "Aplicar filtros", "Ver solo las que te interesan",
                               lambda e: mostrar_pantalla("Aplicar filtros")),
                tarjeta_opcion(ft.Icons.SCATTER_PLOT_OUTLINED, "Visualizar gráficos", "Dispersión, caja e histograma",
                               lambda e: mostrar_pantalla("Visualizar gráficos")),
                tarjeta_opcion(ft.Icons.BAR_CHART, "Estadísticas", "Barras, líneas y pastel",
                               lambda e: mostrar_pantalla("Estadísticas")),
            ],
        )

        page.add(
            encabezado,
            ft.Container(
                padding=32,
                content=ft.Column(
                    spacing=18,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,   # ocupa todo el ancho
                    controls=[ft.Text("¿Qué quieres hacer?", size=18, weight=ft.FontWeight.W_500, color=NEGRO),
                              opciones],
                ),
            ),
        )

    # ---------- Pantalla provisional (mientras construimos las demás) ----------
    def mostrar_pantalla(titulo):
        page.clean()                                                # borra el inicio
        page.add(
            ft.Container(                                           # barra superior oscura
                bgcolor=NEGRO,
                padding=ft.Padding.symmetric(vertical=18, horizontal=28),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,   # título a la izquierda, botón a la derecha
                    controls=[
                        ft.Text(titulo, size=22, weight=ft.FontWeight.W_500, color=BLANCO),
                        ft.OutlinedButton("Inicio", icon=ft.Icons.HOME_OUTLINED,
                                          style=ft.ButtonStyle(color=BLANCO),
                                          on_click=mostrar_inicio),  # vuelve al inicio
                    ],
                ),
            ),
            ft.Container(
                padding=32,
                content=ft.Text("Esta ventana está en construcción.", size=16, color=GRIS_TEXTO),
            ),
        )

    mostrar_inicio()                                                # al abrir la app, muestra el inicio


ft.run(main)                                                        # arranca la aplicación