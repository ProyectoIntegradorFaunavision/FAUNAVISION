import sys
import os
import tkinter as tk
import customtkinter as ctk
import math

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from especies.especies import Especies

ctk.set_appearance_mode("Light")

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
COLOR_TRANSPARENTE = "#010101"


class EspeciesView(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # 1. Configuración de la ventana principal
        self.title("FaunaVision - Especies")
        self.geometry("800x600")
        self.configure(fg_color="#FFFFFF")

        self.registros_filtrados = []
        self.pagina_actual = 0
        self.filas_por_pagina = 20

        self.crear_interfaz()

    # Método principal que organiza las secciones de la vista
    def crear_interfaz(self):
        self.crear_menu_superior()
        self.crear_barra_acciones()
        self.crear_tabla()

    # Crea la barra de navegación superior (Botón atrás, Título y Menú con botones funcionales)
    def crear_menu_superior(self):
        self.menuSuperiorFrame = ctk.CTkFrame(self, fg_color="#FFFFFF", height=70)
        self.menuSuperiorFrame.pack(fill="x", padx=30, pady=(15, 10))

        # Botón de Regresar
        self.btn_Regresar = ctk.CTkButton(
            self.menuSuperiorFrame, text="←", width=36, height=36, 
            corner_radius=18, fg_color="#95BA00", hover_color="#7da000",
            text_color="#FFFFFF", font=("", 16, "bold"),
            command=self.ir_menu
        )
        self.btn_Regresar.pack(side="left", padx=(0, 15), pady=10)

        # Título de la vista
        self.lbl_titulo = ctk.CTkLabel(
            self.menuSuperiorFrame, text="Especies", 
            font=("Inder", 25, "bold"), text_color="#000000"
        )
        self.lbl_titulo.pack(side="left", padx=(25,0))

        # Botones de navegación interactivos (Menú, Veterinarios, Expediente, Medicamentos, Animales Cautiverio)
        navegacion = [
            ("Menú", self.ir_menu),
            ("Veterinarios", self.ir_veterinarios),
            ("Expediente", self.ir_expediente),
            ("Medicamentos", self.ir_medicamentos),
            ("Animales Cautiverio", self.ir_animales_cautiverio)
        ]

        for texto, funcion_comando in navegacion:
            btn_menuSuperior = ctk.CTkButton(
                self.menuSuperiorFrame, text=texto, width=50, height=30,
                fg_color="transparent", font=("Inder", 11, "normal"), text_color="#000000",
                hover_color="#EFEFEF", command=funcion_comando
            )
            btn_menuSuperior.pack(side="right", padx=10)

    # Frame para la barra de búsqueda y el botón de añadir especie
    def crear_barra_acciones(self):
        self.acciones_frame = ctk.CTkFrame(self, fg_color="#FFFFFF")
        self.acciones_frame.pack(fill="x", padx=45, pady=(5, 15))

        self.acciones_frame.grid_columnconfigure(0, weight=1)
        self.acciones_frame.grid_columnconfigure(1, weight=0)

        # Barra de búsqueda
        self.entry_buscar = ctk.CTkEntry(
            self.acciones_frame, placeholder_text="Buscar, nombre de especie o código", 
            width=500, height=42, corner_radius=21,
            fg_color="white", border_color="#000000", border_width=2,
            font=("poppins", 12, "normal"), text_color="#757575"
        )
        self.entry_buscar.grid(row=0, column=0, sticky="ew", padx=(0, 15), pady=5)
        self.entry_buscar.bind("<KeyRelease>", self.filtrar_tabla)

        # Botón Añadir Especie
        self.btn_añadir = ctk.CTkButton(
            self.acciones_frame, text="Añadir Especie", 
            width=180, height=42, corner_radius=21,
            fg_color="#95A330", hover_color="#6D8927",
            font=("poppins", 12, "bold"),
            command=self.abrir_modal_agregar
        )
        self.btn_añadir.grid(row=0, column=1, sticky="ew", padx=(0, 0), pady=5)

    def crear_tabla(self):
        self.tabla_outer = tk.Frame(
            self,
            bg=VERDE_BORDE_TABLA,
            bd=0,
            highlightthickness=1,
            highlightbackground=VERDE_BORDE_TABLA,
        )
        self.tabla_outer.pack(fill="both", expand=True, padx=45, pady=(0, 10))

        self.header_tabla = tk.Frame(
            self.tabla_outer,
            bg=VERDE_HEADER_TABLA,
            height=35,
        )
        self.header_tabla.pack(fill="x", pady=(0, 1))
        self.header_tabla.pack_propagate(False)

        self.pesos_columnas = [1, 3, 5, 5, 2]
        encabezados = ["N°", "Código", "Nombre de la especie", "Nombre Científico", "Acciones"]

        for col_idx, texto in enumerate(encabezados):
            self.header_tabla.grid_columnconfigure(
                col_idx, weight=self.pesos_columnas[col_idx], uniform="col"
            )
            self.header_tabla.grid_rowconfigure(0, weight=1)
            lbl = tk.Label(
                self.header_tabla,
                text=texto,
                font=("poppins", 11, "bold"),
                fg="#111111",
                bg=VERDE_HEADER_TABLA,
                anchor="w" if col_idx > 0 else "center",
            )
            lbl.grid(row=0, column=col_idx, sticky="ew", padx=10)

        self.cuerpo_tabla = tk.Frame(self.tabla_outer, bg=VERDE_BORDE_TABLA)
        self.cuerpo_tabla.pack(fill="both", expand=True)

        self.filas_widgets = []
        for r in range(self.filas_por_pagina):
            self.cuerpo_tabla.grid_rowconfigure(r, weight=1)
            self.cuerpo_tabla.grid_columnconfigure(0, weight=1)

            fila_frame = tk.Frame(self.cuerpo_tabla, bg=FONDO_BLANCO)
            fila_frame.grid(
                row=r,
                column=0,
                sticky="nsew",
                pady=(0, 1 if r < self.filas_por_pagina - 1 else 0),
            )

            celdas = []
            for c in range(5):
                fila_frame.grid_columnconfigure(
                    c, weight=self.pesos_columnas[c], uniform="col"
                )
                fila_frame.grid_rowconfigure(0, weight=1)
                lbl = tk.Label(
                    fila_frame,
                    text="",
                    font=("Poppins", 10),
                    fg=VERDE_OLIVA if c == 4 else "#111111",
                    bg=FONDO_BLANCO,
                    anchor="w" if c > 0 else "center",
                )
                lbl.grid(row=0, column=c, sticky="ew", padx=10)
                celdas.append(lbl)

            self.filas_widgets.append(celdas)

        # Contenedor de Paginación
        self.paginacion_frame = ctk.CTkFrame(self, fg_color="transparent", height=40)
        self.paginacion_frame.pack(pady=(5, 10))

        self.cargar_datos()
    # Métodos de navegación superior (puedes enlazarlos a tus respectivas vistas)
    def ir_menu(self):
        print("Navegando al Menú principal")
        # self.destroy()
        # Aqui abririas la vista del menu

    def ir_veterinarios(self):
        print("Navegando a Veterinarios")

    def ir_expediente(self):
        print("Navegando a Expedientes")

    def ir_medicamentos(self):
        print("Navegando a Medicamentos")

    def ir_animales_cautiverio(self):
        print("Navegando a Animales Cautiverio")

    def cargar_datos(self):
        self.registros_filtrados = Especies.mostrar() or []
        self.pagina_actual = 0
        self.renderizar_tabla()

    def filtrar_tabla(self, event=None):
        criterio = self.entry_buscar.get().strip()
        if criterio:
            self.registros_filtrados = Especies.filtrar(criterio) or []
        else:
            self.registros_filtrados = Especies.mostrar() or []
        self.pagina_actual = 0
        self.renderizar_tabla()

    def cambiar_pagina(self, idx):
        self.pagina_actual = idx
        self.renderizar_tabla()

    def renderizar_tabla(self):
        inicio = self.pagina_actual * self.filas_por_pagina
        pagina_datos = self.registros_filtrados[inicio : inicio + self.filas_por_pagina]

        for idx_fila in range(self.filas_por_pagina):
            celdas = self.filas_widgets[idx_fila]
            if idx_fila < len(pagina_datos):
                esp = pagina_datos[idx_fila]
                num_global = inicio + idx_fila + 1
                valores = [
                    str(num_global),
                    str(esp[0]),
                    str(esp[1]),
                    str(esp[2]),
                    "Ver más",
                ]
                for c_idx, val in enumerate(valores):
                    celdas[c_idx].configure(text=val)
                    if c_idx == 4:
                        celdas[c_idx].configure(cursor="hand2", font=("Poppins", 10, "bold"))
                        celdas[c_idx].bind(
                            "<Button-1>", lambda e, m=esp: self.abrir_modal_detalle(m)
                        )
                    else:
                        celdas[c_idx].configure(cursor="", font=("Poppins", 10))
                        celdas[c_idx].unbind("<Button-1>")
            else:
                for c_idx in range(5):
                    celdas[c_idx].configure(text="", cursor="", font=("Poppins", 10))
                    celdas[c_idx].unbind("<Button-1>")

        self.construir_paginacion()

    def construir_paginacion(self):
        for widget in self.paginacion_frame.winfo_children():
            widget.destroy()

        total_paginas = max(1, math.ceil(len(self.registros_filtrados) / self.filas_por_pagina))

        if self.pagina_actual > total_paginas - 1:
            self.pagina_actual = max(0, total_paginas - 1)

        if total_paginas <= 1:
            return

        for i in range(total_paginas):
            btn_p = ctk.CTkButton(
                self.paginacion_frame,
                text=str(i + 1),
                width=30,
                height=30,
                corner_radius=15,
                fg_color="#84A91C" if i == self.pagina_actual else "#757575",
                hover_color=VERDE_OLIVA,
                font=("Poppins", 11, "bold"),
                command=lambda idx=i: self.cambiar_pagina(idx),
            )
            btn_p.pack(side="left", padx=3)

    def _crear_ventana_redondeada(self, padre, ancho, alto):
        ventana = ctk.CTkToplevel(padre)
        ventana.overrideredirect(True)
        ventana.configure(fg_color=COLOR_TRANSPARENTE)
        try:
            ventana.attributes("-transparentcolor", COLOR_TRANSPARENTE)
        except Exception:
            ventana.configure(fg_color=FONDO_BLANCO)
        ventana.grab_set()

        padre.update_idletasks()
        x = padre.winfo_rootx() + (padre.winfo_width() // 2) - (ancho // 2)
        y = padre.winfo_rooty() + (padre.winfo_height() // 2) - (alto // 2)
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
        return ventana

    def mostrar_alerta_figma(self, padre, mensaje, tipo="info", al_aceptar=None):
        alerta = self._crear_ventana_redondeada(padre, 300, 155)

        caja = ctk.CTkFrame(
            alerta,
            fg_color=FONDO_BLANCO,
            border_color=NEGRO_BORDE,
            border_width=2,
            corner_radius=18,
            bg_color=COLOR_TRANSPARENTE,
        )
        caja.pack(fill="both", expand=True)

        lbl = ctk.CTkLabel(
            caja,
            text=mensaje,
            font=("Poppins", 11),
            text_color="#111111",
            fg_color=FONDO_BLANCO,
            wraplength=250,
            justify="center",
        )
        lbl.pack(expand=True, padx=20, pady=(18, 8))

        btns = ctk.CTkFrame(caja, fg_color=FONDO_BLANCO)
        btns.pack(pady=(0, 18))

        def aceptar():
            alerta.destroy()
            if al_aceptar:
                al_aceptar()

        ctk.CTkButton(
            btns,
            text="Aceptar",
            width=75,
            height=24,
            corner_radius=12,
            fg_color=VERDE_OLIVA,
            hover_color=VERDE_OLIVA_HOVER,
            text_color="#111111",
            font=("Poppins", 10),
            command=aceptar,
        ).pack(side="left", padx=8)

        if tipo == "confirmar":
            ctk.CTkButton(
                btns,
                text="Cancelar",
                width=75,
                height=24,
                corner_radius=12,
                fg_color=FONDO_BLANCO,
                hover_color="#FFEBEB",
                border_color=ROJO_PILDORA,
                border_width=1,
                text_color="#111111",
                font=("Poppins", 10),
                command=alerta.destroy,
            ).pack(side="left", padx=8)

    def _crear_ficha_inputs(self, parent, valores=None, bloquear_codigo=False):
        grid_box = tk.Frame(
            parent,
            bg=NEGRO_BORDE,
            bd=0,
            highlightthickness=1,
            highlightbackground=NEGRO_BORDE,
        )
        grid_box.pack(fill="x", padx=28, pady=(12, 18))

        def celda(row, col, colspan, label_txt, val="", readonly=False):
            cell = tk.Frame(
                grid_box,
                bg=FONDO_BLANCO,
                height=32,
                bd=0,
            )
            cell.grid(
                row=row,
                column=col,
                columnspan=colspan,
                sticky="nsew",
                padx=(0 if col == 0 else 1, 0),
                pady=(0 if row == 0 else 1, 0),
            )
            cell.pack_propagate(False)

            lbl = tk.Label(
                cell,
                text=label_txt,
                font=("Poppins", 9, "bold"),
                fg="#666666" if not val else "#111111",
                bg=FONDO_BLANCO,
            )
            lbl.pack(side="left", padx=(8, 4))

            entry = tk.Entry(
                cell,
                bd=0,
                highlightthickness=0,
                bg=FONDO_BLANCO,
                disabledbackground=FONDO_BLANCO,
                disabledforeground="#111111",
                fg="#111111",
                font=("Poppins", 9),
            )
            entry.pack(side="left", fill="both", expand=True, padx=(0, 8))
            if val != "":
                entry.insert(0, str(val))
            if readonly:
                entry.configure(state="disabled")
            return entry

        grid_box.grid_columnconfigure(0, weight=1)

        v = valores or ("", "", "")
        e_codigo = celda(0, 0, 1, "Código:", v[0], readonly=bloquear_codigo)
        e_nombre = celda(1, 0, 1, "Nombre de la especie:", v[1])
        e_cientifico = celda(2, 0, 1, "Nombre Científico:", v[2])

        return e_codigo, e_nombre, e_cientifico

    def abrir_modal_agregar(self):
        modal = self._crear_ventana_redondeada(self, 450, 275)

        marco = ctk.CTkFrame(
            modal,
            fg_color=FONDO_CREMA_MODAL,
            border_color=BORDE_CAFE_OSCURO,
            border_width=3,
            corner_radius=14,
            bg_color=COLOR_TRANSPARENTE,
        )
        marco.pack(fill="both", expand=True)

        top = ctk.CTkFrame(marco, fg_color=FONDO_CREMA_MODAL)
        top.pack(fill="x", padx=20, pady=(16, 4))

        ctk.CTkLabel(
            top,
            text="Ingresar nueva Especie",
            font=("Poppins", 13, "bold"),
            text_color="#111111",
            fg_color=FONDO_CREMA_MODAL,
        ).pack(side="left", padx=(15, 0))

        ctk.CTkButton(
            top,
            text="✕",
            width=26,
            height=26,
            corner_radius=13,
            fg_color=ROJO_PILDORA,
            hover_color=ROJO_OSCURO,
            border_color=NEGRO_BORDE,
            border_width=1,
            text_color="#111111",
            font=("Poppins", 12, "bold"),
            command=modal.destroy,
        ).pack(side="right")

        e_codigo, e_nombre, e_cientifico = self._crear_ficha_inputs(marco)

        btns = ctk.CTkFrame(marco, fg_color=FONDO_CREMA_MODAL)
        btns.pack(pady=(2, 16))

        def guardar():
            codigo = e_codigo.get().strip()
            nombre = e_nombre.get().strip()
            cientifico = e_cientifico.get().strip()

            if not all([codigo, nombre, cientifico]):
                self.mostrar_alerta_figma(
                    modal, "Datos incorrectos. Verifique la información ingresada."
                )
                return

            nueva_especie = Especies(codigo, nombre, cientifico)
            if nueva_especie.insertar():
                def cerrar_y_refrescar():
                    modal.destroy()
                    self.cargar_datos()

                self.mostrar_alerta_figma(
                    modal, "Acción realizada con éxito", al_aceptar=cerrar_y_refrescar
                )
            else:
                self.mostrar_alerta_figma(
                    modal,
                    "En este momento no se pudo realizar la acción. Por favor, inténtelo de nuevo más tarde.",
                )

        ctk.CTkButton(
            btns,
            text="Guardar",
            width=85,
            height=24,
            corner_radius=12,
            fg_color=VERDE_LIMA_BTN,
            hover_color=VERDE_LIMA_HOVER,
            border_color=VERDE_OLIVA,
            border_width=1,
            text_color="#111111",
            font=("Poppins", 10, "bold"),
            command=guardar,
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            btns,
            text="Cancelar",
            width=85,
            height=24,
            corner_radius=12,
            fg_color=FONDO_BLANCO,
            hover_color="#FFEBEB",
            border_color=ROJO_PILDORA,
            border_width=1,
            text_color="#111111",
            font=("Poppins", 10),
            command=modal.destroy,
        ).pack(side="left", padx=8)

    def abrir_modal_detalle(self, esp):
        modal = self._crear_ventana_redondeada(self, 450, 275)

        marco = ctk.CTkFrame(
            modal,
            fg_color=FONDO_CREMA_MODAL,
            border_color=BORDE_CAFE_OSCURO,
            border_width=3,
            corner_radius=14,
            bg_color=COLOR_TRANSPARENTE,
        )
        marco.pack(fill="both", expand=True)

        top = ctk.CTkFrame(marco, fg_color=FONDO_CREMA_MODAL)
        top.pack(fill="x", padx=20, pady=(16, 4))

        ctk.CTkLabel(
            top,
            text=f"Especie: {esp[1]}",
            font=("Poppins", 13, "bold"),
            text_color="#111111",
            fg_color=FONDO_CREMA_MODAL,
        ).pack(side="left", padx=(15, 0))

        ctk.CTkButton(
            top,
            text="✕",
            width=26,
            height=26,
            corner_radius=13,
            fg_color=ROJO_PILDORA,
            hover_color=ROJO_OSCURO,
            border_color=NEGRO_BORDE,
            border_width=1,
            text_color="#111111",
            font=("Poppins", 12, "bold"),
            command=modal.destroy,
        ).pack(side="right")

        e_codigo, e_nombre, e_cientifico = self._crear_ficha_inputs(
            marco, valores=esp, bloquear_codigo=True
        )

        btns = ctk.CTkFrame(marco, fg_color=FONDO_CREMA_MODAL)
        btns.pack(pady=(2, 16))

        def ejecutar_modificar():
            nombre = e_nombre.get().strip()
            cientifico = e_cientifico.get().strip()

            if not all([nombre, cientifico]):
                self.mostrar_alerta_figma(
                    modal, "Datos incorrectos. Verifique la información ingresada."
                )
                return

            def guardar_cambios():
                actualizada = Especies(esp[0], nombre, cientifico)
                if actualizada.actualizar():
                    def cerrar_todo():
                        modal.destroy()
                        self.cargar_datos()

                    self.mostrar_alerta_figma(
                        modal, "Acción realizada con éxito", al_aceptar=cerrar_todo
                    )
                else:
                    self.mostrar_alerta_figma(
                        modal,
                        "En este momento no se pudo realizar la acción. Por favor, inténtelo de nuevo más tarde.",
                    )

            self.mostrar_alerta_figma(
                modal,
                "¿Estás seguro que deseas guardar las modificaciones de este registro?",
                tipo="confirmar",
                al_aceptar=guardar_cambios,
            )

        def ejecutar_eliminar():
            def borrar_registro():
                if Especies.eliminar(esp[0]):
                    def cerrar_todo():
                        modal.destroy()
                        self.cargar_datos()

                    self.mostrar_alerta_figma(
                        modal, "Acción realizada con éxito", al_aceptar=cerrar_todo
                    )
                else:
                    self.mostrar_alerta_figma(
                        modal,
                        "En este momento no se pudo realizar la acción. Por favor, inténtelo de nuevo más tarde.",
                    )

            self.mostrar_alerta_figma(
                modal,
                "¿Estás seguro que deseas eliminar este registro?",
                tipo="confirmar",
                al_aceptar=borrar_registro,
            )

        ctk.CTkButton(
            btns,
            text="Modificar",
            width=85,
            height=24,
            corner_radius=12,
            fg_color=VERDE_LIMA_BTN,
            hover_color=VERDE_LIMA_HOVER,
            text_color="#111111",
            font=("Poppins", 10, "bold"),
            command=ejecutar_modificar,
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            btns,
            text="Eliminar",
            width=85,
            height=24,
            corner_radius=12,
            fg_color=ROJO_PILDORA,
            hover_color=ROJO_OSCURO,
            text_color="#111111",
            font=("Poppins", 10),
            command=ejecutar_eliminar,
        ).pack(side="left", padx=8)


if __name__ == "__main__":
    app = EspeciesView()
    app.mainloop()
   


