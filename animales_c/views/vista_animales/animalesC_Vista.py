import sys
import os
import tkinter as tk
import customtkinter as ctk
import math

# Ruta para conectar con la raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from controllers.animales_controllers import AnimalesController


ctk.set_appearance_mode("Light")

VERDE_OLIVA = "#95BA00"
VERDE_OLIVA_HOVER = "#7da000"
VERDE_HEADER_TABLA = "#C5D88A"
VERDE_BORDE_TABLA = "#9BB354"
VERDE_LIMA_BTN = "#A3D900"
VERDE_LIMA_HOVER = "#8AB800"
FONDO_BLANCO = "#FFFFFF"
NEGRO_BORDE = "#1A1A1A"
T_NEGRO = "#000000"
ROJO_PILDORA = "#FF0000"
ROJO_OSCURO = "#CC0000"
EN_EMERGENTE = ("poppins", 20, "bold")
T_CUERPO = ("poppins", 16, "normal")
C_T_ENTRY= "#A9A9A9"


class AnimalesCView(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        
        # 1. Configuración de la ventana principal
        self.title("FaunaVision - Animales en Cautiverio")
        self.geometry("980x670")
        self.configure(fg_color=FONDO_BLANCO)
        self.datos_completos=[]
        self.registros_filtrados = []
        self.pagina_actual = 0
        self.filas_por_pagina = 15
        self.controlador=AnimalesController(self, filas_por_pagina=self.filas_por_pagina)

        self.crear_interfaz()

    def crear_interfaz(self):
        self.crear_menu_superior()
        self.crear_barra_acciones()
        self.crear_tabla()

    def crear_menu_superior(self):
        self.menuSuperiorFrame = ctk.CTkFrame(self, fg_color=FONDO_BLANCO, height=70)
        self.menuSuperiorFrame.pack(fill="x", padx=30, pady=(15, 10))

        # Botón de Regresar
        self.btn_Regresar = ctk.CTkButton(
            self.menuSuperiorFrame, text="←", width=36, height=36, 
            corner_radius=18, fg_color=VERDE_OLIVA, hover_color=VERDE_OLIVA_HOVER,
            text_color="#FFFFFF", font=("Arial", 16, "bold"),
            command=""
        )
        self.btn_Regresar.pack(side="left", padx=(0, 15), pady=10)

        # Título de la vista
        self.lbl_titulo = ctk.CTkLabel(
            self.menuSuperiorFrame, text="Animales en Cautiverio", 
            font=("Inder", 28, "bold"), text_color=T_NEGRO
        )
        self.lbl_titulo.pack(side="left", padx=(20,0))

        # Botones de navegación superior
        navegacion = [
            ("Menú", self.ir_menu),
            ("Veterinarios", self.ir_veterinarios),
            ("Expediente", self.ir_expediente),
            ("Medicamentos", self.ir_medicamentos),
            ("Especies", self.ir_especie)
        ]

        for texto, funcion_comando in navegacion:
            btn_menuSuperior = ctk.CTkButton(
                self.menuSuperiorFrame, text=texto, width=50, height=30,
                fg_color="transparent", font=("Inder", 12, "normal"), text_color="#000000",
                hover_color="#EFEFEF", command=funcion_comando
            )
            btn_menuSuperior.pack(side="right", padx=10)


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

    def ir_especie(self):
        print("Navegando a Animales Cautiverio")


    def crear_barra_acciones(self):
        self.acciones_frame = ctk.CTkFrame(self, fg_color="#FFFFFF")
        self.acciones_frame.pack(fill="x", padx=45, pady=(5, 15))

        self.acciones_frame.grid_columnconfigure(0, weight=1)
        self.acciones_frame.grid_columnconfigure(1, weight=0)
        self.acciones_frame.grid_columnconfigure(2, weight=0)

        # Barra de búsqueda
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
        
        #Boton Filtro
        self.btn_filtro = ctk.CTkButton(
            self.acciones_frame,
            text="☰", 
            width=42,
            height=42,
            corner_radius=1,
            fg_color="#FFFFFF",
            hover_color="#F2F2F2",
            text_color="#111111",
            font=("poppins", 20, "normal"),
            command=None,
             )
        self.btn_filtro.grid(row=0, column=1, padx=(0, 15), pady=5)


        # Botón Añadir Animal
        self.btn_añadir = ctk.CTkButton(
            self.acciones_frame, text="Añadir Animal", 
            width=180, height=42, corner_radius=21,
            fg_color="#95A330", hover_color="#6D8927",
            font=("Poppins", 12, "bold"),
            command=self.ventanaAñadir
        )
        self.btn_añadir.grid(row=0, column=1, sticky="ew", padx=(0, 0), pady=5)

    def crear_tabla(self):
        self.tabla_animales = tk.Frame(
            self,
              bg=VERDE_BORDE_TABLA,
              bd=0,
              highlightthickness=2,
              highlightbackground=VERDE_BORDE_TABLA,
        )
        self.tabla_animales.pack(fill="both", expand=True, padx=45, pady=(0, 10))

        self.titulos_tabla = tk.Frame(
            self.tabla_animales,
            bg=VERDE_HEADER_TABLA,
            height=40,
        )
        self.titulos_tabla.pack(fill="x", pady=(0, 1))
        self.titulos_tabla.pack_propagate(False)

        # Columnas según tus atributos
        self.pesos_columnas = [2, 2, 3, 2, 2, 2, 2, 2]
        encabezados = ["N°", "Código", "Especie", "Sexo", "Peso", "Edad", "Estado de salud", "Acciones"]

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

        self.cuerpo_tabla = tk.Frame(self.tabla_animales, bg=VERDE_BORDE_TABLA)
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
            for c in range(len(self.pesos_columnas)):
                fila_frame.grid_columnconfigure(
                    c, weight=self.pesos_columnas[c], uniform="col"
                )
                fila_frame.grid_rowconfigure(0, weight=1)
                if c == len(self.pesos_columnas)-1:
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

                    btn_ver = ctk.CTkButton(
                        acciones_celda,
                        text="👁",
                        width=28,
                        height=15,
                        font=("poppins",15,"normal"),
                        fg_color="transparent",
                        text_color=T_NEGRO,
                        corner_radius=8,
                        cursor="hand2",
                    )
                    btn_ver.pack(side="left")

                    # Ocultos por defecto hasta que haya registro en esa fila
                    btn_editar.pack_forget()
                    btn_eliminar.pack_forget()
                    btn_ver.pack_forget()

                    celdas.append({
                        "frame": acciones_celda,
                        "eliminar": btn_eliminar,
                        "editar": btn_editar,
                        "ver": btn_ver,
                        
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
            acciones = celdas[7]

            if idx_fila < len(pagina_datos):
                dato_celda = pagina_datos[idx_fila]
                num_global = inicio + idx_fila + 1

                codigo = dato_celda[0]
                especie = dato_celda[1]
                sexo = dato_celda[2]
                peso = dato_celda[5]
                fNacimiento = dato_celda[3]
                estado_salud = dato_celda[6]

                edad_texto = self.controlador.calcular_edad(fNacimiento)

                valores = [
                    str(num_global),
                    str(codigo),
                    str(especie),
                    str(sexo),
                    str(peso),
                    edad_texto,
                    str(estado_salud),
                ]
                for c_idx, valor in enumerate(valores):
                    celdas[c_idx].configure(text=valor, font=("Poppins", 14))


                    #Agregar Accion de modificar
                acciones["ver"].pack(side="left")
                acciones["editar"].pack(side="left")
                acciones["eliminar"].pack(side="left")
                acciones["ver"].configure(
                    command=lambda fila=dato_celda: self.ventanaInformacion(fila)
                )
                acciones["editar"].configure(
                    command= lambda fila=dato_celda: self.ventanaModificar(fila)
                )
                acciones["eliminar"].configure(
                    command= lambda fila=dato_celda: self.ventanaEliminar(fila)
                )

            else:
                for c_idx in range(7):
                    celdas[c_idx].configure(text="", font=("Poppins", 15))

                acciones = celdas[7]
                acciones["ver"].pack_forget()
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
        self.vAñadir= self.ventanaEmergente(520,450)

        self.frameCabeza= ctk.CTkFrame(self.vAñadir,fg_color="transparent")
        self.frameCabeza.pack(fill="x",padx=10,pady=10)
        self.frameCabeza.grid_columnconfigure(0, weight=1)

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

        self.frameCampos = ctk.CTkFrame(self.vAñadir,fg_color="transparent")
        self.frameCampos.pack(fill="x",padx=10,pady=10)

        self.frameObservaciones = ctk.CTkFrame(self.vAñadir,fg_color="transparent")
        self.frameObservaciones.pack(fill="both",expand=True,padx=10,pady=10)

        self.frameBotones = ctk.CTkFrame(self.vAñadir, fg_color="transparent")
        self.frameBotones.pack(fill="x", padx=14, pady=(6, 12))
        self.frameBotones.grid_columnconfigure(0, weight=1)
        self.frameBotones.grid_columnconfigure(1, weight=1)



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

        lbl_pesoInicial= ctk.CTkLabel(
            self.frameCampos,
            text="Peso:",
            font=T_CUERPO,
            text_color=T_NEGRO,
        )
        lbl_pesoInicial.grid(row=3, column=2, pady=5, padx=(15, 3),sticky="e")
        self.pesoInicial=ctk.CTkEntry(
            self.frameCampos,
            placeholder_text="25",
            font=T_CUERPO,
            placeholder_text_color=C_T_ENTRY         
            )
        self.pesoInicial.grid(row=3, column=3, pady=5, padx=(15, 3))


        lbl_estado_salud = ctk.CTkLabel(
            self.frameCampos,
            text="Estado\nActual:",
            font=T_CUERPO,
            text_color=T_NEGRO,
        )
        lbl_estado_salud.grid(row=4, column=0, pady=5, padx=(15, 3),sticky="e")
        self.estado_salud=ctk.CTkEntry(
            self.frameCampos,
            placeholder_text="Bueno",
            font=T_CUERPO,
            placeholder_text_color=C_T_ENTRY         
            )
        self.estado_salud.grid(row=4, column=1, pady=5, padx=(15, 3))

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
        for entry in (
            self.codigo, 
            self.especie, 
            self.sexo,
            self.fNacimiento,
            self.fIngreso,
            self.pesoInicial,
            self.estado_salud,
            self.observaciones
        ):
            entry.delete(0, "end")
        self.codigo.focus()

    def ventanaInformacion(self, fila):
        self.vInfo = self.ventanaEmergente(520, 450)

        self.frameCabeza = ctk.CTkFrame(self.vInfo, fg_color="transparent")
        self.frameCabeza.pack(fill="x", padx=10, pady=10)
        self.frameCabeza.grid_columnconfigure(0, weight=1)

        tituloInfo = ctk.CTkLabel(
            self.frameCabeza,
            text="Información",
            font=EN_EMERGENTE,
            text_color=T_NEGRO,
        )
        tituloInfo.grid(row=0, column=0, pady=(5, 2))

        subt = ctk.CTkLabel(
            self.frameCabeza,
            text=f"Detalle del animal:  {fila[0]}",
            font=("poppins", 15, "normal"),
            text_color=T_NEGRO,
        )
        subt.grid(row=1, column=0, pady=(0, 5))

        self.frameCampos = ctk.CTkFrame(self.vInfo, fg_color="transparent")
        self.frameCampos.pack(fill="x", padx=10, pady=10)

        self.frameObservaciones = ctk.CTkFrame(self.vInfo, fg_color="transparent")
        self.frameObservaciones.pack(fill="both", expand=True, padx=10, pady=10)

        self.frameBotones = ctk.CTkFrame(self.vInfo, fg_color="transparent")
        self.frameBotones.pack(fill="x", padx=14, pady=(6, 12))
        self.frameBotones.grid_columnconfigure(0, weight=1)

        codigo = str(fila[0]) if len(fila) > 0 and fila[0] is not None else ""
        especie = str(fila[1]) if len(fila) > 1 and fila[1] is not None else ""
        sexo = str(fila[2]) if len(fila) > 2 and fila[2] is not None else ""
        fNacimiento = str(fila[3]) if len(fila) > 3 and fila[3] is not None else ""
        fIngreso = str(fila[4]) if len(fila) > 4 and fila[4] is not None else ""
        pesoInicial = str(fila[5]) if len(fila) > 5 and fila[5] is not None else ""
        estado_salud = str(fila[6]) if len(fila) > 6 and fila[6] is not None else ""
        observaciones = str(fila[7]) if len(fila) > 7 and fila[7] is not None else ""

        edad_calculada = self.controlador.calcular_edad(fNacimiento)

        def crear_campo_lectura(label_txt, valor_txt, row, col):
            lbl = ctk.CTkLabel(
                self.frameCampos,
                text=label_txt,
                font=T_CUERPO,
                text_color=T_NEGRO,
            )
            lbl.grid(row=row, column=col, pady=5, padx=(15, 3), sticky="e")

            entry = ctk.CTkEntry(
                self.frameCampos,
                font=T_CUERPO,
                fg_color="#FFFFFF",
                text_color=T_NEGRO,
            )
            entry.insert(0, valor_txt)
            entry.configure(state="disabled")
            entry.grid(row=row, column=col + 1, pady=5, padx=(15, 3))
            return entry

            # Fila 2
        crear_campo_lectura("Código:", codigo, row=2, col=0)
        crear_campo_lectura("Especie:", especie, row=2, col=2)

            # Fila 3
        crear_campo_lectura("Sexo:", sexo, row=3, col=0)
        crear_campo_lectura("Peso:", f"{pesoInicial} kg" if pesoInicial else "", row=3, col=2)

            # Fila 4
        crear_campo_lectura("Estado\nActual:", estado_salud, row=4, col=0)
        crear_campo_lectura("Fecha\nIngreso:", fIngreso, row=4, col=2)

            # Fila 5 (Fecha Nacimiento + Edad agregada)
        crear_campo_lectura("Fecha\nNacimiento:", fNacimiento, row=5, col=0)
        crear_campo_lectura("Edad:", edad_calculada, row=5, col=2)

        lbl_observaciones = ctk.CTkLabel(
            self.frameObservaciones,
            text="Observaciones:",
            font=T_CUERPO,
            text_color=T_NEGRO,
        )
        lbl_observaciones.pack(anchor="w", padx=4, pady=(0, 4))

        txt_observaciones = ctk.CTkTextbox(
            self.frameObservaciones,
            corner_radius=12,
            border_width=2,
            height=40,
            font=T_CUERPO,
            fg_color="#FFFFFF",
            text_color=T_NEGRO,
        )
        txt_observaciones.insert("1.0", observaciones if observaciones else "Sin observaciones")
        txt_observaciones.configure(state="disabled")
        txt_observaciones.pack(fill="both", expand=True)

        self.btn_cerrar = ctk.CTkButton(
            self.frameBotones,
            text="Cerrar",
            font=T_CUERPO,
            text_color=T_NEGRO,
            fg_color=VERDE_LIMA_BTN,
            corner_radius=20,
            command=self.vInfo.destroy,
        )
        self.btn_cerrar.grid(row=0, column=0, pady=(2, 0))


    def ventanaModificar(self,fila):
        self.vModificar = self.ventanaEmergente(520, 450)

        self.frameCabeza = ctk.CTkFrame(self.vModificar, fg_color="transparent")
        self.frameCabeza.pack(fill="x", padx=10, pady=10)
        self.frameCabeza.grid_columnconfigure(0, weight=1)

        tituloModificar = ctk.CTkLabel(
            self.frameCabeza,
            text="Modificar",
            font=EN_EMERGENTE,
            text_color=T_NEGRO,
        )
        tituloModificar.grid(row=0, column=0, pady=(5, 2))

        subt = ctk.CTkLabel(
            self.frameCabeza,
            text=f"Editar animal: {fila[0]}",
            font=("poppins", 15, "normal"),
            text_color=T_NEGRO,
        )
        subt.grid(row=1, column=0, pady=(0, 5))

        self.frameCampos = ctk.CTkFrame(self.vModificar, fg_color="transparent")
        self.frameCampos.pack(fill="x", padx=10, pady=10)

        self.frameObservaciones = ctk.CTkFrame(self.vModificar, fg_color="transparent")
        self.frameObservaciones.pack(fill="both", expand=True, padx=10, pady=10)

        self.frameBotones = ctk.CTkFrame(self.vModificar, fg_color="transparent")
        self.frameBotones.pack(fill="x", padx=14, pady=(6, 12))
        self.frameBotones.grid_columnconfigure(0, weight=1)
        self.frameBotones.grid_columnconfigure(1, weight=1)

        # Ajusta los índices según el orden de tu consulta:
        # [0]: código, [1]: especie, [2]: sexo, [3]: f_nacimiento, [4]: f_ingreso, [5]: peso, [6]: estado_salud, [7]: observaciones
        codigo_val = str(fila[0]) if len(fila) > 0 and fila[0] is not None else ""
        especie_val = str(fila[1]) if len(fila) > 1 and fila[1] is not None else ""
        sexo_val = str(fila[2]) if len(fila) > 2 and fila[2] is not None else ""
        f_nac_val = str(fila[3]) if len(fila) > 3 and fila[3] is not None else ""
        f_ing_val = str(fila[4]) if len(fila) > 4 and fila[4] is not None else ""
        peso_val = str(fila[5]) if len(fila) > 5 and fila[5] is not None else ""
        estado_val = str(fila[6]) if len(fila) > 6 and fila[6] is not None else ""
        obs_val = str(fila[7]) if len(fila) > 7 and fila[7] is not None else ""

        # Código (NO editable)
        lbl_codigo = ctk.CTkLabel(
            self.frameCampos, text="Código:", font=T_CUERPO, text_color=T_NEGRO
        )
        lbl_codigo.grid(row=2, column=0, pady=5, padx=(15, 3), sticky="e")
        self.codigo = ctk.CTkEntry(
            self.frameCampos, font=T_CUERPO, text_color=T_NEGRO
        )
        self.codigo.insert(0, codigo_val)
        self.codigo.configure(state="disabled")
        self.codigo.grid(row=2, column=1, pady=5, padx=(15, 3))

        # Especie
        lbl_especie = ctk.CTkLabel(
            self.frameCampos, text="Especie:", font=T_CUERPO, text_color=T_NEGRO
        )
        lbl_especie.grid(row=2, column=2, pady=5, padx=(15, 3), sticky="e")
        self.especie = ctk.CTkEntry(
            self.frameCampos, font=T_CUERPO, text_color=T_NEGRO
        )
        self.especie.insert(0, especie_val)
        self.especie.grid(row=2, column=3, pady=5, padx=(15, 3))

        # Sexo
        lbl_sexo = ctk.CTkLabel(
            self.frameCampos, text="Sexo:", font=T_CUERPO, text_color=T_NEGRO
        )
        lbl_sexo.grid(row=3, column=0, pady=5, padx=(15, 3), sticky="e")
        self.sexo = ctk.CTkEntry(
            self.frameCampos, font=T_CUERPO, text_color=T_NEGRO
        )
        self.sexo.insert(0, sexo_val)
        self.sexo.grid(row=3, column=1, pady=5, padx=(15, 3))

        # Peso
        lbl_peso = ctk.CTkLabel(
            self.frameCampos, text="Peso:", font=T_CUERPO, text_color=T_NEGRO
        )
        lbl_peso.grid(row=3, column=2, pady=5, padx=(15, 3), sticky="e")
        self.pesoInicial = ctk.CTkEntry(
            self.frameCampos, font=T_CUERPO, text_color=T_NEGRO
        )
        self.pesoInicial.insert(0, peso_val)
        self.pesoInicial.grid(row=3, column=3, pady=5, padx=(15, 3))

        # Estado Actual
        lbl_estado = ctk.CTkLabel(
            self.frameCampos, text="Estado\nActual:", font=T_CUERPO, text_color=T_NEGRO
        )
        lbl_estado.grid(row=4, column=0, pady=5, padx=(15, 3), sticky="e")
        self.estado_salud = ctk.CTkEntry(
            self.frameCampos, font=T_CUERPO, text_color=T_NEGRO
        )
        self.estado_salud.insert(0, estado_val)
        self.estado_salud.grid(row=4, column=1, pady=5, padx=(15, 3))

        # Fecha Ingreso
        lbl_f_ingreso = ctk.CTkLabel(
            self.frameCampos, text="Fecha\nIngreso:", font=T_CUERPO, text_color=T_NEGRO
        )
        lbl_f_ingreso.grid(row=4, column=2, pady=5, padx=(15, 3), sticky="e")
        self.fIngreso = ctk.CTkEntry(
            self.frameCampos, font=T_CUERPO, text_color=T_NEGRO
        )
        self.fIngreso.insert(0, f_ing_val)
        self.fIngreso.grid(row=4, column=3, pady=5, padx=(15, 3))

        # Fecha Nacimiento
        lbl_f_nac = ctk.CTkLabel(
            self.frameCampos,
            text="Fecha\nNacimiento:",
            font=T_CUERPO,
            text_color=T_NEGRO,
        )
        lbl_f_nac.grid(row=5, column=0, pady=5, padx=(15, 3), sticky="e")
        self.fNacimiento = ctk.CTkEntry(
            self.frameCampos, font=T_CUERPO, text_color=T_NEGRO
        )
        self.fNacimiento.insert(0, f_nac_val)
        self.fNacimiento.grid(row=5, column=1, pady=5, padx=(15, 3))

        # Observaciones
        lbl_obs = ctk.CTkLabel(
            self.frameObservaciones,
            text="Observaciones:",
            font=T_CUERPO,
            text_color=T_NEGRO,
        )
        lbl_obs.pack(anchor="w", padx=4, pady=(0, 4))
        self.observaciones = ctk.CTkTextbox(
            self.frameObservaciones,
            corner_radius=12,
            border_width=2,
            height=40,
            font=T_CUERPO,
            fg_color="#FFFFFF",
            text_color=T_NEGRO,
        )
        self.observaciones.insert("1.0", obs_val)
        self.observaciones.pack(fill="both", expand=True)

        # Botones
        self.btn_actualizar = ctk.CTkButton(
            self.frameBotones,
            text="Guardar cambios",
            font=T_CUERPO,
            text_color=T_NEGRO,
            fg_color=VERDE_LIMA_BTN,
            corner_radius=20,
            command= self.controlador.modificarController
        )
        self.btn_actualizar.grid(row=0, column=0, padx=(0, 8), sticky="e")

        self.btn_cancelar_mod = ctk.CTkButton(
            self.frameBotones,
            text="Cancelar",
            font=T_CUERPO,
            fg_color="transparent",
            border_width=2,
            border_color=ROJO_OSCURO,
            text_color=T_NEGRO,
            corner_radius=20,
            command=self.vModificar.destroy,
        )
        self.btn_cancelar_mod.grid(row=0, column=1, padx=(8, 0), sticky="w")

    def ventanaEliminar(self, fila):
        if not fila:
            return

        codigo_eliminar = str(fila[0]).strip()
        self.codigo_eliminar = codigo_eliminar
        self.controlador.eliminarController(codigo_eliminar)

if __name__ == "__main__":
    app = AnimalesCView()
    app.mainloop()