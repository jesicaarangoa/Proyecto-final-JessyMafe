# ============================================================
# pantallas/p2_agregar.py
# Pantalla AGREGAR PELÍCULA: formulario vacío + botón Guardar.
# ============================================================
import flet as ft                                                   # librería para la interfaz

from colores import ROJO_ERROR                                      # color del aviso de error
import manejo_datos as datos                                        # para el código nuevo y guardar la película
from piezas_comunes import (barra_superior, boton_principal, avisar,
                            crear_campos, armar_grupos, validar)


def mostrar(page, navegar):
    codigo = ft.TextField(label="Código", value=datos.siguiente_codigo(), read_only=True, width=160)   # no se edita
    campos = crear_campos()                                         # todos los campos vacíos
    mensaje = ft.Text("", size=15, color=ROJO_ERROR)                # aquí aparece el aviso de error

    def guardar(e):
        valores = validar(campos)
        if valores is None:                                         # si algo falló, avisa y no guarda
            mensaje.value = "Revisa los campos marcados en rojo."
            page.update()
            return
        nueva = {"Codigo": codigo.value, **valores,                 # la fila nueva
                 "Generos": valores["Genero"], "Descripcion": ""}
        datos.agregar_pelicula(nueva)                               # la agrega al DataFrame y guarda el CSV
        avisar(page, f"{nueva['Titulo']} guardada como {codigo.value}")
        navegar("agregar")                                          # formulario vacío con el código siguiente

    def limpiar(e):
        for c in campos.values():
            c.value = None if isinstance(c, ft.Dropdown) else ""
            if isinstance(c, ft.Dropdown):
                c.error_text = None
            else:
                c.error = None
        mensaje.value = ""
        page.update()

    page.add(
        barra_superior("Agregar película", "Completa los campos y guarda", navegar),
        ft.Container(
            padding=28,
            content=ft.Column(
                spacing=18,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=armar_grupos(campos, codigo) + [
                    ft.Row(spacing=12, wrap=True, controls=[
                        boton_principal("Guardar película", ft.Icons.SAVE_OUTLINED, guardar),
                        ft.OutlinedButton("Limpiar campos", on_click=limpiar),
                        mensaje,
                    ]),
                ],
            ),
        ),
    )