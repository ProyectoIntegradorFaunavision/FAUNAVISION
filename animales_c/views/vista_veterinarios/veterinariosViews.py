
import sys
import os
import math
import tkinter as tk
import customtkinter as ctk

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from controllers.veterinariosController import VeterinariosController


class VeterinariosView(ctk.CTk):

    # COLORES
    VERDE_OLIVA = "#95BA00"
    VERDE_OLIVA_HOVER = "#7da000"
    VERDE_HEADER_TABLA = "#C5D88A"
    VERDE_BORDE_TABLA = "#9BB354"
    VERDE_LIMA_BTN = "#A3D900"
    VERDE_LIMA_HOVER = "#8AB800"

    FONDO_BLANCO = "#FFFFFF"
    FONDO_EMERGENTE = "#FFFCF4"
    NEGRO_BORDE = "#1A1A1A"
    T_NEGRO = "#000000"
    GRIS = "#A9A9A9"
    ROJO = "#FF0000"
    ROJO_OSCURO = "#CC0000"

    # FUENTES
    T_TITULO = ("Inder", 28, "bold")
    T_MENU = ("Inder", 12)
    T_CUERPO = ("Poppins", 14)
    T_CUERPO_GRANDE = ("Poppins", 16)
    T_BOTON = ("Poppins", 13, "bold")
    T_EMERGENTE = ("Poppins", 20, "bold")
    T_TABLA = ("Poppins", 13)

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("Light")

        self.title("FAUNAVISION - Veterinarios")
        self.geometry("980x670")
        self.resizable(False, False)
        self.configure(fg_color=self.FONDO_BLANCO)

        self.filas_por_pagina = 15
        self.pagina_actual = 0
        self.registros_filtrados = []
        self.entries = {}

        # Primero se crea el controlador
        self.controlador = VeterinariosController(
            self,
            self.filas_por_pagina
        )

        self.crear_interfaz()

        # Después se cargan los registros
        self.controlador.mostrarController()

    # --------------------------------------------------
    # INTERFAZ PRINCIPAL
    # --------------------------------------------------

    def crear_interfaz(self):

        self.crear_menu_superior()
        self.crear_barra_acciones()
        self.crear_tabla()
        self.crear_paginacion()

    # --------------------------------------------------
    # MENÚ SUPERIOR
    # --------------------------------------------------

    def crear_menu_superior(self):

        menu = ctk.CTkFrame(
            self,
            fg_color=self.FONDO_BLANCO,
            height=70
        )

        menu.pack(
            fill="x",
            padx=30,
            pady=(15, 10)
        )

        menu.pack_propagate(False)

        # Botón regresar
        btn_regresar = ctk.CTkButton(
            menu,
            text="←",
            width=36,
            height=36,
            corner_radius=18,
            fg_color=self.VERDE_OLIVA,
            hover_color=self.VERDE_OLIVA_HOVER,
            text_color=self.T_NEGRO,
            font=("Poppins", 20, "bold"),
            command=self.destroy
        )

        btn_regresar.pack(
            side="left",
            padx=(0, 15),
            pady=15
        )

        # Título
        titulo = ctk.CTkLabel(
            menu,
            text="Veterinarios",
            font=self.T_TITULO,
            text_color=self.T_NEGRO
        )

        titulo.pack(
            side="left",
            pady=15
        )

        # Navegación
        navegacion = ctk.CTkFrame(
            menu,
            fg_color="transparent"
        )

        navegacion.pack(
            side="right",
            pady=18
        )

        botones = [
            ("Menú", self.ir_menu),
            ("Animales", self.ir_animales),
            ("Expedientes", self.ir_expedientes),
            ("Medicamentos", self.ir_medicamentos),
            ("Especies", self.ir_especies)
        ]

        for texto, comando in botones:

            boton = ctk.CTkButton(
                navegacion,
                text=texto,
                width=75,
                height=30,
                corner_radius=15,
                fg_color=self.FONDO_BLANCO,
                hover_color="#E8E8E8",
                text_color=self.T_NEGRO,
                font=self.T_MENU,
                command=comando
            )

            boton.pack(
                side="left",
                padx=2
            )

    # --------------------------------------------------
    # BARRA DE BÚSQUEDA Y ACCIONES
    # --------------------------------------------------

    def crear_barra_acciones(self):

        barra = ctk.CTkFrame(
            self,
            fg_color=self.FONDO_BLANCO
        )

        barra.pack(
            fill="x",
            padx=45,
            pady=(5, 15)
        )

        barra.grid_columnconfigure(0, weight=1)

        # Contenedor del buscador
        buscador = ctk.CTkFrame(
            barra,
            height=42,
            corner_radius=21,
            fg_color=self.FONDO_BLANCO,
            border_width=2,
            border_color=self.NEGRO_BORDE
        )

        buscador.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 10)
        )

        buscador.grid_propagate(False)
        buscador.grid_columnconfigure(0, weight=1)

        self.txt_buscar = ctk.CTkEntry(
            buscador,
            placeholder_text="Buscar por nombre, apellido o número de empleado",
            placeholder_text_color=self.GRIS,
            border_width=0,
            fg_color="transparent",
            text_color=self.T_NEGRO,
            font=("Poppins", 12),
            height=35
        )

        self.txt_buscar.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(15, 0),
            pady=2
        )

        self.txt_buscar.bind(
            "<Return>",
            lambda event: self.buscar()
        )

        btn_buscar = ctk.CTkButton(
            buscador,
            text="⌕",
            width=38,
            height=35,
            corner_radius=18,
            fg_color="transparent",
            hover_color="#E8E8E8",
            text_color=self.T_NEGRO,
            font=("Poppins", 22),
            command=self.buscar
        )

        btn_buscar.grid(
            row=0,
            column=1,
            padx=(0, 5),
            pady=2
        )

        # Botón limpiar búsqueda
        btn_limpiar = ctk.CTkButton(
            barra,
            text="↻",
            width=42,
            height=42,
            corner_radius=21,
            fg_color=self.VERDE_HEADER_TABLA,
            hover_color=self.VERDE_BORDE_TABLA,
            text_color=self.T_NEGRO,
            font=("Poppins", 18, "bold"),
            command=self.limpiar_busqueda
        )

        btn_limpiar.grid(
            row=0,
            column=1,
            padx=(0, 10)
        )

        # Botón añadir
        btn_anadir = ctk.CTkButton(
            barra,
            text="+ Añadir Veterinario",
            width=180,
            height=42,
            corner_radius=21,
            fg_color=self.VERDE_LIMA_BTN,
            hover_color=self.VERDE_LIMA_HOVER,
            text_color=self.T_NEGRO,
            font=self.T_BOTON,
            command=self.ventana_anadir
        )

        btn_anadir.grid(
            row=0,
            column=2
        )

    # --------------------------------------------------
    # TABLA
    # --------------------------------------------------

    def crear_tabla(self):

        contenedor = ctk.CTkFrame(
            self,
            fg_color=self.FONDO_BLANCO
        )

        contenedor.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 5)
        )

        # Marco exterior de la tabla
        self.marco_tabla = tk.Frame(
            contenedor,
            bg=self.VERDE_BORDE_TABLA,
            highlightbackground=self.VERDE_BORDE_TABLA,
            highlightthickness=2
        )

        self.marco_tabla.pack(
            fill="both",
            expand=True
        )

        # Columnas
        self.columnas = [
            ("N°", 5),
            ("Num. empleado", 13),
            ("Nombre", 16),
            ("Apellido paterno", 17),
            ("Apellido materno", 17),
            ("Cargo", 15),
            ("Acciones", 17)
        ]

        self.pesos_columnas = [1, 2, 3, 3, 3, 2, 3]

        # Encabezado
        encabezado = tk.Frame(
            self.marco_tabla,
            bg=self.VERDE_HEADER_TABLA,
            height=40
        )

        encabezado.pack(
            fill="x"
        )

        encabezado.pack_propagate(False)

        for i, (texto, ancho) in enumerate(self.columnas):

            encabezado.grid_columnconfigure(
                i,
                weight=self.pesos_columnas[i]
            )

            etiqueta = tk.Label(
                encabezado,
                text=texto,
                bg=self.VERDE_HEADER_TABLA,
                fg=self.T_NEGRO,
                font=("Poppins", 11, "bold"),
                anchor="center"
            )

            etiqueta.grid(
                row=0,
                column=i,
                sticky="nsew",
                padx=2
            )

        # Cuerpo de la tabla
        self.cuerpo_tabla = tk.Frame(
            self.marco_tabla,
            bg=self.VERDE_BORDE_TABLA
        )

        self.cuerpo_tabla.pack(
            fill="both",
            expand=True
        )

        for i, peso in enumerate(self.pesos_columnas):

            self.cuerpo_tabla.grid_columnconfigure(
                i,
                weight=peso
            )

    def renderizar_tabla(self):

        # Limpiar filas anteriores
        for widget in self.cuerpo_tabla.winfo_children():
            widget.destroy()

        inicio = self.pagina_actual * self.filas_por_pagina
        fin = inicio + self.filas_por_pagina

        registros = self.registros_filtrados[inicio:fin]

        # Crear las 15 filas
        for numero_fila in range(self.filas_por_pagina):

            fila = tk.Frame(
                self.cuerpo_tabla,
                bg=self.FONDO_BLANCO,
                height=34
            )

            fila.grid(
                row=numero_fila,
                column=0,
                columnspan=len(self.columnas),
                sticky="nsew",
                pady=1
            )

            fila.grid_propagate(False)

            for i, peso in enumerate(self.pesos_columnas):
                fila.grid_columnconfigure(
                    i,
                    weight=peso
                )

            if numero_fila < len(registros):

                veterinario = registros[numero_fila]

                datos = [
                    str(inicio + numero_fila + 1),
                    str(veterinario[0]),
                    str(veterinario[1]),
                    str(veterinario[2]),
                    str(veterinario[3]),
                    str(veterinario[4])
                ]

                for columna, dato in enumerate(datos):

                    etiqueta = tk.Label(
                        fila,
                        text=dato,
                        bg=self.FONDO_BLANCO,
                        fg=self.T_NEGRO,
                        font=self.T_TABLA,
                        anchor="center"
                    )

                    etiqueta.grid(
                        row=0,
                        column=columna,
                        sticky="nsew",
                        padx=2
                    )

                # Botones de acciones
                acciones = tk.Frame(
                    fila,
                    bg=self.FONDO_BLANCO
                )

                acciones.grid(
                    row=0,
                    column=6,
                    sticky="nsew"
                )

                btn_ver = tk.Button(
                    acciones,
                    text="👁",
                    font=("Arial", 12),
                    bg=self.FONDO_BLANCO,
                    fg=self.T_NEGRO,
                    relief="flat",
                    cursor="hand2",
                    command=lambda v=veterinario: self.ventana_ver(v)
                )

                btn_ver.pack(
                    side="left",
                    expand=True
                )

                btn_editar = tk.Button(
                    acciones,
                    text="✏",
                    font=("Arial", 12),
                    bg=self.FONDO_BLANCO,
                    fg=self.T_NEGRO,
                    relief="flat",
                    cursor="hand2",
                    command=lambda v=veterinario: self.ventana_editar(v)
                )

                btn_editar.pack(
                    side="left",
                    expand=True
                )

                btn_eliminar = tk.Button(
                    acciones,
                    text="🗑",
                    font=("Arial", 12),
                    bg=self.FONDO_BLANCO,
                    fg=self.ROJO,
                    relief="flat",
                    cursor="hand2",
                    command=lambda v=veterinario: self.ventana_eliminar(v)
                )

                btn_eliminar.pack(
                    side="left",
                    expand=True
                )

            else:

                # Fila vacía para conservar el diseño
                for columna in range(len(self.columnas)):

                    espacio = tk.Label(
                        fila,
                        text="",
                        bg=self.FONDO_BLANCO
                    )

                    espacio.grid(
                        row=0,
                        column=columna,
                        sticky="nsew"
                    )

        self.actualizar_paginacion()

    # --------------------------------------------------
    # PAGINACIÓN
    # --------------------------------------------------

    def crear_paginacion(self):

        self.marco_paginacion = ctk.CTkFrame(
            self,
            fg_color=self.FONDO_BLANCO,
            height=48
        )

        self.marco_paginacion.pack(
            fill="x",
            padx=35,
            pady=(5, 12)
        )

        self.marco_paginacion.pack_propagate(False)

        self.actualizar_paginacion()

    def actualizar_paginacion(self):

        if not hasattr(self, "marco_paginacion"):
            return

        for widget in self.marco_paginacion.winfo_children():
            widget.destroy()

        total_registros = len(self.registros_filtrados)

        total_paginas = max(
            1,
            math.ceil(total_registros / self.filas_por_pagina)
        )

        self.pagina_actual = max(
            0,
            min(self.pagina_actual, total_paginas - 1)
        )

        # Botón anterior
        btn_anterior = ctk.CTkButton(
            self.marco_paginacion,
            text="‹",
            width=32,
            height=30,
            corner_radius=15,
            fg_color=self.VERDE_HEADER_TABLA,
            hover_color=self.VERDE_BORDE_TABLA,
            text_color=self.T_NEGRO,
            font=("Poppins", 18, "bold"),
            command=self.pagina_anterior
        )

        btn_anterior.pack(
            side="left",
            padx=(5, 10),
            pady=5
        )

        # Números de página
        for numero in range(total_paginas):

            if total_paginas > 5:

                if numero not in [
                    0,
                    total_paginas - 1,
                    self.pagina_actual,
                    self.pagina_actual - 1,
                    self.pagina_actual + 1
                ]:
                    continue

            numero_visible = numero + 1

            if numero == self.pagina_actual:
                color = self.VERDE_OLIVA
                hover = self.VERDE_OLIVA_HOVER
            else:
                color = self.FONDO_BLANCO
                hover = "#E8E8E8"

            boton = ctk.CTkButton(
                self.marco_paginacion,
                text=str(numero_visible),
                width=30,
                height=30,
                corner_radius=15,
                fg_color=color,
                hover_color=hover,
                text_color=self.T_NEGRO,
                font=("Poppins", 12, "bold"),
                command=lambda p=numero: self.ir_a_pagina(p)
            )

            boton.pack(
                side="left",
                padx=3,
                pady=5
            )

        # Botón siguiente
        btn_siguiente = ctk.CTkButton(
            self.marco_paginacion,
            text="›",
            width=32,
            height=30,
            corner_radius=15,
            fg_color=self.VERDE_HEADER_TABLA,
            hover_color=self.VERDE_BORDE_TABLA,
            text_color=self.T_NEGRO,
            font=("Poppins", 18, "bold"),
            command=self.pagina_siguiente
        )

        btn_siguiente.pack(
            side="left",
            padx=(10, 5),
            pady=5
        )

    def ir_a_pagina(self, pagina):

        total_paginas = max(
            1,
            math.ceil(
                len(self.registros_filtrados) / self.filas_por_pagina
            )
        )

        if 0 <= pagina < total_paginas:

            self.pagina_actual = pagina
            self.controlador.pagina_actual = pagina

            self.renderizar_tabla()

    def pagina_anterior(self):

        if self.pagina_actual > 0:

            self.ir_a_pagina(
                self.pagina_actual - 1
            )

    def pagina_siguiente(self):

        total_paginas = max(
            1,
            math.ceil(
                len(self.registros_filtrados) / self.filas_por_pagina
            )
        )

        if self.pagina_actual < total_paginas - 1:

            self.ir_a_pagina(
                self.pagina_actual + 1
            )

    # --------------------------------------------------
    # BÚSQUEDA
    # --------------------------------------------------

    def buscar(self):

        criterio = self.txt_buscar.get().strip()

        self.controlador.buscarController(criterio)

    def limpiar_busqueda(self):

        self.txt_buscar.delete(0, "end")

        self.controlador.mostrarController()

    # --------------------------------------------------
    # VENTANAS EMERGENTES
    # --------------------------------------------------

    def ventana_emergente(self, titulo, ancho, alto):

        ventana = ctk.CTkToplevel(self)

        ventana.title(titulo)
        ventana.geometry(f"{ancho}x{alto}")
        ventana.resizable(False, False)
        ventana.configure(fg_color=self.FONDO_EMERGENTE)

        ventana.transient(self)
        ventana.grab_set()

        # Centrar ventana
        self.update_idletasks()

        x = self.winfo_x() + (self.winfo_width() // 2) - (ancho // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (alto // 2)

        ventana.geometry(f"+{x}+{y}")

        return ventana

    def crear_titulo_emergente(self, ventana, titulo):

        etiqueta = ctk.CTkLabel(
            ventana,
            text=titulo,
            font=self.T_EMERGENTE,
            text_color=self.T_NEGRO
        )

        etiqueta.pack(
            pady=(20, 15)
        )

    # --------------------------------------------------
    # CAMPOS DEL FORMULARIO
    # --------------------------------------------------

    def crear_campos(self, contenedor, valores=None, solo_lectura=False):

        if valores is None:
            valores = [""] * 11

        campos = [
            ("Número de empleado", "num_empleado"),
            ("Nombre", "nombre"),
            ("Apellido paterno", "apellido1"),
            ("Apellido materno", "apellido2"),
            ("Cargo", "cargo"),
            ("Calle", "calle"),
            ("Colonia", "col"),
            ("Número de domicilio", "num"),
            ("Código postal", "codigo_postal"),
            ("Teléfono", "telefono"),
            ("Correo electrónico", "correo")
        ]

        self.entries = {}

        formulario = ctk.CTkFrame(
            contenedor,
            fg_color="transparent"
        )

        formulario.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=5
        )

        formulario.grid_columnconfigure(0, weight=1)
        formulario.grid_columnconfigure(1, weight=1)

        for i, (texto, atributo) in enumerate(campos):

            columna = i % 2
            fila = i // 2

            grupo = ctk.CTkFrame(
                formulario,
                fg_color="transparent"
            )

            grupo.grid(
                row=fila,
                column=columna,
                sticky="ew",
                padx=8,
                pady=5
            )

            etiqueta = ctk.CTkLabel(
                grupo,
                text=texto,
                font=("Poppins", 12, "bold"),
                text_color=self.T_NEGRO,
                anchor="w"
            )

            etiqueta.pack(
                fill="x",
                pady=(0, 3)
            )

            entrada = ctk.CTkEntry(
                grupo,
                height=34,
                corner_radius=8,
                border_color=self.VERDE_BORDE_TABLA,
                fg_color=self.FONDO_BLANCO,
                text_color=self.T_NEGRO,
                font=("Poppins", 12)
            )

            entrada.pack(fill="x")

            entrada.insert(
                0,
                str(valores[i]) if valores[i] is not None else ""
            )

            if solo_lectura:
                entrada.configure(state="disabled")

            self.entries[atributo] = entrada

            # El controlador utiliza estos atributos
            setattr(self, atributo, entrada)

        return formulario

    def limpiar_campos_anadir(self):

        for entrada in self.entries.values():

            entrada.configure(state="normal")
            entrada.delete(0, "end")

    # --------------------------------------------------
    # AÑADIR VETERINARIO
    # --------------------------------------------------

    def ventana_anadir(self):

        ventana = self.ventana_emergente(
            "Añadir veterinario",
            650,
            650
        )

        self.crear_titulo_emergente(
            ventana,
            "Registrar nuevo veterinario"
        )

        self.crear_campos(ventana)

        botones = ctk.CTkFrame(
            ventana,
            fg_color="transparent"
        )

        botones.pack(
            fill="x",
            padx=35,
            pady=15
        )

        btn_guardar = ctk.CTkButton(
            botones,
            text="Guardar",
            width=150,
            height=38,
            corner_radius=19,
            fg_color=self.VERDE_LIMA_BTN,
            hover_color=self.VERDE_LIMA_HOVER,
            text_color=self.T_NEGRO,
            font=self.T_BOTON,
            command=self.controlador.insertarController
        )

        btn_guardar.pack(
            side="left",
            expand=True,
            padx=10
        )

        btn_cancelar = ctk.CTkButton(
            botones,
            text="Cancelar",
            width=150,
            height=38,
            corner_radius=19,
            fg_color="#D9D9D9",
            hover_color="#BFBFBF",
            text_color=self.T_NEGRO,
            font=self.T_BOTON,
            command=ventana.destroy
        )

        btn_cancelar.pack(
            side="left",
            expand=True,
            padx=10
        )

    # --------------------------------------------------
    # VER VETERINARIO
    # --------------------------------------------------

    def ventana_ver(self, veterinario):

        ventana = self.ventana_emergente(
            "Consultar veterinario",
            650,
            650
        )

        self.crear_titulo_emergente(
            ventana,
            "Información del veterinario"
        )

        self.crear_campos(
            ventana,
            veterinario[:11],
            solo_lectura=True
        )

        btn_cerrar = ctk.CTkButton(
            ventana,
            text="Cerrar",
            width=150,
            height=38,
            corner_radius=19,
            fg_color=self.VERDE_OLIVA,
            hover_color=self.VERDE_OLIVA_HOVER,
            text_color=self.T_NEGRO,
            font=self.T_BOTON,
            command=ventana.destroy
        )

        btn_cerrar.pack(
            pady=15
        )

    # --------------------------------------------------
    # MODIFICAR VETERINARIO
    # --------------------------------------------------

    def ventana_editar(self, veterinario):

        ventana = self.ventana_emergente(
            "Modificar veterinario",
            650,
            650
        )

        self.crear_titulo_emergente(
            ventana,
            "Modificar información"
        )

        self.crear_campos(
            ventana,
            veterinario[:11]
        )

        # El número de empleado es la clave primaria
        self.num_empleado.configure(
            state="disabled"
        )

        botones = ctk.CTkFrame(
            ventana,
            fg_color="transparent"
        )

        botones.pack(
            fill="x",
            padx=35,
            pady=15
        )

        def guardar():

            self.num_empleado.configure(
                state="normal"
            )

            self.controlador.modificarController()

            self.num_empleado.configure(
                state="disabled"
            )

        btn_guardar = ctk.CTkButton(
            botones,
            text="Guardar cambios",
            width=170,
            height=38,
            corner_radius=19,
            fg_color=self.VERDE_LIMA_BTN,
            hover_color=self.VERDE_LIMA_HOVER,
            text_color=self.T_NEGRO,
            font=self.T_BOTON,
            command=guardar
        )

        btn_guardar.pack(
            side="left",
            expand=True,
            padx=10
        )

        btn_cancelar = ctk.CTkButton(
            botones,
            text="Cancelar",
            width=150,
            height=38,
            corner_radius=19,
            fg_color="#D9D9D9",
            hover_color="#BFBFBF",
            text_color=self.T_NEGRO,
            font=self.T_BOTON,
            command=ventana.destroy
        )

        btn_cancelar.pack(
            side="left",
            expand=True,
            padx=10
        )

    # --------------------------------------------------
    # ELIMINAR VETERINARIO
    # --------------------------------------------------

    def ventana_eliminar(self, veterinario):

        ventana = self.ventana_emergente(
            "Eliminar veterinario",
            400,
            230
        )

        self.crear_titulo_emergente(
            ventana,
            "Eliminar registro"
        )

        mensaje = ctk.CTkLabel(
            ventana,
            text=(
                "¿Está seguro de eliminar al veterinario?\n\n"
                f"{veterinario[1]} {veterinario[2]} {veterinario[3]}"
            ),
            font=self.T_CUERPO,
            text_color=self.T_NEGRO
        )

        mensaje.pack(
            pady=10
        )

        botones = ctk.CTkFrame(
            ventana,
            fg_color="transparent"
        )

        botones.pack(
            fill="x",
            padx=25,
            pady=15
        )

        def eliminar():

            self.controlador.eliminarController(
                veterinario[0]
            )

            ventana.destroy()

        btn_eliminar = ctk.CTkButton(
            botones,
            text="Eliminar",
            width=130,
            height=38,
            corner_radius=19,
            fg_color=self.ROJO,
            hover_color=self.ROJO_OSCURO,
            text_color="#FFFFFF",
            font=self.T_BOTON,
            command=eliminar
        )

        btn_eliminar.pack(
            side="left",
            expand=True,
            padx=5
        )

        btn_cancelar = ctk.CTkButton(
            botones,
            text="Cancelar",
            width=130,
            height=38,
            corner_radius=19,
            fg_color="#D9D9D9",
            hover_color="#BFBFBF",
            text_color=self.T_NEGRO,
            font=self.T_BOTON,
            command=ventana.destroy
        )

        btn_cancelar.pack(
            side="left",
            expand=True,
            padx=5
        )

    # --------------------------------------------------
    # NAVEGACIÓN
    # --------------------------------------------------

    def ir_menu(self):
        print("Regresando al menú principal...")

    def ir_animales(self):
        print("Abriendo Animales en Cautiverio...")

    def ir_expedientes(self):
        print("Abriendo Expedientes...")

    def ir_medicamentos(self):
        print("Abriendo Medicamentos...")

    def ir_especies(self):
        print("Abriendo Especies...")


# --------------------------------------------------
# EJECUTAR VISTA
# --------------------------------------------------

if __name__ == "__main__":

    app = VeterinariosView()
    app.mainloop()
