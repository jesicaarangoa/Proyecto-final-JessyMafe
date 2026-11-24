# ============================================================
# pantallas/p6_estadisticas.py
# Pantalla ESTADÍSTICAS: barras, líneas y pastel.  ← PENDIENTE
# Por ahora muestra un aviso de "en construcción".
# ============================================================
import flet as ft                                                   # librería para la interfaz

from colores import GRIS_MALVA
from piezas_comunes import barra_superior


def mostrar(page, navegar):
    page.add(
        barra_superior("Estadísticas", "En construcción", navegar),
        ft.Container(
            padding=32,
            content=ft.Text("Esta ventana está en construcción.", size=16, color=GRIS_MALVA),
        ),
    )