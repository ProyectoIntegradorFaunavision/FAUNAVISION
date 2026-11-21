import sys
import os
from customtkinter import CTkButton,CTkFrame,CTkEntry,CTkOptionMenu,CTkTextbox
import CTkMessagebox
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
T_NEGRO = "#000000"
COLOR_TRANSPARENTE = "#010101"
EN_EMERGENTE = ("poppins", 20, "bold")
T_CUERPO = ("poppins", 12, "normal")
C_T_ENTRY= "#A9A9A9"


class EspeciesView(ctk.CTk):
    def __init__(self):
        super().__init__()

        #Creación atributos
        self.title("FaunaVision - Especies")
        self.geometry("900x650")
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
            command=self.ventanaAñadir
        )
        self.btn_añadir.grid(row=0, column=1, sticky="ew", padx=(0, 0), pady=5)

    def crear_tabla(self):
        #Frame de tablas
        self.tabla_especies = tk.Frame(
            self,
              bg=VERDE_BORDE_TABLA,
              bd=0,
              highlightthickness=2,
              highlightbackground=VERDE_BORDE_TABLA,
        )
        self.tabla_especies.pack(fill="both", expand=True, padx=45, pady=(0, 10))

        self.titulos_tabla = tk.Frame(
            self.tabla_especies,
            bg=VERDE_HEADER_TABLA,
            height=35,
        )
        self.titulos_tabla.pack(fill="x", pady=(0, 1))
        self.titulos_tabla.pack_propagate(False)

        self.pesos_columnas = [3, 5, 10, 10, 3]
        encabezados = ["N°", "Código", "Nombre de la especie", "Nombre Científico", "Acciones"]

        for col_idx, texto in enumerate(encabezados):
            self.titulos_tabla.grid_columnconfigure(
                col_idx, weight=self.pesos_columnas[col_idx], uniform="col"
            )
            self.titulos_tabla.grid_rowconfigure(0, weight=1)
            lbl = tk.Label(
                self.titulos_tabla,
                text=texto,
                font=("poppins", 12, "bold"),
                fg="#111111",
                bg=VERDE_HEADER_TABLA,
                anchor="w" if col_idx > 0 else "center",
            )
            lbl.grid(row=0, column=col_idx, sticky="ew", padx=10)

        self.cuerpo_tabla = tk.Frame(self.tabla_especies, bg=VERDE_BORDE_TABLA)
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
        self.registros_mostrar = Especies.mostrar()
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
                dato_celda = pagina_datos[idx_fila]
                num_global = inicio + idx_fila + 1
                valores = [
                    str(num_global),
                    str(dato_celda[0]),
                    str(dato_celda[1]),
                    str(dato_celda[2]),
                  #  "Ver más",
                ]
                for c_idx, valor in enumerate(valores):
                    celdas[c_idx].configure(text=valor)
                    if c_idx == 4:
                        celdas[c_idx].configure(cursor="hand2", font=("Poppins", 12, "bold"))
                        celdas[c_idx].bind(
                            "<Button-1>", lambda e, m=valor: self.abrir_ventana_redondeada(m)
                        )
                    else:
                        celdas[c_idx].configure(cursor="", font=("Poppins", 12))
                        celdas[c_idx].unbind("<Button-1>")
            else:
                for c_idx in range(5):
                    celdas[c_idx].configure(text="", cursor="", font=("Poppins", 12))
                    celdas[c_idx].unbind("<Button-1>")

        self.construir_paginacion()

    def construir_paginacion(self):

        for widget in self.paginacion_frame.winfo_children():
            widget.destroy()
        total_paginas = max(
            1, math.ceil(len(self.registros_filtrados) / self.filas_por_pagina)
        )

        if self.pagina_actual > total_paginas - 1:
            self.pagina_actual = max(0, total_paginas - 1)

        if total_paginas <= 1:
             return


        ESTILO_BTN = {
        "width": 30,
        "height": 30,
        "corner_radius": 15,
        "font": ("Poppins", 11, "bold"),
        }

        # Botón anterior
        btn_anterior = ctk.CTkButton(
            self.paginacion_frame,
            text="<",
            fg_color="#757575" if self.pagina_actual > 0 else "#D3D3D3",
            hover_color=VERDE_OLIVA if self.pagina_actual > 0 else "#D3D3D3",
            state="normal" if self.pagina_actual > 0 else "disabled",
            command=lambda: self.cambiar_pagina(self.pagina_actual - 1),
            **ESTILO_BTN,
            )
        btn_anterior.pack(side="left", padx=2)

        rango_visible = 2  
        paginas_a_mostrar = set()

        paginas_a_mostrar.add(0)  # Primera página
        paginas_a_mostrar.add(total_paginas - 1)  # Última página

        for i in range(
            max(0, self.pagina_actual - rango_visible),
            min(total_paginas, self.pagina_actual + rango_visible + 1),
            ):
            paginas_a_mostrar.add(i)

        paginas_ordenadas = sorted(list(paginas_a_mostrar))

        # Dibujar botones y puntos suspensivos
        ultimo_idx = -1
        for p in paginas_ordenadas:
        # Puntos suspensivos en cantidad masiva de paginas
            if ultimo_idx != -1 and p - ultimo_idx > 1:
                lbl_puntos = ctk.CTkLabel(
                self.paginacion_frame,
                text="...",
                font=("Poppins", 12, "bold"),
                text_color="#555555",
                )
        lbl_puntos.pack(side="left", padx=4)

        # Botón numérico de página
        especies_actual = p == self.pagina_actual
        btn_p = ctk.CTkButton(
            self.paginacion_frame,
            text=str(p + 1),
            fg_color="#84A91C" if especies_actual else "#757575",
            hover_color=VERDE_OLIVA,
            command=lambda idx=p: self.cambiar_pagina(idx),
            **ESTILO_BTN,
        )
        btn_p.pack(side="left", padx=2)
        ultimo_idx = p

        # Botón siguiente
        btn_siguiente = ctk.CTkButton(
            self.paginacion_frame,
            text=">",
            fg_color=(
                "#757575" if self.pagina_actual < total_paginas - 1 else "#D3D3D3"
            ),
            hover_color=(
                VERDE_OLIVA if self.pagina_actual < total_paginas - 1 else "#D3D3D3"
            ),
            state="normal" if self.pagina_actual < total_paginas - 1 else "disabled",
            command=lambda: self.cambiar_pagina(self.pagina_actual + 1),
            **ESTILO_BTN,
        )
        btn_siguiente.pack(side="left", padx=2)

    # def crear_ventana_redondeada(self, padre, ancho, alto):
    #     ventana = ctk.CTkToplevel(
    #         padre, 
    #         title="Especies"
    #         )
    #     ventana.resizable(False, False)
    #     ventana.configure(fg_color=COLOR_TRANSPARENTE)
    #     try:
    #         ventana.attributes("-transparentcolor", COLOR_TRANSPARENTE)
    #     except Exception:
    #         ventana.configure(fg_color=FONDO_BLANCO)
       

    #     padre.update_idletasks()
    #     x = padre.winfo_rootx() + (padre.winfo_width() // 2) - (ancho // 2)
    #     y = padre.winfo_rooty() + (padre.winfo_height() // 2) - (alto // 2)
    #     ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
    #     return ventana

    def respuesta_alerta(self, padre, mensaje, tipo="info"):
         if mensaje:
            CTkMessagebox.CTkMessagebox(title="Exitoso", message="Acción realizada con exito" )
         else:
            CTkMessagebox.CTkMessagebox(title="Verifica por favor", message="Esta acción no se pudo realizar con exito")
 

    #     def aceptar():#Borrar funcion
    #         alerta.destroy()
    #         if al_aceptar:
    #             al_aceptar()




    # def crear_ventana_info(self, parent, valores=None, bloquear_codigo=False):
    #     frame_info = ctk.CTkFrame(
    #         parent,
    #         fg_color="#FFFFFF",          # Ejemplo: color de fondo en CustomTkinter
    #         border_width=2,             # Grosor del borde
    #         border_color=NEGRO_BORDE    # Color del borde
    #     )
    #     frame_info.pack(fill="none", padx=28, pady=(12, 18))


    #     def celda(row, col, colspan, label_txt, val="", readonly=False):
    #         cell = ctk.CTkFrame(
    #             frame_Info,
    #             bg=FONDO_BLANCO,
    #             height=32,
    #             bd=0,
    #         )
    #         cell.grid(
    #             row=row,
    #             column=col,
    #             columnspan=colspan,
    #             sticky="nsew",
    #             padx=(0 if col == 0 else 1, 0),
    #             pady=(0 if row == 0 else 1, 0),
    #         )
    #         cell.pack_propagate(False)

    #         lbl = tk.Label(
    #             cell,
    #             text=label_txt,
    #             font=("Poppins", 9, "bold"),
    #             fg="#666666" if not val else "#111111",
    #             bg=FONDO_BLANCO,
    #         )
    #         lbl.pack(side="left", padx=(8, 4))

    #         entry = tk.Entry(
    #             cell,
    #             bd=0,
    #             highlightthickness=0,
    #             bg=FONDO_BLANCO,
    #             disabledbackground=FONDO_BLANCO,
    #             disabledforeground="#111111",
    #             fg="#111111",
    #             font=("Poppins", 9),
    #         )
    #         entry.pack(side="left", fill="both", expand=True, padx=(0, 8))
    #         if val != "":
    #             entry.insert(0, str(val))
    #         if readonly:
    #             entry.configure(state="disabled")
    #         return entry

    #     frame_Info.grid_columnconfigure(0, weight=1)

    #     v = valores or ("", "", "")
    #     e_codigo = celda(0, 0, 1, "Código:", v[0], readonly=bloquear_codigo)
    #     e_nombre = celda(1, 0, 1, "Nombre de la especie:", v[1])
    #     e_cientifico = celda(2, 0, 1, "Nombre Científico:", v[2])

    #     return e_codigo, e_nombre, e_cientifico

    # def ventanaAgregar(self):
    #     modal = self.crear_ventana_redondeada(self, 450, 275)

    #     marco = ctk.CTkFrame(
    #         modal,
    #         fg_color=FONDO_CREMA_MODAL,
    #         border_width=1,
    #         corner_radius=2,
    #         bg_color=COLOR_TRANSPARENTE,
    #     )
    #     marco.pack(fill="both", expand=True)

    #     top = ctk.CTkFrame(marco, fg_color=FONDO_CREMA_MODAL)
    #     top.pack(fill="x", padx=20, pady=(16, 4))

    #     ctk.CTkLabel(
    #         top,
    #         text="Ingresar nueva Especie",
    #         font=("Poppins", 13, "bold"),
    #         text_color="#111111",
    #         fg_color=FONDO_CREMA_MODAL,
    #     ).pack(side="left", padx=(15, 0))

    #     ctk.CTkButton(
    #          top,
    #          text="✕",
    #          width=26,
    #          height=26,
    #          corner_radius=13,
    #          fg_color=ROJO_PILDORA,
    #          hover_color=ROJO_OSCURO,
    #          border_color=NEGRO_BORDE,
    #          border_width=1,
    #          text_color="#111111",
    #          font=("Poppins", 12, "bold"),
    #          command=modal.destroy,
    #      ).pack(side="right")

    #     e_codigo, e_nombre, e_cientifico = self.crear_ventana_info(marco)

    #     btns = ctk.CTkFrame(marco, fg_color=FONDO_CREMA_MODAL)
    #     btns.pack(pady=(2, 16))

    #     def guardar():
    #         codigo = e_codigo.get().strip()
    #         nombre = e_nombre.get().strip()
    #         cientifico = e_cientifico.get().strip()

    #         if not all([codigo, nombre, cientifico]):
    #             self.respuesta_alerta(
    #                 modal, "Datos incorrectos. Verifique la información ingresada."
    #             )
    #             return

    #         nueva_especie = Especies(codigo, nombre, cientifico)
    #         if nueva_especie.insertar():
    #             def cerrar_y_refrescar():
    #                 modal.destroy()
    #                 self.cargar_datos()

    #             self.respuesta_alerta(
    #                 modal, "Acción realizada con éxito", al_aceptar=cerrar_y_refrescar
    #             )
    #         else:
    #             self.respuesta_alerta(
    #                 modal,
    #                 "En este momento no se pudo realizar la acción. Por favor, inténtelo de nuevo más tarde.",
    #             )

    #     ctk.CTkButton(
    #         btns,
    #         text="Guardar",
    #         width=85,
    #         height=24,
    #         corner_radius=12,
    #         fg_color=VERDE_LIMA_BTN,
    #         hover_color=VERDE_LIMA_HOVER,
    #         border_color=VERDE_OLIVA,
    #         border_width=1,
    #         text_color="#111111",
    #         font=("Poppins", 10, "bold"),
    #         command=guardar,
    #     ).pack(side="left", padx=8)

    #     ctk.CTkButton(
    #         btns,
    #         text="Cancelar",
    #         width=85,
    #         height=24,
    #         corner_radius=12,
    #         fg_color=FONDO_BLANCO,
    #         hover_color="#FFEBEB",
    #         border_color=ROJO_PILDORA,
    #         border_width=1,
    #         text_color="#111111",
    #         font=("Poppins", 10),
    #         command=modal.destroy,
    #     ).pack(side="left", padx=8)

    # def abrir_ventana_redondeada(self, esp):
    #     modal = self.crear_ventana_redondeada(self, 450, 275)

    #     marco = ctk.CTkFrame(
    #         modal,
    #         fg_color=FONDO_CREMA_MODAL,
    #         border_color=BORDE_CAFE_OSCURO,
    #         border_width=3,
    #         corner_radius=14,
    #         bg_color=COLOR_TRANSPARENTE,
    #     )
    #     marco.pack(fill="both", expand=True)

    #     top = ctk.CTkFrame(marco, fg_color=FONDO_CREMA_MODAL)
    #     top.pack(fill="x", padx=20, pady=(16, 4))

    #     ctk.CTkLabel(
    #         top,
    #         text=f"Especie: {esp[1]}",
    #         font=("Poppins", 13, "bold"),
    #         text_color="#111111",
    #         fg_color=FONDO_CREMA_MODAL,
    #     ).pack(side="left", padx=(15, 0))

    #     ctk.CTkButton(
    #         top,
    #         text="✕",
    #         width=26,
    #         height=26,
    #         corner_radius=13,
    #         fg_color=ROJO_PILDORA,
    #         hover_color=ROJO_OSCURO,
    #         border_color=NEGRO_BORDE,
    #         border_width=1,
    #         text_color="#111111",
    #         font=("Poppins", 12, "bold"),
    #         command=modal.destroy,
    #     ).pack(side="right")

    #     e_codigo, e_nombre, e_cientifico = self._crear_ventana_info(
    #         marco, valores=esp, bloquear_codigo=True
    #     )

    #     btns = ctk.CTkFrame(marco, fg_color=FONDO_CREMA_MODAL)
    #     btns.pack(pady=(2, 16))

    #     def ejecutar_modificar():
    #         nombre = e_nombre.get().strip()
    #         cientifico = e_cientifico.get().strip()

    #         if not all([nombre, cientifico]):
    #             self.respuesta_alerta(
    #                 modal, "Datos incorrectos. Verifique la información ingresada."
    #             )
    #             return

    #         def guardar_cambios():
    #             actualizada = Especies(esp[0], nombre, cientifico)
    #             if actualizada.actualizar():
    #                 def cerrar_todo():
    #                     modal.destroy()
    #                     self.cargar_datos()

    #                 self.respuesta_alerta(
    #                     modal, "Acción realizada con éxito", al_aceptar=cerrar_todo
    #                 )
    #             else:
    #                 self.respuesta_alerta(
    #                     modal,
    #                     "En este momento no se pudo realizar la acción. Por favor, inténtelo de nuevo más tarde.",
    #                 )

    #         self.respuesta_alerta(
    #             modal,
    #             "¿Estás seguro que deseas guardar las modificaciones de este registro?",
    #             tipo="confirmar",
    #             al_aceptar=guardar_cambios,
    #         )

    #     def ejecutar_eliminar():
    #         def borrar_registro():
    #             if Especies.eliminar(esp[0]):
    #                 def cerrar_todo():
    #                     modal.destroy()
    #                     self.cargar_datos()

    #                 self.respuesta_alerta(
    #                     modal, "Acción realizada con éxito", al_aceptar=cerrar_todo
    #                 )
    #             else:
    #                 self.respuesta_alerta(
    #                     modal,
    #                     "En este momento no se pudo realizar la acción. Por favor, inténtelo de nuevo más tarde.",
    #                 )

    #         self.respuesta_alerta(
    #             modal,
    #             "¿Estás seguro que deseas eliminar este registro?",
    #             tipo="confirmar",
    #             al_aceptar=borrar_registro,
    #         )

    #     ctk.CTkButton(
    #         btns,
    #         text="Modificar",
    #         width=85,
    #         height=24,
    #         corner_radius=12,
    #         fg_color=VERDE_LIMA_BTN,
    #         hover_color=VERDE_LIMA_HOVER,
    #         text_color="#111111",
    #         font=("Poppins", 10, "bold"),
    #         command=ejecutar_modificar,
    #     ).pack(side="left", padx=8)

    #     ctk.CTkButton(
    #         btns,
    #         text="Eliminar",
    #         width=85,
    #         height=24,
    #         corner_radius=12,
    #         fg_color=ROJO_PILDORA,
    #         hover_color=ROJO_OSCURO,
    #         text_color="#111111",
    #         font=("Poppins", 10),
    #         command=ejecutar_eliminar,
    #     ).pack(side="left", padx=8)

    def ventanaEmergente(self,ancho,alto):
        ancho = 500
        alto = 500

        ventanaEmergente = ctk.CTkToplevel(self)
        ventanaEmergente.title("Añadir Nueva Especie")
        ventanaEmergente.pack_propagate(False)
        ventanaEmergente.grid_propagate(False)
        ventanaEmergente.minsize(ancho, alto)
        ventanaEmergente.maxsize(ancho, alto)
        ventanaEmergente.resizable(False, False)

        self.update_idletasks()
        x = int(self.winfo_rootx() + (self.winfo_width() // 2) - (ancho // 2))
        y = int(self.winfo_rooty() + (self.winfo_height() // 2) - (alto // 2))
        x = max(0, x)
        y = max(0, y)
        ventanaEmergente.geometry(f"{ancho}x{alto}+{x}+{y}")
        ventanaEmergente.after(50, lambda: ventanaEmergente.geometry(f"{ancho}x{alto}+{x}+{y}"))
        ventanaEmergente.grab_set()
        ventanaEmergente.configure(fg_color="#FFFCF4")

        return ventanaEmergente
    
    def ventanaAñadir(self):
        self.vAñadir= self.ventanaEmergente(300,300)
        self.vAñadir.title("Añadir Nueva Especie")

        self.frameCabeza= ctk.CTkFrame(self.vAñadir,fg_color="transparent")
        self.frameCabeza.pack(fill="x",padx=10,pady=10)
        self.frameCabeza.grid_columnconfigure(0, weight=1)

        self.frameCampos = ctk.CTkFrame(self.vAñadir,fg_color="transparent")
        self.frameCampos.pack(fill="x",padx=10,pady=10)

        self.frameObservaciones = ctk.CTkFrame(self.vAñadir,fg_color="transparent")
        self.frameObservaciones.pack(fill="both",expand=True,padx=10,pady=10)

        self.frameBotones = ctk.CTkFrame(self.vAñadir, fg_color="transparent")
        self.frameBotones.pack(fill="x", padx=14, pady=(6, 12))
        self.frameBotones.grid_columnconfigure(0, weight=1)
        self.frameBotones.grid_columnconfigure(1, weight=1)

        tituloAñadir=ctk.CTkLabel(
            self.frameCabeza,
            text="Añadir",
            font=EN_EMERGENTE,
            text_color=T_NEGRO
            )
        tituloAñadir.grid(row=0, column=0,pady=(5,2))
        subt = ctk.CTkLabel(
            self.frameCabeza,
            text="Nuevo animal en cautiverio",
            font=("poppins", 15, "normal"),
            text_color=T_NEGRO
            )
        subt.grid(row=1, column=0,pady=(0,5))

        lbl_codigo = ctk.CTkLabel(
            self.frameCampos,
            text="Código:",
            font=T_CUERPO,
            text_color=T_NEGRO,
        )
        lbl_codigo.grid(row=2, column=0, pady=5, padx=(15, 3),sticky="e")
        self.codigo=ctk.CTkEntry(
            self.frameCampos,
            placeholder_text="A12451",
            font=T_CUERPO,
            placeholder_text_color=C_T_ENTRY         
            )
        self.codigo.focus()
        self.codigo.grid(row=2, column=1, pady=5, padx=(15, 3))

        lbl_especie= ctk.CTkLabel(
            self.frameCampos,
            text="Especie:",
            font=T_CUERPO,
            text_color=T_NEGRO,
        )
        lbl_especie.grid(row=2, column=2, pady=5, padx=(15, 3),sticky="e")
        self.especie=ctk.CTkEntry(
            self.frameCampos,
            placeholder_text="Lobo Mexicano",
            font=T_CUERPO,
            placeholder_text_color=C_T_ENTRY         
            )
        self.especie.grid(row=2, column=3, pady=5, padx=(15, 3))

        lbl_sexo = ctk.CTkLabel(
            self.frameCampos,
            text="Sexo:",
            font=T_CUERPO,
            text_color=T_NEGRO,
        )
        lbl_sexo.grid(row=3, column=0, pady=5, padx=(15, 3),sticky="e")
        self.sexo=ctk.CTkEntry(
            self.frameCampos,
            placeholder_text="Macho",
            font=T_CUERPO,
            placeholder_text_color=C_T_ENTRY         
            )
        self.sexo.grid(row=3, column=1, pady=5, padx=(15, 3))

        lbl_peso= ctk.CTkLabel(
            self.frameCampos,
            text="Peso:",
            font=T_CUERPO,
            text_color=T_NEGRO,
        )
        lbl_peso.grid(row=3, column=2, pady=5, padx=(15, 3),sticky="e")
        self.peso=ctk.CTkEntry(
            self.frameCampos,
            placeholder_text="25",
            font=T_CUERPO,
            placeholder_text_color=C_T_ENTRY         
            )
        self.peso.grid(row=3, column=3, pady=5, padx=(15, 3))


        lbl_estado = ctk.CTkLabel(
            self.frameCampos,
            text="Estado\nActual:",
            font=T_CUERPO,
            text_color=T_NEGRO,
        )
        lbl_estado.grid(row=4, column=0, pady=5, padx=(15, 3),sticky="e")
        self.estado=ctk.CTkEntry(
            self.frameCampos,
            placeholder_text="Bueno",
            font=T_CUERPO,
            placeholder_text_color=C_T_ENTRY         
            )
        self.estado.grid(row=4, column=1, pady=5, padx=(15, 3))

        lbl_fIngreso= ctk.CTkLabel(
            self.frameCampos,
            text="Fecha\nIngreso:",
            font=T_CUERPO,
            text_color=T_NEGRO,
        )
        lbl_fIngreso.grid(row=4, column=2, pady=5, padx=(15, 3),sticky="e")
        self.fIngreso=ctk.CTkEntry(
            self.frameCampos,
            placeholder_text="DD/MM/AAAA",
            font=T_CUERPO,
            placeholder_text_color=C_T_ENTRY         
            )
        self.fIngreso.grid(row=4, column=3, pady=5, padx=(15, 3))

        lbl_fNacimiento= ctk.CTkLabel(
            self.frameCampos,
            text="Fecha\nNacimiento:",
            font=T_CUERPO,
            text_color=T_NEGRO,
        )
        lbl_fNacimiento.grid(row=5, column=0, pady=5, padx=(15, 3),sticky="e")
        self.fNacimiento=ctk.CTkEntry(
            self.frameCampos,
            placeholder_text="DD/MM/AAAA",
            font=T_CUERPO,
            placeholder_text_color=C_T_ENTRY         
            )
        self.fNacimiento.grid(row=5, column=1, pady=5, padx=(15, 3))

        lbl_observaciones=ctk.CTkLabel(
            self.frameObservaciones,
            text="Escribe una observación breve:",
            font=T_CUERPO,
            text_color=T_NEGRO
        )
        lbl_observaciones.pack(anchor="w", padx=4, pady=(0, 4))
        self.observaciones=ctk.CTkTextbox(
            self.frameObservaciones,
            corner_radius=12,
            border_width=2,
            height=40,
            font=T_CUERPO,
            fg_color="#FFFFFF",
            text_color=T_NEGRO                   
        )
        self.observaciones.pack(fill="both", expand=True)

        self.btn_guardar=ctk.CTkButton(
            self.frameBotones,
            text="Guardar",
            font=T_CUERPO,
            text_color=T_NEGRO,
            fg_color=VERDE_LIMA_BTN,
            corner_radius=20,
            command=None
        )      
        self.btn_guardar.grid(row=0,column=0, padx=(0, 8), sticky="e")

        self.btn_cancelar = ctk.CTkButton(
            self.frameBotones,
            text="Cancelar",
            font=T_CUERPO,
            fg_color="transparent",
            border_width=2,
            border_color=ROJO_OSCURO,
            text_color=T_NEGRO,
            corner_radius=20,
            command=lambda: self.vAñadir.destroy
        )
        self.btn_cancelar.grid(row=0, column=1, padx=(8, 0), sticky="w")
  






        






if __name__ == "__main__":
    app = EspeciesView()
    app.mainloop()
   


