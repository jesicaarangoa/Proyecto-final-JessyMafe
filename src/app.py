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

# ---------- Lógica de los FILTROS (solo Pandas, sin interfaz) ----------
filtrado = df                                                       # último resultado filtrado (lo usarán los gráficos)

def aplicar_filtros(datos, nota_alta=False, cortas=False, populares_largas=False,
                    genero="Todos", desde=None, hasta=None, clasificacion="Todas"):
    resultado = datos                                               # empezamos con todas las películas
    if nota_alta:                                                   # 1. nota mayor al promedio
        resultado = resultado[resultado["Nota"] > datos["Nota"].mean()]
    if cortas:                                                      # 2. películas cortas (menos de 100 min)
        resultado = resultado[resultado["Duracion"] < 100]
    if populares_largas:                                            # 3. popularidad alta y más de 120 min
        resultado = resultado[(resultado["Popularidad"] == "Alta") & (resultado["Duracion"] > 120)]
    if genero != "Todos":                                           # 4. un género específico
        resultado = resultado[resultado["Genero"] == genero]
    if desde is not None:                                           # 5a. desde un año
        resultado = resultado[resultado["Año"] >= desde]
    if hasta is not None:                                           # 5b. hasta un año
        resultado = resultado[resultado["Año"] <= hasta]
    if clasificacion != "Todas":                                    # 6. una clasificación específica
        resultado = resultado[resultado["Clasificacion"] == clasificacion]
    return resultado


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
                tarjeta_opcion(ft.Icons.SEARCH, "Consultar y modificar", "Buscar por nombre o código",
                               mostrar_consultar),
                tarjeta_opcion(ft.Icons.FILTER_ALT_OUTLINED, "Aplicar filtros", "Ver solo las que te interesan",
                               mostrar_filtros),
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
        caja_codigo = ft.TextField(label="Nombre o código de la película", hint_text="Interstellar o PEL-021", width=320)
        resultado = ft.Column(spacing=18, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)   # aquí sale lo encontrado

        def texto_de(valor):                                         # convierte un dato del df en texto para el campo
            if pd.isna(valor):                                       # dato vacío (NaN) → campo vacío
                return ""
            if isinstance(valor, float) and valor.is_integer():      # 74.0 → "74"
                return str(int(valor))
            return str(valor)

        def no_existe(busqueda):                                     # recuadro naranja cuando no se encuentra
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

        def lista_opciones(indices):                                # varias coinciden: lista para elegir una
            def elegir(indice):                                      # al tocar una, muestra su formulario
                resultado.controls.clear()
                resultado.controls.extend(formulario_edicion(indice))
                page.update()

            filas = []
            for i in indices[:10]:                                   # máximo 10 opciones
                f = df.loc[i]
                filas.append(ft.Container(
                    bgcolor=BLANCO, border=ft.Border.all(1, GRIS_BORDE), border_radius=8,
                    padding=ft.Padding.symmetric(vertical=10, horizontal=16), ink=True,
                    on_click=lambda e, i=i: elegir(i),               # i=i: cada opción recuerda SU película
                    content=ft.Row(spacing=12, controls=[
                        ft.Icon(ft.Icons.MOVIE_OUTLINED, color=CAFE, size=20),
                        ft.Text(f["Titulo"], size=15, weight=ft.FontWeight.W_500, color=NEGRO, expand=True),
                        ft.Text(f"{f['Año']} · {f['Codigo']}", size=13, color=GRIS_TEXTO),
                    ]),
                ))
            mas = [ft.Text(f"…y {len(indices) - 10} más. Escribe un nombre más completo.", size=13,
                           color=GRIS_TEXTO)] if len(indices) > 10 else []
            return [ft.Text(f"{len(indices)} películas coinciden. Elige una:", size=16,
                            weight=ft.FontWeight.W_500, color=NEGRO)] + filas + mas

        def buscar(e):
            texto = caja_codigo.value.strip()                        # quita espacios al inicio y al final
            resultado.controls.clear()                               # borra el resultado anterior
            caja_codigo.error = None
            if texto == "":
                caja_codigo.error = "Escribe un nombre o un código"
                page.update()
                return

            if texto.isdigit() or texto.upper().startswith("PEL-"):  # parece un CÓDIGO (21 o PEL-021)
                codigo = "PEL-" + texto.zfill(3) if texto.isdigit() else texto.upper()
                caja_codigo.value = codigo
                encontradas = list(df.index[df["Codigo"] == codigo])
            else:                                                    # si no, busca por NOMBRE
                coincide = df["Titulo"].str.contains(texto, case=False, regex=False)   # sin importar mayúsculas
                encontradas = list(df.index[coincide])

            if len(encontradas) == 0:                                # no existe → ofrecer agregarla
                resultado.controls.append(no_existe(caja_codigo.value))
            elif len(encontradas) == 1:                              # una sola → directo al formulario
                resultado.controls.extend(formulario_edicion(encontradas[0]))
            else:                                                    # varias → lista para elegir
                resultado.controls.extend(lista_opciones(encontradas))
            page.update()

        caja_codigo.on_submit = buscar                               # Enter en la caja también busca

        page.add(
            barra_superior("Consultar y modificar", "Busca una película por su nombre o su código"),
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
                                         content=ft.Text("Prueba: interstellar, lord o 21", size=13, color=GRIS_TEXTO)),
                        ]),
                        resultado,
                    ],
                ),
            ),
        )

    # ---------- Ventana APLICAR FILTROS ----------
    def mostrar_filtros(e=None):
        page.clean()                                                # borra lo que haya en pantalla
        promedio = df["Nota"].mean()                                # promedio actual de las notas

        # --- Controles del panel izquierdo ---
        chk_nota = ft.Checkbox(label=f"Nota mayor al promedio ({promedio:.2f})")
        chk_cortas = ft.Checkbox(label="Cortas (menos de 100 min)")
        chk_populares = ft.Checkbox(label="Popularidad alta y +120 min")
        dd_genero = ft.Dropdown(label="Género", value="Todos", width=270,
                                options=[ft.DropdownOption(g) for g in ["Todos"] + sorted(df["Genero"].unique())])
        txt_desde = ft.TextField(label="Desde (año)", width=127, keyboard_type=ft.KeyboardType.NUMBER)
        txt_hasta = ft.TextField(label="Hasta (año)", width=127, keyboard_type=ft.KeyboardType.NUMBER)
        dd_clasif = ft.Dropdown(label="Clasificación", value="Todas", width=270,
                                options=[ft.DropdownOption(c) for c in ["Todas"] + sorted(df["Clasificacion"].unique())])

        # --- Zona de resultados (derecha) ---
        conteo = ft.Text("", size=18, weight=ft.FontWeight.W_500, color=NEGRO)
        nota_limite = ft.Text("", size=13, color=GRIS_TEXTO)
        tabla = ft.DataTable(
            columns=[ft.DataColumn(ft.Text(t)) for t in
                     ["Código", "Título", "Género", "Nota", "Min", "Popularidad", "Año", "Clasif."]],
            rows=[],
            heading_row_color="#F4F3F0",                            # encabezado gris claro
            border=ft.Border.all(1, GRIS_BORDE),
            border_radius=8,
            column_spacing=18,
            data_row_max_height=56,
        )
        MAX_FILAS = 100                                             # máximo de filas que se dibujan (para que sea rápido)

        def mostrar_resultado(datos):                               # llena la tabla con un DataFrame
            tabla.rows = [
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(f["Codigo"])),
                    ft.DataCell(ft.Container(width=200, content=ft.Text(f["Titulo"], max_lines=2))),   # título en máx. 2 líneas
                    *[ft.DataCell(ft.Text(str(v))) for v in
                      [f["Genero"], f["Nota"], f["Duracion"], f["Popularidad"], f["Año"], f["Clasificacion"]]],
                ])
                for _, f in datos.head(MAX_FILAS).iterrows()       # recorre fila por fila
            ]
            conteo.value = f"{len(datos)} de {len(df)} películas"
            nota_limite.value = (f"Se muestran las primeras {MAX_FILAS}." if len(datos) > MAX_FILAS
                                 else ("Ninguna película cumple esos filtros. Prueba quitando alguno."
                                       if len(datos) == 0 else ""))

        def leer_anio(campo):                                       # lee un año opcional; "error" si es inválido
            campo.error = None
            texto = campo.value.strip()
            if texto == "":
                return None
            if not texto.isdigit():
                campo.error = "Solo números"
                return "error"
            return int(texto)

        def aplicar(e):
            global filtrado                                         # guardamos el resultado para los gráficos
            desde, hasta = leer_anio(txt_desde), leer_anio(txt_hasta)
            if "error" in [desde, hasta]:                           # si un año está mal, no filtra
                page.update()
                return
            filtrado = aplicar_filtros(df, chk_nota.value, chk_cortas.value, chk_populares.value,
                                       dd_genero.value, desde, hasta, dd_clasif.value)
            mostrar_resultado(filtrado)
            page.update()

        def limpiar(e):
            global filtrado
            chk_nota.value = chk_cortas.value = chk_populares.value = False
            dd_genero.value, dd_clasif.value = "Todos", "Todas"
            txt_desde.value = txt_hasta.value = ""
            txt_desde.error = txt_hasta.error = None
            filtrado = df                                           # sin filtros = todas
            mostrar_resultado(df)
            page.update()

        mostrar_resultado(df)                                       # al abrir, muestra todas

        titulo_seccion = lambda t: ft.Text(t, size=13, weight=ft.FontWeight.W_500, color=CAFE)
        panel = ft.Container(                                       # panel izquierdo con los filtros
            width=310,
            bgcolor=BLANCO,
            border=ft.Border.all(1, GRIS_BORDE),
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
        zona_resultados = ft.Container(                             # derecha: conteo + tabla
            expand=True,
            content=ft.Column(spacing=10, controls=[
                conteo,
                nota_limite,
                ft.Row(scroll=ft.ScrollMode.AUTO, controls=[tabla]),   # si la tabla es ancha, se desliza
            ]),
        )

        page.add(
            barra_superior("Aplicar filtros", "Marca los filtros y presiona Aplicar"),
            ft.Container(
                padding=28,
                content=ft.Row(spacing=24, vertical_alignment=ft.CrossAxisAlignment.START,
                               controls=[panel, zona_resultados]),
            ),
        )

    mostrar_inicio()                                                # al abrir la app, muestra el inicio


ft.run(main, assets_dir=str(Path(__file__).parent / "assets"))      # arranca la aplicación y carga las imágenes