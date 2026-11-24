# ============================================================
# pantallas/p1_inicio.py
# Pantalla principal: logo, 3 datos del dataset y las 5 tarjetas del menú.
# ============================================================
import flet as ft                                                   # librería para la interfaz

from colores import CIRUELA                                         # color del encabezado
import manejo_datos as datos                                        # para contar películas, años y promedio
from piezas_comunes import chip, tarjeta_opcion                     # piezas reutilizables


def mostrar(page, navegar):
    df = datos.df                                                   # la versión más nueva de los datos

    encabezado = ft.Container(
        bgcolor=CIRUELA,
        padding=ft.Padding.symmetric(vertical=44, horizontal=24),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,      # todo centrado
            spacing=10,
            controls=[
                ft.Image(src="logo.png", width=120, height=120, fit=ft.BoxFit.CONTAIN),   # logo de CineData
                ft.Row(                                             # datos calculados con Pandas
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

    # Cada tarjeta: (ícono, título, subtítulo, a qué pantalla lleva al hacer clic)
    opciones = ft.Row(
        wrap=True,                                                  # si no caben, bajan a otra fila
        spacing=16,
        run_spacing=16,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            tarjeta_opcion(ft.Icons.ADD, "Agregar película", "Registrar una película nueva",
                           lambda e: navegar("agregar")),
            tarjeta_opcion(ft.Icons.SEARCH, "Consultar y modificar", "Buscar por nombre o código",
                           lambda e: navegar("consultar")),
            tarjeta_opcion(ft.Icons.FILTER_ALT_OUTLINED, "Aplicar filtros", "Ver solo las que te interesan",
                           lambda e: navegar("filtros")),
            tarjeta_opcion(ft.Icons.SCATTER_PLOT_OUTLINED, "Visualizar gráficos", "Dispersión, caja e histograma",
                           lambda e: navegar("graficos")),
            tarjeta_opcion(ft.Icons.BAR_CHART, "Estadísticas", "Barras, líneas y pastel",
                           lambda e: navegar("estadisticas")),
        ],
    )

    page.add(
        encabezado,
        ft.Container(
            padding=32,
            content=ft.Column(
                spacing=18,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,  # ocupa todo el ancho
                controls=[ft.Text("¿Qué quieres hacer?", size=18, weight=ft.FontWeight.W_500, color=CIRUELA),
                          opciones],
            ),
        ),
    )