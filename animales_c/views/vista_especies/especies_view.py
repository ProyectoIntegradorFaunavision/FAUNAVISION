import sys
import os
from customtkinter import CTkButton,CTkFrame,CTkEntry,CTkOptionMenu,CTkTextbox
import CTkMessagebox
import tkinter as tk
import customtkinter as ctk
import math

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from especies.especies import Especies
from controllers.especies_controller import EspeciesController

ctk.set_appearance_mode("Light")


VERDE_OLIVA = "#84A91C"
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
EN_EMERGENTE = ("poppins", 20, "bold")
T_CUERPO = ("poppins", 16, "normal")
C_T_ENTRY= "#A9A9A9"


class EspeciesView(ctk.CTk):
    def __init__(self):
        super().__init__()

        #Creación atributos
        self.title("FaunaVision - Especies")
        self.geometry("900x650")
        self.configure(fg_color="#FFFFFF")
        self.datos_completos=[]
        self.registros_filtrados = []
        self.pagina_actual = 0
        self.filas_por_pagina = 15
        self.controlador=EspeciesController(self, filas_por_pagina=self.filas_por_pagina)
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
            font=("Inder", 30, "bold"), text_color="#000000"
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
                fg_color="transparent", font=("Inder", 12, "normal"), text_color="#000000",
                hover_color="#EFEFEF", command=funcion_comando
            )
            btn_menuSuperior.pack(side="right", padx=10)

    # Frame para la barra de búsqueda y el botón de añadir especie
    def crear_barra_acciones(self):
        self.acciones_frame = ctk.CTkFrame(self, fg_color="#FFFFFF")
        self.acciones_frame.pack(fill="x", padx=45, pady=(5, 15))

        self.acciones_frame.grid_columnconfigure(0, weight=1)
        self.acciones_frame.grid_columnconfigure(1, weight=0)
        self.acciones_frame.grid_columnconfigure(2, weight=0)

        self.buscar_contenedor = ctk.CTkFrame(
            self.acciones_frame,
            height=42,
            corner_radius=21,
            fg_color="#FFFFFF",
            border_color="#000000",
            border_width=2,
        )
        self.buscar_contenedor.grid(row=0, column=0, sticky="ew", padx=(0, 10), pady=5)
        self.buscar_contenedor.grid_columnconfigure(0, weight=1)
        self.buscar_contenedor.grid_columnconfigure(1, weight=0)
        self.buscar_contenedor.grid_propagate(False)

        self.entry_buscar = ctk.CTkEntry(
            self.buscar_contenedor,
            placeholder_text="Buscar, nombre de especie o código",
            height=36,
            border_width=0,
            fg_color="transparent",
            font=("poppins", 12, "normal"),
            text_color="#111111",
        )
        self.entry_buscar.grid(row=0, column=0, sticky="ew", padx=(14, 4), pady=2)
        self.entry_buscar.bind("<KeyRelease>", lambda _e: self.buscar_tabla())

        # Icono interno para enviar a buscar
        self.lbl_buscar = ctk.CTkLabel(
            self.buscar_contenedor,
            text="🔍",
            text_color=T_NEGRO,
            font=("poppins", 15, "normal"),
            
        )
        self.lbl_buscar.grid(row=0, column=1, padx=(0, 15), pady=4)

        # self.btn_filtro = ctk.CTkButton(
        #     self.acciones_frame,
        #     text="☰", 
        #     width=42,
        #     height=42,
        #     corner_radius=1,
        #     fg_color="#FFFFFF",
        #     hover_color="#F2F2F2",
        #     text_color="#111111",
        #     font=("poppins", 20, "normal"),
        #     command=None,
        #     )
        # self.btn_filtro.grid(row=0, column=1, padx=(0, 15), pady=5)


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
            height=40,
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
                font=("poppins", 14, "bold"),
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
                if c == 4:
                    acciones_celda = tk.Frame(fila_frame, bg=FONDO_BLANCO)
                    acciones_celda.grid(row=0,column=c,sticky="ew",padx=6)
                    btn_editar = ctk.CTkButton(
                        acciones_celda,
                        text="✏",
                        width=28,
                        height=18,
                        font=("poppins",15,"normal"),
                        fg_color="transparent",
                        hover_color="#6D8927",
                        text_color=T_NEGRO,
                        corner_radius=8,
                        cursor="hand2",
                    )

                    btn_editar.pack(side="left", padx=(0, 4))

                    btn_eliminar = ctk.CTkButton(
                        acciones_celda,
                        text="🗑",
                        width=24,
                        height=18,
                        font=("poppins",15,"normal"),
                        fg_color="transparent",
                        hover_color=ROJO_PILDORA,
                        text_color=T_NEGRO,
                        corner_radius=8,
                        cursor="hand2",
                    )
                    btn_eliminar.pack(side="left")

                    # Ocultos por defecto hasta que haya registro en esa fila
                    btn_editar.pack_forget()
                    btn_eliminar.pack_forget()

                    celdas.append({
                        "frame": acciones_celda,
                        "editar": btn_editar,
                        "eliminar": btn_eliminar,
                    })
                else:
                    lbl = tk.Label(
                        fila_frame,
                        text="",
                        font=("Poppins", 15),
                        fg="#111111",
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
        self.registros_filtrados = self.controlador.mostrarController() or []
        self.pagina_actual = 0
        self.renderizar_tabla()

    def buscar_tabla(self):
        criterio = self.entry_buscar.get().strip()

        if criterio:
            resultados = self.controlador.buscarController(criterio)
            if resultados is None and hasattr(self.controlador, "mostrarController"):
                try:
                    resultados = self.controlador.mostrarController(criterio)
                except TypeError:
                    resultados = []
            self.registros_filtrados = resultados or []
        else:
            self.registros_filtrados = self.controlador.mostrarController() or []

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
                ]
                for c_idx, valor in enumerate(valores):
                    celdas[c_idx].configure(text=valor, font=("Poppins", 14))

                acciones = celdas[4]
                acciones["eliminar"].pack(side="left", padx=(0, 6))
                acciones["editar"].pack(side="left")
                acciones["eliminar"].configure(
                    command=lambda fila=dato_celda: self.ventanaEliminar(fila)
                )
                acciones["editar"].configure(
                    command=lambda fila=dato_celda: self.ventanaModificar(fila)
                )
            else:
                for c_idx in range(4):
                    celdas[c_idx].configure(text="", font=("Poppins", 15))

                acciones = celdas[4]
                acciones["eliminar"].pack_forget()
                acciones["editar"].pack_forget()

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

 
    def ventanaEmergente(self,ancho,alto):
        ventanaEmergente = ctk.CTkToplevel(self)
        ventanaEmergente.title("Añadir nueva Especie")

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
        ventanaEmergente.configure(fg_color="#FFFCF4")
        ventanaEmergente.lift()
        ventanaEmergente.focus_force()
        ventanaEmergente.grab_set()
       
        
        

        return ventanaEmergente
    
    def ventanaAñadir(self):
        self.vAñadir= self.ventanaEmergente(350,300)
        self.vAñadir.title("Añadir Nueva Especie")

        self.frameCabeza= ctk.CTkFrame(self.vAñadir,fg_color="transparent")
        self.frameCabeza.pack(fill="x",padx=10,pady=10)
        self.frameCabeza.grid_columnconfigure(0, weight=1)

        self.frameCampos = ctk.CTkFrame(self.vAñadir,fg_color="transparent")
        self.frameCampos.pack(fill="x",padx=10,pady=10)

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
            text="Nueva Especie",
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
            placeholder_text="12451",
            font=T_CUERPO,
            placeholder_text_color=C_T_ENTRY         
            )
        self.codigo.focus()
        self.codigo.grid(row=2, column=1, pady=5, padx=(15, 3))

        lbl_especie= ctk.CTkLabel(
            self.frameCampos,
            text="Nombre Especie:",
            font=T_CUERPO,
            text_color=T_NEGRO,
        )
        lbl_especie.grid(row=3, column=0, pady=5, padx=(15, 3),sticky="e")
        self.nombre_especie=ctk.CTkEntry(
            self.frameCampos,
            placeholder_text="Lobo Mexicano",
            font=T_CUERPO,
            placeholder_text_color=C_T_ENTRY         
            )
        self.nombre_especie.grid(row=3, column=1, pady=5, padx=(15, 3))

        lbl_cientifico = ctk.CTkLabel(
            self.frameCampos,
            text="Nombre científico:",
            font=T_CUERPO,
            text_color=T_NEGRO,
        )
        lbl_cientifico.grid(row=4, column=0, pady=5, padx=(15, 3),sticky="e")
        self.nombre_cientifico=ctk.CTkEntry(
            self.frameCampos,
            placeholder_text="Canis lupus",
            font=T_CUERPO,
            placeholder_text_color=C_T_ENTRY         
            )
        self.nombre_cientifico.grid(row=4, column=1, pady=5, padx=(15, 3))

        self.btn_guardar=ctk.CTkButton(
            self.frameBotones,
            text="Guardar",
            font=T_CUERPO,
            text_color=T_NEGRO,
            fg_color=VERDE_LIMA_HOVER,
            corner_radius=20,
            command= self.controlador.insertarController
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
            command=self.vAñadir.destroy
        )
        self.btn_cancelar.grid(row=0, column=1, padx=(8, 0), sticky="w")

    def limpiar_campos_anadir(self):
        for entry in (self.codigo, self.nombre_especie, self.nombre_cientifico):
            entry.delete(0, "end")
        self.codigo.focus()

    def ventanaModificar(self,fila):
        self.vModificar= self.ventanaEmergente(350,300)
        self.vModificar.title("Modificar Especie")

        self.frameCabeza= ctk.CTkFrame(self.vModificar,fg_color="transparent")
        self.frameCabeza.pack(fill="x",padx=10,pady=10)
        self.frameCabeza.grid_columnconfigure(0, weight=1)

        self.frameCampos = ctk.CTkFrame(self.vModificar,fg_color="transparent")
        self.frameCampos.pack(fill="x",padx=10,pady=10)

        self.frameBotones = ctk.CTkFrame(self.vModificar, fg_color="transparent")
        self.frameBotones.pack(fill="x", padx=14, pady=(6, 12))
        self.frameBotones.grid_columnconfigure(0, weight=1)
        self.frameBotones.grid_columnconfigure(1, weight=1)

        self.codigo_actual = fila[0]
        self.nuevo_nombre = fila[1]
        self.nuevo_cientifico = fila[2]

        tituloModificar=ctk.CTkLabel(
            self.frameCabeza,
            text="Modificar",
            font=EN_EMERGENTE,
            text_color=T_NEGRO
            )
        tituloModificar.grid(row=0, column=0,pady=(5,2))
        subt = ctk.CTkLabel(
            self.frameCabeza,
            text="Especie",
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
            font=T_CUERPO,
            placeholder_text_color=T_NEGRO         
            )
        self.codigo.grid(row=2, column=1, pady=5, padx=(15, 3))
        self.codigo.delete(0, "end")
        self.codigo.insert(0, str(self.codigo_actual))
        self.codigo.configure(state="disabled")


        lbl_especie= ctk.CTkLabel(
            self.frameCampos,
            text="Nombre Especie:",
            font=T_CUERPO,
            text_color=T_NEGRO,
        )

        lbl_especie.grid(row=3, column=0, pady=5, padx=(15, 3),sticky="e")
        self.nombre_especie=ctk.CTkEntry(
            self.frameCampos,
            font=T_CUERPO,
            placeholder_text_color=C_T_ENTRY         
            )
        self.nombre_especie.grid(row=3, column=1, pady=5, padx=(15, 3))
        self.nombre_especie.delete(0, "end")
        self.nombre_especie.insert(0, str(self.nuevo_nombre))

        lbl_cientifico = ctk.CTkLabel(
            self.frameCampos,
            text="Nombre científico:",
            font=T_CUERPO,
            text_color=T_NEGRO,
        )
        lbl_cientifico.grid(row=4, column=0, pady=5, padx=(15, 3),sticky="e")
        self.nombre_cientifico=ctk.CTkEntry(
            self.frameCampos,
            font=T_CUERPO,
            placeholder_text_color=C_T_ENTRY         
            )
        self.nombre_cientifico.grid(row=4, column=1, pady=5, padx=(15, 3))
        self.nombre_cientifico.delete(0, "end")
        self.nombre_cientifico.insert(0, str(self.nuevo_cientifico))

        self.btn_guardar=ctk.CTkButton(
            self.frameBotones,
            text="Guardar",
            font=T_CUERPO,
            text_color=T_NEGRO,
            fg_color=VERDE_LIMA_HOVER,
            corner_radius=20,
            command= self.controlador.modificarController
            
        )      
        self.btn_guardar.grid(row=0,column=0, padx=(0, 2), sticky="e")

        self.btn_cancelar = ctk.CTkButton(
            self.frameBotones,
            text="Cancelar",
            font=T_CUERPO,
            fg_color="transparent",
            border_width=2,
            border_color=ROJO_OSCURO,
            text_color=T_NEGRO,
            corner_radius=20,
            command=self.vModificar.destroy
        )
        self.btn_cancelar.grid(row=0, column=1, padx=(2, 0), sticky="w")
        
    def ventanaEliminar(self,fila):
        elemento = fila[1]
        self.codigo_eliminar=fila[0]
        self.vEliminar=self.ventanaEmergente(350,180)

        self.vEliminar.title("Eliminar Registro")
        lbl_titulo = ctk.CTkLabel(
            self.vEliminar,
            text="¿Eliminar registro?",
            font=EN_EMERGENTE ,
            text_color=T_NEGRO,
        )
        lbl_titulo.pack(pady=(18, 4))
        lbl_mensaje = ctk.CTkLabel(
            self.vEliminar,
            text=f"¿Seguro que deseas eliminar {elemento}?",
            font=("poppins",14,"normal") ,
            text_color=T_NEGRO ,
        )
        lbl_mensaje.pack(pady=(0, 16))

        self.frameBotones=ctk.CTkFrame(self.vEliminar , fg_color="transparent")
        self.frameBotones.pack(pady=4)

        def confirmar():
            self.vEliminar.destroy()
            self.controlador.eliminarController(self.codigo_eliminar)

        self.btn_aceptar=ctk.CTkButton(
            self.frameBotones,
            text="Aceptar",
            font=T_CUERPO,
            text_color=T_NEGRO,
            fg_color=VERDE_LIMA_HOVER,
            corner_radius=20,
            command= confirmar,
        )      
        self.btn_aceptar.grid(row=0,column=0, padx=(0, 8), sticky="e")

        self.btn_cancelar = ctk.CTkButton(
            self.frameBotones,
            text="Cancelar",
            font=T_CUERPO,
            fg_color="transparent",
            border_width=2,
            border_color=ROJO_OSCURO,
            text_color=T_NEGRO,
            corner_radius=20,
            command=self.vEliminar.destroy
        )
        self.btn_cancelar.grid(row=0, column=1, padx=(8, 0), sticky="w")

        






if __name__ == "__main__":
    app = EspeciesView()
    app.mainloop()
   


