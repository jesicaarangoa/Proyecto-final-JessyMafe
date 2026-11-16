import flet as ft                                                   # librería para la interfaz
import pandas as pd                                                 # para leer el CSV limpio
from pathlib import Path                                            # para armar rutas de archivos

# ---------- Datos ----------
RUTA_DATOS = Path(__file__).parent.parent / "data" / "peliculas_limpio.csv"   # src/ → sube a la raíz → data/  # src/ → sube a la raíz → data/
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
                    ft.Image(src="logo.png", width=120, height=120, fit=ft.BoxFit.CONTAIN),   # logo de CineData
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
                               mostrar_agregar),
                tarjeta_opcion(ft.Icons.SEARCH, "Consultar y modificar", "Buscar por código y editar",
                               mostrar_consultar),
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

    # ---------- Barra superior de cada ventana (título + botón Inicio) ----------
    def barra_superior(titulo, subtitulo):
        return ft.Container(
            bgcolor=NEGRO,
            padding=ft.Padding.symmetric(vertical=18, horizontal=28),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,       # título a la izquierda, botón a la derecha
                controls=[
                    ft.Column(spacing=2, controls=[
                        ft.Text(titulo, size=22, weight=ft.FontWeight.W_500, color=BLANCO),
                        ft.Text(subtitulo, size=14, color=GRIS_CLARO),
                    ]),
                    ft.OutlinedButton("Inicio", icon=ft.Icons.HOME_OUTLINED,
                                      style=ft.ButtonStyle(color=BLANCO),
                                      on_click=mostrar_inicio),      # vuelve al inicio
                ],
            ),
        )

    # ---------- Pantalla provisional (mientras construimos las demás) ----------
    def mostrar_pantalla(titulo):
        page.clean()                                                # borra el inicio
        page.add(
            barra_superior(titulo, "En construcción"),
            ft.Container(
                padding=32,
                content=ft.Text("Esta ventana está en construcción.", size=16, color=GRIS_TEXTO),
            ),
        )

    # ---------- Formulario compartido (lo usan AGREGAR y CONSULTAR) ----------
    def grupo(titulo, controles):                                   # recuadro con título (como en el diseño)
        return ft.Container(
            bgcolor=BLANCO,
            border=ft.Border.all(1, GRIS_BORDE),
            border_radius=10,
            padding=20,
            content=ft.Column(spacing=14, controls=[
                ft.Text(titulo, size=14, weight=ft.FontWeight.W_500, color=CAFE),
                ft.Row(wrap=True, spacing=16, run_spacing=16, controls=controles),
            ]),
        )

    def crear_campos():                                             # crea todos los campos vacíos del formulario
        numero = ft.KeyboardType.NUMBER
        return {
            "Titulo": ft.TextField(label="Título", width=300),
            "Genero": ft.Dropdown(label="Género principal", width=220,
                                  options=[ft.DropdownOption(g) for g in sorted(df["Genero"].unique())]),
            "Director": ft.TextField(label="Director", width=260),
            "Nota": ft.TextField(label="Nota IMDb (0 a 10)", width=200, keyboard_type=numero),
            "Duracion": ft.TextField(label="Duración (min)", width=170, keyboard_type=numero),
            "Año": ft.TextField(label="Año", width=160, keyboard_type=numero),
            "Clasificacion": ft.Dropdown(label="Clasificación", width=170,
                                         options=[ft.DropdownOption(c) for c in sorted(df["Clasificacion"].unique())]),
            "Metascore": ft.TextField(label="Metascore (opcional)", width=220, keyboard_type=numero),
            "Votos": ft.TextField(label="Votos", width=170, keyboard_type=numero),
            "Recaudacion": ft.TextField(label="Recaudación en millones USD (opcional)", width=360, keyboard_type=numero),
            "Popularidad": ft.Dropdown(label="Popularidad", width=170,
                                       options=[ft.DropdownOption(p) for p in ["Alta", "Media", "Baja"]]),
        }

    def armar_grupos(campos, codigo):                               # acomoda los campos en los 3 recuadros
        return [
            grupo("Datos principales", [codigo, campos["Titulo"], campos["Genero"], campos["Director"]]),
            grupo("Calificación y duración", [campos["Nota"], campos["Duracion"], campos["Año"],
                                              campos["Clasificacion"], campos["Metascore"]]),
            grupo("Público y taquilla", [campos["Votos"], campos["Recaudacion"], campos["Popularidad"]]),
        ]

    def leer_numero(campo, minimo, maximo, entero=False, opcional=False):
        texto = campo.value.strip().replace(",", ".")                # acepta 8,5 o 8.5
        if texto == "":                                              # si está vacío…
            if opcional:                                             # …y es opcional → sin dato
                return None
            campo.error = "Campo obligatorio"                        # …y es obligatorio → error
            return "error"
        try:
            valor = int(float(texto)) if entero else float(texto)    # intenta convertirlo en número
            if entero and float(texto) != valor:                     # ej. 102.5 no es entero
                raise ValueError
        except ValueError:                                           # si no es número…
            campo.error = "Solo enteros" if entero else "Solo números"
            return "error"
        if not (minimo <= valor <= maximo):                          # fuera de rango
            campo.error = f"Entre {minimo} y {maximo}"
            return "error"
        return valor

    def validar(campos):                                            # revisa todo; devuelve los valores o None si hay error
        for c in campos.values():                                    # borra los errores anteriores
            if isinstance(c, ft.Dropdown):
                c.error_text = None
            else:
                c.error = None
        hay_error = False
        for clave in ["Titulo", "Director"]:                         # textos obligatorios
            if campos[clave].value.strip() == "":
                campos[clave].error = "Campo obligatorio"
                hay_error = True
        for clave in ["Genero", "Clasificacion", "Popularidad"]:     # listas obligatorias
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

    def boton_principal(texto, icono, accion):                      # botón negro (Guardar)
        return ft.FilledButton(texto, icon=icono, style=ft.ButtonStyle(bgcolor=NEGRO, color=BLANCO),
                               on_click=accion)

    def avisar(texto):                                              # mensaje que aparece abajo unos segundos
        page.show_dialog(ft.SnackBar(ft.Text(texto)))

    # ---------- Ventana AGREGAR PELÍCULA ----------
    def mostrar_agregar(e=None):
        page.clean()                                                # borra lo que haya en pantalla
        siguiente_codigo = "PEL-" + str(len(df) + 1).zfill(3)       # ej. PEL-399
        codigo = ft.TextField(label="Código", value=siguiente_codigo, read_only=True, width=160)   # no se edita
        campos = crear_campos()                                     # todos los campos vacíos
        mensaje = ft.Text("", size=15, color="#A32D2D")             # aquí aparece el aviso de error

        def guardar(e):
            global df                                                # vamos a cambiar el DataFrame de afuera
            valores = validar(campos)
            if valores is None:                                      # si algo falló, avisa y no guarda
                mensaje.value = "Revisa los campos marcados en rojo."
                page.update()
                return
            nueva = {"Codigo": codigo.value, **valores,              # la fila nueva
                     "Generos": valores["Genero"], "Descripcion": ""}
            df = pd.concat([df, pd.DataFrame([nueva])], ignore_index=True)   # agrega la fila al DataFrame
            df.to_csv(RUTA_DATOS, index=False)                       # guarda el CSV actualizado
            avisar(f"{nueva['Titulo']} guardada como {codigo.value}")
            mostrar_agregar()                                        # formulario vacío con el código siguiente

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
            barra_superior("Agregar película", "Completa los campos y guarda"),
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

    # ---------- Ventana CONSULTAR Y MODIFICAR ----------
    def mostrar_consultar(e=None):
        page.clean()                                                # borra lo que haya en pantalla
        caja_codigo = ft.TextField(label="Código de la película", hint_text="PEL-021", width=240)
        resultado = ft.Column(spacing=18, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)   # aquí sale lo encontrado

        def texto_de(valor):                                         # convierte un dato del df en texto para el campo
            if pd.isna(valor):                                       # dato vacío (NaN) → campo vacío
                return ""
            if isinstance(valor, float) and valor.is_integer():      # 74.0 → "74"
                return str(int(valor))
            return str(valor)

        def no_existe(codigo):                                       # recuadro naranja cuando no se encuentra
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
                            ft.Text(f"No existe una película con el código {codigo}",
                                    size=16, weight=ft.FontWeight.W_500, color="#6E3A0C"),
                            ft.Text("Puedes registrarla ahora mismo.", size=14, color="#6E3A0C"),
                        ]),
                        boton_principal("Agregar esta película", ft.Icons.ADD, mostrar_agregar),
                    ],
                ),
            )

        def formulario_edicion(indice):                              # formulario lleno con los datos de la película
            fila = df.loc[indice]                                    # la fila encontrada
            codigo = ft.TextField(label="Código", value=fila["Codigo"], read_only=True, width=160)
            campos = crear_campos()
            for clave, campo in campos.items():                      # llena cada campo con su valor actual
                campo.value = fila[clave] if isinstance(campo, ft.Dropdown) else texto_de(fila[clave])
            mensaje = ft.Text("", size=15, color="#A32D2D")

            def guardar_cambios(e):
                valores = validar(campos)
                if valores is None:
                    mensaje.value = "Revisa los campos marcados en rojo."
                    page.update()
                    return
                for clave, valor in valores.items():                 # actualiza la fila columna por columna
                    df.loc[indice, clave] = valor
                df.to_csv(RUTA_DATOS, index=False)                   # guarda el CSV actualizado
                mensaje.value = ""
                avisar(f"Cambios guardados en {fila['Codigo']}")
                page.update()

            aviso_ok = ft.Container(                                 # franja verde "encontrada"
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

        def buscar(e):
            texto = caja_codigo.value.strip().upper()                # quita espacios y pasa a mayúsculas
            if texto.isdigit():                                      # si escribió solo "21"…
                texto = "PEL-" + texto.zfill(3)                      # …lo convierte en "PEL-021"
            caja_codigo.value = texto
            resultado.controls.clear()                               # borra el resultado anterior
            encontradas = df.index[df["Codigo"] == texto]            # busca filas con ese código
            if texto == "":
                caja_codigo.error = "Escribe un código"
            elif len(encontradas) == 0:                              # no existe
                caja_codigo.error = None
                resultado.controls.append(no_existe(texto))
            else:                                                    # sí existe
                caja_codigo.error = None
                resultado.controls.extend(formulario_edicion(encontradas[0]))
            page.update()

        caja_codigo.on_submit = buscar                               # Enter en la caja también busca

        page.add(
            barra_superior("Consultar y modificar", "Busca una película por su código"),
            ft.Container(
                padding=28,
                content=ft.Column(
                    spacing=18,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    controls=[
                        ft.Row(spacing=12, wrap=True, vertical_alignment=ft.CrossAxisAlignment.START, controls=[
                            caja_codigo,
                            boton_principal("Buscar", ft.Icons.SEARCH, buscar),
                            ft.Container(padding=ft.Padding.only(top=14),
                                         content=ft.Text("Prueba PEL-021 o PEL-999", size=13, color=GRIS_TEXTO)),
                        ]),
                        resultado,
                    ],
                ),
            ),
        )

    mostrar_inicio()                                                # al abrir la app, muestra el inicio


ft.run(main, assets_dir=str(Path(__file__).parent / "assets"))      # arranca la aplicación y carga las imágenes
