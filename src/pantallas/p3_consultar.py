# ============================================================
# pantallas/p3_consultar.py
# Pantalla CONSULTAR Y MODIFICAR: busca por nombre o por código
# y deja editar la película encontrada.
# ============================================================
import flet as ft                                                   # librería para la interfaz
import pandas as pd                                                 # solo para pd.isna (detectar datos vacíos)

from colores import CIRUELA, MALVA, LILA_BORDE, GRIS_MALVA, BLANCO, ROJO_ERROR
import manejo_datos as datos                                        # buscar, agregar y modificar películas
from piezas_comunes import (barra_superior, boton_principal, avisar,
                            crear_campos, armar_grupos, validar)


def mostrar(page, navegar):
    caja_busqueda = ft.TextField(label="Nombre o código de la película",
                                 hint_text="Interstellar o PEL-021", width=320)
    resultado = ft.Column(spacing=18, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)   # aquí sale lo encontrado

    def texto_de(valor):                                            # convierte un dato del df en texto para el campo
        if pd.isna(valor):                                          # dato vacío (NaN) → campo vacío
            return ""
        if isinstance(valor, float) and valor.is_integer():         # 74.0 → "74"
            return str(int(valor))
        return str(valor)

    def no_existe(busqueda):                                        # recuadro naranja cuando no se encuentra
        return ft.Container(
            bgcolor="#FBF1E6",
            border=ft.Border.all(1, "#EBC9A4"),
            border_radius=10,
            padding=20,
            content=ft.Row(
                wrap=True,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(spacing=4, controls=[
                        ft.Text(f"No encontramos ninguna película con «{busqueda}»",
                                size=16, weight=ft.FontWeight.W_500, color="#6E3A0C"),
                        ft.Text("Puedes registrarla ahora mismo.", size=14, color="#6E3A0C"),
                    ]),
                    boton_principal("Agregar esta película", ft.Icons.ADD, lambda e: navegar("agregar")),
                ],
            ),
        )

    def formulario_edicion(indice):                                 # formulario lleno con los datos de la película
        fila = datos.df.loc[indice]                                 # la fila encontrada
        codigo = ft.TextField(label="Código", value=fila["Codigo"], read_only=True, width=160)
        campos = crear_campos()
        for clave, campo in campos.items():                         # llena cada campo con su valor actual
            campo.value = fila[clave] if isinstance(campo, ft.Dropdown) else texto_de(fila[clave])
        mensaje = ft.Text("", size=15, color=ROJO_ERROR)

        def guardar_cambios(e):
            valores = validar(campos)
            if valores is None:
                mensaje.value = "Revisa los campos marcados en rojo."
                page.update()
                return
            datos.actualizar_pelicula(indice, valores)              # cambia la fila y guarda el CSV
            mensaje.value = ""
            avisar(page, f"Cambios guardados en {fila['Codigo']}")
            page.update()

        aviso_ok = ft.Container(                                    # franja verde "encontrada"
            bgcolor="#E7F2DF", border_radius=8, padding=12,
            content=ft.Row(spacing=8, controls=[
                ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color="#2D6A1E", size=20),
                ft.Text("Película encontrada. Puedes editar sus datos.", color="#2D6A1E", size=15),
            ]),
        )
        return [aviso_ok] + armar_grupos(campos, codigo) + [
            ft.Row(spacing=12, wrap=True, controls=[
                boton_principal("Guardar cambios", ft.Icons.SAVE_OUTLINED, guardar_cambios),
                mensaje,
            ]),
        ]

    def lista_opciones(indices):                                    # varias coinciden: lista para elegir una
        def elegir(indice):                                         # al tocar una, muestra su formulario
            resultado.controls.clear()
            resultado.controls.extend(formulario_edicion(indice))
            page.update()

        filas = []
        for i in indices[:10]:                                      # máximo 10 opciones
            f = datos.df.loc[i]
            filas.append(ft.Container(
                bgcolor=BLANCO, border=ft.Border.all(1, LILA_BORDE), border_radius=8,
                padding=ft.Padding.symmetric(vertical=10, horizontal=16), ink=True,
                on_click=lambda e, i=i: elegir(i),                  # i=i: cada opción recuerda SU película
                content=ft.Row(spacing=12, controls=[
                    ft.Icon(ft.Icons.MOVIE_OUTLINED, color=MALVA, size=20),
                    ft.Text(f["Titulo"], size=15, weight=ft.FontWeight.W_500, color=CIRUELA, expand=True),
                    ft.Text(f"{f['Año']} · {f['Codigo']}", size=13, color=GRIS_MALVA),
                ]),
            ))
        mas = [ft.Text(f"…y {len(indices) - 10} más. Escribe un nombre más completo.", size=13,
                       color=GRIS_MALVA)] if len(indices) > 10 else []
        return [ft.Text(f"{len(indices)} películas coinciden. Elige una:", size=16,
                        weight=ft.FontWeight.W_500, color=CIRUELA)] + filas + mas

    def buscar(e):
        texto = caja_busqueda.value.strip()                         # quita espacios al inicio y al final
        resultado.controls.clear()                                  # borra el resultado anterior
        caja_busqueda.error = None
        if texto == "":
            caja_busqueda.error = "Escribe un nombre o un código"
            page.update()
            return
        if texto.isdigit():                                         # muestra "21" como "PEL-021" en la caja
            caja_busqueda.value = "PEL-" + texto.zfill(3)
        encontradas = datos.buscar(texto)                           # la búsqueda la hace manejo_datos.py

        if len(encontradas) == 0:                                   # no existe → ofrecer agregarla
            resultado.controls.append(no_existe(caja_busqueda.value))
        elif len(encontradas) == 1:                                 # una sola → directo al formulario
            resultado.controls.extend(formulario_edicion(encontradas[0]))
        else:                                                       # varias → lista para elegir
            resultado.controls.extend(lista_opciones(encontradas))
        page.update()

    caja_busqueda.on_submit = buscar                                # Enter en la caja también busca

    page.add(
        barra_superior("Consultar y modificar", "Busca una película por su nombre o su código", navegar),
        ft.Container(
            padding=28,
            content=ft.Column(
                spacing=18,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    ft.Row(spacing=12, wrap=True, vertical_alignment=ft.CrossAxisAlignment.START, controls=[
                        caja_busqueda,
                        boton_principal("Buscar", ft.Icons.SEARCH, buscar),
                        ft.Container(padding=ft.Padding.only(top=14),
                                     content=ft.Text("Prueba: interstellar, lord o 21", size=13, color=GRIS_MALVA)),
                    ]),
                    resultado,
                ],
            ),
        ),
    )