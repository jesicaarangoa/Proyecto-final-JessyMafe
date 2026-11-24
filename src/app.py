# ============================================================
# app.py  ·  CineData   ▶ EMPIEZA AQUÍ
# Abre la ventana y cambia de una pantalla a otra.
# Para ejecutar la app: botón ▷ de VS Code con este archivo abierto.
# ============================================================
import flet as ft                                                   # librería para la interfaz
from pathlib import Path                                            # para armar la ruta de la carpeta assets

from colores import FONDO_ROSADO                                    # color de fondo de la app
from pantallas import (p1_inicio, p2_agregar, p3_consultar,         # los archivos de cada pantalla
                       p4_filtros, p5_graficos, p6_estadisticas)

# Nombre de cada pantalla → función que la dibuja
PANTALLAS = {
    "inicio": p1_inicio.mostrar,
    "agregar": p2_agregar.mostrar,
    "consultar": p3_consultar.mostrar,
    "filtros": p4_filtros.mostrar,
    "graficos": p5_graficos.mostrar,
    "estadisticas": p6_estadisticas.mostrar,
}


def main(page: ft.Page):
    page.title = "CineData"                                         # título de la ventana
    page.theme_mode = ft.ThemeMode.LIGHT                            # siempre en modo claro
    page.window.width = 1000                                        # ancho inicial
    page.window.height = 720                                        # alto inicial
    page.window.min_width = 700                                     # no se puede achicar más de esto
    page.window.min_height = 500
    page.bgcolor = FONDO_ROSADO                                     # color de fondo
    page.padding = 0                                                # sin margen alrededor
    page.scroll = ft.ScrollMode.AUTO                                # barra de desplazamiento si no cabe
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH       # todo ocupa el ancho completo

    def navegar(nombre, **opciones):                                # cambia de pantalla, ej. navegar("filtros")
        page.clean()                                                # 1. borra la pantalla actual
        PANTALLAS[nombre](page, navegar, **opciones)                # 2. busca la pantalla y la dibuja
        page.update()                                               # 3. refresca la ventana

    navegar("inicio")                                               # al abrir la app, muestra el inicio


ft.run(main, assets_dir=str(Path(__file__).parent / "assets"))      # arranca la app y carga el logo de assets/