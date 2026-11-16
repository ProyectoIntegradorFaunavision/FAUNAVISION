
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk

from Veterinarios import Veterinarios


# COLORES
VERDE_OLIVA = "#84A91C"
VERDE_OLIVA_HOVER = "#6E8E14"
VERDE_HEADER_TABLA = "#C5D88A"
VERDE_BORDE_TABLA = "#9BB354"

VERDE_LIMA_BTN = "#A3D900"
VERDE_LIMA_HOVER = "#8AB800"

FONDO_BLANCO = "#FFFFFF"
FONDO_CREMA_MODAL = "#FBF8F1"

BORDE_CAFE_OSCURO = "#3B2618"

ROJO_PILDORA = "#FF0000"
ROJO_OSCURO = "#CC0000"

NEGRO_BORDE = "#1A1A1A"


ctk.set_appearance_mode("Light")


class VistaVeterinarios(ctk.CTkFrame):

    def __init__(self, master, volver_menu=None):
        super().__init__(master, fg_color=FONDO_BLANCO)

        self.master = master
        self.volver_menu = volver_menu

        self.filas_por_pagina = 8
        self.pagina_actual = 1

        self.datos = []

        self.pack(fill="both", expand=True)

        self.crear_interfaz()
        self.cargar_datos()

    # --------------------------------------------------
    # VENTANA PRINCIPAL
    # --------------------------------------------------

    def crear_interfaz(self):
        encabezado = ctk.CTkFrame(
            self,
            fg_color=FONDO_BLANCO,
            height=75
        )
        encabezado.pack(fill="x", padx=15, pady=(10, 0))
        encabezado.pack_propagate(False)
        encabezado.grid_columnconfigure(2, weight=1)
        btn_volver = ctk.CTkButton(
            encabezado,
            text="↶",
            width=35,
            height=35,
            corner_radius=20,
            fg_color=VERDE_OLIVA,
            hover_color=VERDE_OLIVA_HOVER,
            font=("Arial", 20),
            command=self.volver
        )
        btn_volver.grid(row=0, column=0, padx=(0, 8), pady=15)
        titulo = ctk.CTkLabel(
            encabezado,
            text="Veterinarios",
            font=("Arial", 23, "bold"),
            text_color="black"
        )
        titulo.grid(row=0, column=1, padx=5)

        navegacion = ctk.CTkFrame(
            encabezado,
            fg_color="transparent"
        )
        navegacion.grid(row=0, column=2, padx=5)
        enlaces = [
            "Menú",
            "Especies",
            "Medicamentos",
            "Expediente",
            "Animales"
        ]
        for texto in enlaces:
            etiqueta = ctk.CTkLabel(
                navegacion,
                text=texto,
                font=("Arial", 10),
                text_color="black",
                cursor="hand2"
            )
            etiqueta.pack(side="left", padx=5)
        logo = ctk.CTkLabel(
            encabezado,
            text="EL TECUÁN",
            font=("Arial", 13, "bold"),
            text_color=VERDE_OLIVA
        )
        logo.grid(row=0, column=3, padx=(8, 0))
        barra = ctk.CTkFrame(
            self,
            fg_color=FONDO_BLANCO
        )
        barra.pack(fill="x", padx=25, pady=(10, 15))
        self.buscar = ctk.CTkEntry(
            barra,
            placeholder_text="Buscar",
            height=35,
            corner_radius=18,
            border_color=VERDE_BORDE_TABLA,
            text_color="black"
        )
        self.buscar.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        self.buscar.bind(
            "<KeyRelease>",
            lambda evento: self.filtrar_tabla()
        )

        btn_agregar = ctk.CTkButton(
            barra,
            text="Añadir Veterinario",
            height=35,
            corner_radius=18,
            fg_color=VERDE_OLIVA,
            hover_color=VERDE_OLIVA_HOVER,
            font=("Arial", 12, "bold"),
            command=self.abrir_modal_agregar
        )
        btn_agregar.pack(side="right")

        # TABLA
        contenedor_tabla = ctk.CTkFrame(
            self,
            fg_color=FONDO_BLANCO
        )
        contenedor_tabla.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 5)
        )

        columnas = (
            "numero",
            "empleado",
            "nombre",
            "apellido1",
            "apellido2",
            "cargo",
            "acciones"
        )

        self.tabla = ttk.Treeview(
            contenedor_tabla,
            columns=columnas,
            show="headings",
            height=8
        )

        encabezados = [
            ("numero", "N°", 35),
            ("empleado", "Empleado", 75),
            ("nombre", "Nombre", 100),
            ("apellido1", "Primer Apellido", 110),
            ("apellido2", "Segundo Apellido", 110),
            ("cargo", "Cargo", 95),
            ("acciones", "Acciones", 80)
        ]

        for columna, texto, ancho in encabezados:

            self.tabla.heading(
                columna,
                text=texto,
                anchor="center"
            )

            self.tabla.column(
                columna,
                width=ancho,
                anchor="center"
            )

        estilo = ttk.Style()

        estilo.theme_use("default")

        estilo.configure(
            "Treeview",
            background="white",
            foreground="black",
            rowheight=39,
            fieldbackground="white",
            font=("Arial", 9)
        )

        estilo.configure(
            "Treeview.Heading",
            background=VERDE_HEADER_TABLA,
            foreground="black",
            font=("Arial", 9, "bold"),
            relief="flat"
        )

        estilo.map(
            "Treeview",
            background=[("selected", "#E5EDCC")],
            foreground=[("selected", "black")]
        )

        self.tabla.tag_configure(
            "fila",
            background="white"
        )

        self.tabla.pack(
            fill="both",
            expand=True
        )

        self.tabla.bind(
            "<Double-1>",
            self.abrir_desde_tabla
        )

        # PAGINACION
        self.paginacion = ctk.CTkFrame(
            self,
            fg_color=FONDO_BLANCO
        )
        self.paginacion.pack(pady=(5, 10))

        self.botones_paginas = []

        for numero in range(1, 4):

            boton = ctk.CTkButton(
                self.paginacion,
                text=str(numero),
                width=30,
                height=30,
                corner_radius=20,
                fg_color="#D9D9D9",
                hover_color=VERDE_OLIVA,
                text_color="black",
                command=lambda p=numero: self.cambiar_pagina(p)
            )

            boton.pack(side="left", padx=5)

            self.botones_paginas.append(boton)

    # --------------------------------------------------
    # CARGAR Y MOSTRAR DATOS
    # --------------------------------------------------

    def cargar_datos(self):

        self.datos = Veterinarios.mostrar()

        if self.datos is None:
            self.datos = []

        self.pagina_actual = 1

        self.renderizar_tabla()

    def renderizar_tabla(self):

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        inicio = (self.pagina_actual - 1) * self.filas_por_pagina
        final = inicio + self.filas_por_pagina

        datos_pagina = self.datos[inicio:final]

        for indice, vet in enumerate(datos_pagina, start=inicio + 1):

            self.tabla.insert(
                "",
                "end",
                values=(
                    indice,
                    vet[0],
                    vet[1],
                    vet[2],
                    vet[3],
                    vet[4],
                    "Ver más"
                ),
                tags=("fila",)
            )

        self.actualizar_paginacion()

    def actualizar_paginacion(self):

        total_paginas = max(
            1,
            (len(self.datos) + self.filas_por_pagina - 1)
            // self.filas_por_pagina
        )

        for indice, boton in enumerate(self.botones_paginas, start=1):

            if indice <= total_paginas:

                boton.pack(side="left", padx=5)

                if indice == self.pagina_actual:
                    boton.configure(
                        fg_color=VERDE_OLIVA,
                        text_color="white"
                    )
                else:
                    boton.configure(
                        fg_color="#D9D9D9",
                        text_color="black"
                    )

            else:
                boton.pack_forget()

    def cambiar_pagina(self, pagina):

        total_paginas = max(
            1,
            (len(self.datos) + self.filas_por_pagina - 1)
            // self.filas_por_pagina
        )

        if 1 <= pagina <= total_paginas:
            self.pagina_actual = pagina
            self.renderizar_tabla()

    def filtrar_tabla(self):

        criterio = self.buscar.get().strip()

        if criterio:
            self.datos = Veterinarios.filtrar(criterio)
        else:
            self.datos = Veterinarios.mostrar()

        if self.datos is None:
            self.datos = []

        self.pagina_actual = 1
        self.renderizar_tabla()

    def abrir_desde_tabla(self, evento):

        seleccion = self.tabla.selection()

        if not seleccion:
            return

        columna = self.tabla.identify_column(evento.x)

        if columna != "#7":
            return

        valores = self.tabla.item(seleccion[0], "values")

        if valores:
            veterinario = Veterinarios.buscar(str(valores[1]))

            if veterinario:
                self.abrir_modal_detalle(veterinario)

    # --------------------------------------------------
    # VENTANAS EMERGENTES
    # --------------------------------------------------

    def crear_ventana_modal(self, ancho, alto):

        ventana = ctk.CTkToplevel(self)

        ventana.title("Veterinarios")
        ventana.geometry(f"{ancho}x{alto}")
        ventana.resizable(False, False)
        ventana.configure(fg_color=FONDO_CREMA_MODAL)

        ventana.transient(self.winfo_toplevel())

        ventana.update_idletasks()

        x = (
            ventana.winfo_screenwidth() // 2
            - ancho // 2
        )

        y = (
            ventana.winfo_screenheight() // 2
            - alto // 2
        )

        ventana.geometry(f"+{x}+{y}")

        ventana.grab_set()

        return ventana

    def mostrar_alerta(
        self,
        padre,
        mensaje,
        tipo="info",
        al_aceptar=None
    ):

        alerta = ctk.CTkToplevel(padre)

        alerta.title("Mensaje")
        alerta.geometry("350x175")
        alerta.resizable(False, False)
        alerta.configure(fg_color=FONDO_BLANCO)

        alerta.transient(padre)
        alerta.grab_set()

        alerta.update_idletasks()

        x = (
            alerta.winfo_screenwidth() // 2
            - 175
        )

        y = (
            alerta.winfo_screenheight() // 2
            - 87
        )

        alerta.geometry(f"+{x}+{y}")

        marco = ctk.CTkFrame(
            alerta,
            fg_color=FONDO_BLANCO,
            border_color=NEGRO_BORDE,
            border_width=1,
            corner_radius=12
        )
        marco.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        etiqueta = ctk.CTkLabel(
            marco,
            text=mensaje,
            text_color="black",
            font=("Arial", 13),
            wraplength=300
        )
        etiqueta.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(15, 5)
        )

        botones = ctk.CTkFrame(
            marco,
            fg_color="transparent"
        )
        botones.pack(pady=(5, 15))

        def aceptar():

            alerta.destroy()

            if al_aceptar:
                al_aceptar()

        if tipo == "confirmar":

            btn_aceptar = ctk.CTkButton(
                botones,
                text="Aceptar",
                width=95,
                height=30,
                fg_color=VERDE_OLIVA,
                hover_color=VERDE_OLIVA_HOVER,
                command=aceptar
            )
            btn_aceptar.pack(side="left", padx=5)

            btn_cancelar = ctk.CTkButton(
                botones,
                text="Cancelar",
                width=95,
                height=30,
                fg_color=FONDO_BLANCO,
                hover_color="#EEEEEE",
                border_color=ROJO_OSCURO,
                border_width=1,
                text_color="black",
                command=alerta.destroy
            )
            btn_cancelar.pack(side="left", padx=5)

        else:

            btn_aceptar = ctk.CTkButton(
                botones,
                text="Aceptar",
                width=100,
                height=30,
                fg_color=VERDE_OLIVA,
                hover_color=VERDE_OLIVA_HOVER,
                command=aceptar
            )
            btn_aceptar.pack()

    # --------------------------------------------------
    # FORMULARIO
    # --------------------------------------------------

    def crear_formulario(self, padre, valores=None, bloquear_id=False):

        if valores is None:
            valores = [""] * 11

        formulario = ctk.CTkScrollableFrame(
            padre,
            fg_color=FONDO_CREMA_MODAL,
            scrollbar_button_color=VERDE_OLIVA
        )

        formulario.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=5
        )

        campos = [
            "Número de empleado",
            "Nombre",
            "Primer apellido",
            "Segundo apellido",
            "Cargo",
            "Calle",
            "Colonia",
            "Número exterior",
            "Código postal",
            "Teléfono",
            "Correo electrónico"
        ]

        entradas = {}

        for indice, campo in enumerate(campos):

            fila = indice // 2
            columna = indice % 2

            contenedor = ctk.CTkFrame(
                formulario,
                fg_color="transparent"
            )

            contenedor.grid(
                row=fila,
                column=columna,
                padx=10,
                pady=8,
                sticky="ew"
            )

            etiqueta = ctk.CTkLabel(
                contenedor,
                text=campo,
                font=("Arial", 11, "bold"),
                text_color="black"
            )
            etiqueta.pack(
                anchor="w",
                pady=(0, 3)
            )

            entrada = ctk.CTkEntry(
                contenedor,
                width=240,
                height=32,
                corner_radius=8,
                border_color=VERDE_BORDE_TABLA,
                fg_color=FONDO_BLANCO,
                text_color="black"
            )
            entrada.pack(fill="x")

            entrada.insert(0, str(valores[indice]))

            if indice == 0 and bloquear_id:
                entrada.configure(state="disabled")

            entradas[indice] = entrada

        formulario.grid_columnconfigure(
            0,
            weight=1
        )

        formulario.grid_columnconfigure(
            1,
            weight=1
        )

        return entradas

    def obtener_datos_formulario(self, entradas, padre):

        datos = []

        for indice in range(11):

            if indice == 0 and str(entradas[indice].cget("state")) == "disabled":

                valor = entradas[indice].get().strip()

            else:
                valor = entradas[indice].get().strip()

            datos.append(valor)

        # VALIDAR CAMPOS VACIOS
        if any(valor == "" for valor in datos):

            self.mostrar_alerta(
                padre,
                "Datos incorrectos. Verifique que todos los campos estén completos."
            )
            return None

        # VALIDAR NUMEROS
        try:

            datos[0] = int(datos[0])
            datos[7] = int(datos[7])
            datos[8] = int(datos[8])

        except ValueError:

            self.mostrar_alerta(
                padre,
                "El número de empleado, número exterior y código postal deben ser números."
            )
            return None

        # VALIDAR TELEFONO
        if not datos[9].isdigit():

            self.mostrar_alerta(
                padre,
                "El teléfono solamente debe contener números."
            )
            return None

        # VALIDAR CORREO
        if "@" not in datos[10] or "." not in datos[10]:

            self.mostrar_alerta(
                padre,
                "El correo electrónico no tiene un formato válido."
            )
            return None

        return datos

    # --------------------------------------------------
    # AGREGAR VETERINARIO
    # --------------------------------------------------

    def abrir_modal_agregar(self):

        modal = self.crear_ventana_modal(620, 560)

        marco = ctk.CTkFrame(
            modal,
            fg_color=FONDO_CREMA_MODAL,
            border_color=BORDE_CAFE_OSCURO,
            border_width=2,
            corner_radius=12
        )
        marco.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )

        # ENCABEZADO
        encabezado = ctk.CTkFrame(
            marco,
            fg_color="transparent"
        )
        encabezado.pack(
            fill="x",
            padx=15,
            pady=(10, 0)
        )

        titulo = ctk.CTkLabel(
            encabezado,
            text="Ingresar nuevo veterinario",
            font=("Arial", 18, "bold"),
            text_color="black"
        )
        titulo.pack(side="left")

        cerrar = ctk.CTkButton(
            encabezado,
            text="X",
            width=30,
            height=30,
            corner_radius=20,
            fg_color=ROJO_PILDORA,
            hover_color=ROJO_OSCURO,
            command=modal.destroy
        )
        cerrar.pack(side="right")

        entradas = self.crear_formulario(marco)

        # BOTONES
        botones = ctk.CTkFrame(
            marco,
            fg_color="transparent"
        )
        botones.pack(pady=(5, 12))

        def guardar():

            datos = self.obtener_datos_formulario(
                entradas,
                modal
            )

            if datos is None:
                return

            def confirmar_guardado():

                nuevo = Veterinarios(*datos)

                if nuevo.insertar():

                    def cerrar_y_actualizar():

                        modal.destroy()
                        self.cargar_datos()

                    self.mostrar_alerta(
                        modal,
                        "Acción realizada con éxito.",
                        al_aceptar=cerrar_y_actualizar
                    )

                else:

                    self.mostrar_alerta(
                        modal,
                        "En este momento no se pudo realizar la acción. Por favor, inténtelo de nuevo más tarde."
                    )

            self.mostrar_alerta(
                modal,
                "¿Estás seguro que deseas registrar este veterinario?",
                tipo="confirmar",
                al_aceptar=confirmar_guardado
            )

        btn_guardar = ctk.CTkButton(
            botones,
            text="Guardar",
            width=120,
            height=35,
            fg_color=VERDE_OLIVA,
            hover_color=VERDE_OLIVA_HOVER,
            command=guardar
        )
        btn_guardar.pack(side="left", padx=8)

        btn_cancelar = ctk.CTkButton(
            botones,
            text="Cancelar",
            width=120,
            height=35,
            fg_color=FONDO_BLANCO,
            hover_color="#EEEEEE",
            border_color=ROJO_OSCURO,
            border_width=1,
            text_color="black",
            command=modal.destroy
        )
        btn_cancelar.pack(side="left", padx=8)

    # --------------------------------------------------
    # CONSULTAR VETERINARIO
    # --------------------------------------------------

    def abrir_modal_detalle(self, vet):

        modal = self.crear_ventana_modal(620, 560)

        marco = ctk.CTkFrame(
            modal,
            fg_color=FONDO_CREMA_MODAL,
            border_color=BORDE_CAFE_OSCURO,
            border_width=2,
            corner_radius=12
        )
        marco.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )

        encabezado = ctk.CTkFrame(
            marco,
            fg_color="transparent"
        )
        encabezado.pack(
            fill="x",
            padx=15,
            pady=(10, 0)
        )

        titulo = ctk.CTkLabel(
            encabezado,
            text=f"Veterinario: {vet[1]} {vet[2]}",
            font=("Arial", 17, "bold"),
            text_color="black"
        )
        titulo.pack(side="left")

        cerrar = ctk.CTkButton(
            encabezado,
            text="X",
            width=30,
            height=30,
            corner_radius=20,
            fg_color=ROJO_PILDORA,
            hover_color=ROJO_OSCURO,
            command=modal.destroy
        )
        cerrar.pack(side="right")

        entradas = self.crear_formulario(
            marco,
            valores=vet,
            bloquear_id=True
        )

        botones = ctk.CTkFrame(
            marco,
            fg_color="transparent"
        )
        botones.pack(pady=(5, 12))

        # MODIFICAR
        def modificar():

            datos = self.obtener_datos_formulario(
                entradas,
                modal
            )

            if datos is None:
                return

            def confirmar_modificacion():

                actualizado = Veterinarios(*datos)

                if actualizado.actualizar():

                    def cerrar_y_actualizar():

                        modal.destroy()
                        self.cargar_datos()

                    self.mostrar_alerta(
                        modal,
                        "Acción realizada con éxito.",
                        al_aceptar=cerrar_y_actualizar
                    )

                else:

                    self.mostrar_alerta(
                        modal,
                        "En este momento no se pudo realizar la acción. Por favor, inténtelo de nuevo más tarde."
                    )

            self.mostrar_alerta(
                modal,
                "¿Estás seguro que deseas guardar las modificaciones de este registro?",
                tipo="confirmar",
                al_aceptar=confirmar_modificacion
            )

        # ELIMINAR
        def eliminar():

            def confirmar_eliminacion():

                if Veterinarios.eliminar(vet[0]):

                    def cerrar_y_actualizar():

                        modal.destroy()
                        self.cargar_datos()

                    self.mostrar_alerta(
                        modal,
                        "Acción realizada con éxito.",
                        al_aceptar=cerrar_y_actualizar
                    )

                else:

                    self.mostrar_alerta(
                        modal,
                        "En este momento no se pudo realizar la acción. Por favor, inténtelo de nuevo más tarde."
                    )

            self.mostrar_alerta(
                modal,
                "¿Estás seguro que deseas eliminar este registro?",
                tipo="confirmar",
                al_aceptar=confirmar_eliminacion
            )

        btn_modificar = ctk.CTkButton(
            botones,
            text="Modificar",
            width=120,
            height=35,
            fg_color=VERDE_OLIVA,
            hover_color=VERDE_OLIVA_HOVER,
            command=modificar
        )
        btn_modificar.pack(side="left", padx=8)

        btn_eliminar = ctk.CTkButton(
            botones,
            text="Eliminar",
            width=120,
            height=35,
            fg_color=ROJO_PILDORA,
            hover_color=ROJO_OSCURO,
            command=eliminar
        )
        btn_eliminar.pack(side="left", padx=8)

    # --------------------------------------------------
    # VOLVER
    # --------------------------------------------------

    def volver(self):

        if self.volver_menu:
            self.volver_menu()


# --------------------------------------------------
# EJECUTAR INTERFAZ DE FORMA INDEPENDIENTE
# --------------------------------------------------

if __name__ == "__main__":

    from conexionBD import crear_db

    crear_db()

    app = ctk.CTk()

    app.title("Parque Ecológico El Tecuán - Veterinarios")
    app.geometry("800x600")
    app.resizable(False, False)

    VistaVeterinarios(app)

    app.mainloop()
