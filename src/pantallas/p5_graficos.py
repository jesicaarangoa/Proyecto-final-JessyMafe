# ============================================================
# pantallas/p5_graficos.py
# Pantalla VISUALIZAR GRÁFICOS: dispersión, caja e histograma,
# con dos paletas de color. Usa las películas filtradas si las hay.
# ============================================================
import flet as ft                                                   # librería para la interfaz

from colores import CIRUELA, LILA_BORDE, GRIS_MALVA, BLANCO, PALETAS
import manejo_datos as datos                                        # datos.df y datos.filtrado
from crear_graficos import crear_graficos                           # crea las 3 imágenes
from piezas_comunes import barra_superior


def mostrar(page, navegar, paleta="Azul"):
    tabla = datos.df if datos.filtrado is None else datos.filtrado  # con filtros o sin filtros
    estado = "sin filtros" if datos.filtrado is None else "con los filtros aplicados"

    def boton_paleta(nombre):                                       # botón para elegir la paleta de colores
        fuerte, suave = PALETAS[nombre]
        activo = nombre == paleta
        return ft.OutlinedButton(
            content=ft.Row(tight=True, spacing=6, controls=[
                ft.Container(width=14, height=14, border_radius=7, bgcolor=fuerte),
                ft.Container(width=14, height=14, border_radius=7, bgcolor=suave),
                ft.Text(nombre, color=BLANCO if activo else CIRUELA),
            ]),
            style=ft.ButtonStyle(bgcolor=CIRUELA if activo else BLANCO),
            on_click=lambda e: navegar("graficos", paleta=nombre),  # redibuja con esa paleta
        )

    if len(tabla) == 0:                                             # nada que graficar
        contenido = [ft.Text("No hay películas con los filtros actuales. Cambia los filtros.",
                             size=16, color=GRIS_MALVA)]
    else:
        imagenes = crear_graficos(tabla, paleta)                    # las 3 imágenes PNG
        contenido = [ft.Row(wrap=True, spacing=16, run_spacing=16, alignment=ft.MainAxisAlignment.CENTER,
                            controls=[ft.Container(bgcolor=BLANCO, border=ft.Border.all(1, LILA_BORDE),
                                                   border_radius=10, padding=8,
                                                   content=ft.Image(src=img, width=470))
                                      for img in imagenes])]

    page.add(
        barra_superior("Visualizar gráficos", "Dispersión, caja e histograma", navegar),
        ft.Container(
            padding=28,
            content=ft.Column(
                spacing=18,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    ft.Row(wrap=True, alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                           vertical_alignment=ft.CrossAxisAlignment.CENTER, controls=[
                        ft.Row(spacing=10, controls=[ft.Text("Colores:", size=15, weight=ft.FontWeight.W_500),
                                                     boton_paleta("Azul"), boton_paleta("Dorado")]),
                        ft.Row(spacing=4, controls=[
                            ft.Text(f"Mostrando {len(tabla)} películas · {estado}", size=14, color=GRIS_MALVA),
                            ft.TextButton("Cambiar filtros", on_click=lambda e: navegar("filtros")),
                        ]),
                    ]),
                ] + contenido,
            ),
        ),
    )