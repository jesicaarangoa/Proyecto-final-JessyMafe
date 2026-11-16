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

    # ---------- Ventana AGREGAR PELÍCULA ----------
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

    def mostrar_agregar(e=None):
        page.clean()                                                # borra lo que haya en pantalla
        siguiente_codigo = "PEL-" + str(len(df) + 1).zfill(3)       # ej. PEL-399

        # --- Campos del formulario ---
        codigo = ft.TextField(label="Código", value=siguiente_codigo, read_only=True, width=160)   # no se edita
        titulo = ft.TextField(label="Título", width=300)
        genero = ft.Dropdown(label="Género principal", width=220,
                             options=[ft.DropdownOption(g) for g in sorted(df["Genero"].unique())])  # géneros del dataset
        director = ft.TextField(label="Director", width=260)
        nota = ft.TextField(label="Nota IMDb (0 a 10)", width=200, keyboard_type=ft.KeyboardType.NUMBER)
        duracion = ft.TextField(label="Duración (min)", width=170, keyboard_type=ft.KeyboardType.NUMBER)
        anio = ft.TextField(label="Año", width=130, keyboard_type=ft.KeyboardType.NUMBER)
        clasificacion = ft.Dropdown(label="Clasificación", width=170,
                                    options=[ft.DropdownOption(c) for c in ["G", "PG", "PG-13", "R", "Not Rated", "Sin dato"]])
        metascore = ft.TextField(label="Metascore (opcional)", width=220, keyboard_type=ft.KeyboardType.NUMBER)
        votos = ft.TextField(label="Votos", width=170, keyboard_type=ft.KeyboardType.NUMBER)
        recaudacion = ft.TextField(label="Recaudación en millones USD (opcional)", width=360,
                                   keyboard_type=ft.KeyboardType.NUMBER)
        popularidad = ft.Dropdown(label="Popularidad", width=170,
                                  options=[ft.DropdownOption(p) for p in ["Alta", "Media", "Baja"]])
        mensaje = ft.Text("", size=15)                              # aquí aparece "guardada" o el error

        campos_texto = [titulo, director, nota, duracion, anio, metascore, votos, recaudacion]
        listas = [genero, clasificacion, popularidad]

        # --- Validar un número ---
        def leer_numero(campo, minimo, maximo, entero=False, opcional=False):
            texto = campo.value.strip().replace(",", ".")            # acepta 8,5 o 8.5
            if texto == "":                                          # si está vacío…
                if opcional:                                         # …y es opcional → sin dato
                    return None
                campo.error = "Campo obligatorio"                    # …y es obligatorio → error
                return "error"
            try:
                valor = int(texto) if entero else float(texto)       # intenta convertirlo en número
            except ValueError:                                       # si no es número…
                campo.error = "Solo enteros" if entero else "Solo números"
                return "error"
            if not (minimo <= valor <= maximo):                      # fuera de rango
                campo.error = f"Entre {minimo} y {maximo}"
                return "error"
            return valor

        # --- Botón GUARDAR ---
        def guardar(e):
            global df                                                # vamos a cambiar el DataFrame de afuera
            for c in campos_texto:                                   # borra los errores anteriores
                c.error = None
            for l in listas:
                l.error_text = None
            hay_error = False

            for c in [titulo, director]:                             # campos de texto obligatorios
                if c.value.strip() == "":
                    c.error = "Campo obligatorio"
                    hay_error = True
            for l in listas:                                         # listas obligatorias
                if l.value is None:
                    l.error_text = "Elige una opción"
                    hay_error = True

            v_nota = leer_numero(nota, 0, 10)
            v_duracion = leer_numero(duracion, 1, 600, entero=True)
            v_anio = leer_numero(anio, 1888, 2030, entero=True)
            v_meta = leer_numero(metascore, 0, 100, opcional=True)
            v_votos = leer_numero(votos, 0, 10_000_000, entero=True)
            v_recaudacion = leer_numero(recaudacion, 0, 10_000, opcional=True)
            if "error" in [v_nota, v_duracion, v_anio, v_meta, v_votos, v_recaudacion]:
                hay_error = True

            if hay_error:                                            # si algo falló, avisa y no guarda
                mensaje.value = "Revisa los campos marcados en rojo."
                mensaje.color = "#A32D2D"
                page.update()
                return

            nueva = {                                                # la fila nueva, con las columnas del CSV
                "Codigo": codigo.value, "Titulo": titulo.value.strip(), "Genero": genero.value,
                "Nota": v_nota, "Duracion": v_duracion, "Director": director.value.strip(),
                "Popularidad": popularidad.value, "Año": v_anio, "Clasificacion": clasificacion.value,
                "Metascore": v_meta, "Recaudacion": v_recaudacion, "Votos": v_votos,
                "Generos": genero.value, "Descripcion": "",
            }
            df = pd.concat([df, pd.DataFrame([nueva])], ignore_index=True)   # agrega la fila al DataFrame
            df.to_csv(RUTA_DATOS, index=False)                       # guarda el CSV actualizado

            page.show_dialog(ft.SnackBar(ft.Text(f"{nueva['Titulo']} guardada como {codigo.value}")))
            mostrar_agregar()                                        # recarga el formulario vacío con el código siguiente

        # --- Botón LIMPIAR ---
        def limpiar(e):
            for c in campos_texto:
                c.value = ""
                c.error = None
            for l in listas:
                l.value = None
                l.error_text = None
            mensaje.value = ""
            page.update()

        page.add(
            barra_superior("Agregar película", "Completa los campos y guarda"),
            ft.Container(
                padding=28,
                content=ft.Column(
                    spacing=18,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    controls=[
                        grupo("Datos principales", [codigo, titulo, genero, director]),
                        grupo("Calificación y duración", [nota, duracion, anio, clasificacion, metascore]),
                        grupo("Público y taquilla", [votos, recaudacion, popularidad]),
                        ft.Row(spacing=12, wrap=True, controls=[
                            ft.FilledButton("Guardar película", icon=ft.Icons.SAVE_OUTLINED,
                                            style=ft.ButtonStyle(bgcolor=NEGRO, color=BLANCO),
                                            on_click=guardar),
                            ft.OutlinedButton("Limpiar campos", on_click=limpiar),
                            mensaje,
                        ]),
                    ],
                ),
            ),
        )

    mostrar_inicio()                                                # al abrir la app, muestra el inicio


ft.run(main, assets_dir=str(Path(__file__).parent / "assets"))      # arranca la aplicación y carga las imágenes