import sys
import os
import tkinter as tk
import customtkinter as ctk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from medicamentos.medicamentos import Medicamentos

ctk.set_appearance_mode("Light")

VERDE_OLIVA = "#84A91C"
VERDE_OLIVA_HOVER = "#6E8E14"
VERDE_HEADER_TABLA = "#C5D88A"
VERDE_BORDE_TABLA = "#9BB354"
VERDE_LIMA_BTN = "#8DB600"
VERDE_LIMA_HOVER = "#769900"
FONDO_BLANCO = "#FFFFFF"
FONDO_CREMA_MODAL = "#FBF8F1"
BORDE_CAFE_OSCURO = "#3B2618"
ROJO_PILDORA = "#E60000"
ROJO_OSCURO = "#B80000"
NEGRO_BORDE = "#1A1A1A"
COLOR_TRANSPARENTE = "#010101"


class VistaMedicamentos(ctk.CTkFrame):
    def __init__(self, master, volver_menu=None):
        super().__init__(master, fg_color=FONDO_BLANCO)
        self.volver_menu = volver_menu
        self.pack(fill="both", expand=True)

        self.registros_filtrados = []
        self.pagina_actual = 0
        self.filas_por_pagina = 15
        self.orden_actual = "id_asc"
        self.menu_filtro = None

        self.header = ctk.CTkFrame(self, fg_color=FONDO_BLANCO, height=75)
        self.header.pack(fill="x", padx=40, pady=(20, 10))

        self.btn_regresar = ctk.CTkButton(
            self.header,
            text="←",
            width=44,
            height=44,
            corner_radius=22,
            fg_color=VERDE_OLIVA,
            hover_color=VERDE_OLIVA_HOVER,
            text_color="#FFFFFF",
            font=("Arial", 25, "bold"),
            command=self.accion_regresar,
        )
        self.btn_regresar.pack(side="left", padx=(0, 20))

        self.lbl_titulo = ctk.CTkLabel(
            self.header,
            text="Medicamentos",
            font=("Arial", 30, "bold"),
            text_color="#111111",
            fg_color=FONDO_BLANCO,
        )
        self.lbl_titulo.pack(side="left")

        self.nav_frame = ctk.CTkFrame(self.header, fg_color=FONDO_BLANCO)
        self.nav_frame.pack(side="right")

        for item in ["Menú", "Especies", "Expediente", "Veterinarios", "Animales Cautiverio"]:
            if item == "Menú":
                btn_nav = ctk.CTkButton(
                    self.nav_frame,
                    text=item,
                    width=55,
                    height=28,
                    fg_color="transparent",
                    hover_color="#EEF5D8",
                    text_color="#111111",
                    font=("Arial", 15, "bold"),
                    command=self.accion_regresar,
                )
                btn_nav.pack(side="left", padx=8)
            else:
                lbl = ctk.CTkLabel(
                    self.nav_frame,
                    text=item,
                    font=("Arial", 18),
                    text_color="#444444",
                    fg_color=FONDO_BLANCO,
                )
                lbl.pack(side="left", padx=12)

        self.search_bar_frame = ctk.CTkFrame(self, fg_color=FONDO_BLANCO)
        self.search_bar_frame.pack(fill="x", padx=45, pady=(10, 18))

        self.entry_buscar = ctk.CTkEntry(
            self.search_bar_frame,
            placeholder_text="Buscar medicamento...",
            height=42,
            corner_radius=21,
            border_color=NEGRO_BORDE,
            border_width=2,
            fg_color=FONDO_BLANCO,
            text_color="#111111",
            placeholder_text_color="#666666",
            font=("Arial", 15),
        )
        self.entry_buscar.pack(side="left", fill="x", expand=True, padx=(0, 14))
        self.entry_buscar.bind("<KeyRelease>", self.filtrar_tabla)

        self.btn_filtro = ctk.CTkButton(
            self.search_bar_frame,
            text="☰",
            width=44,
            height=42,
            corner_radius=12,
            fg_color=FONDO_BLANCO,
            hover_color="#F0F0F0",
            text_color="#111111",
            font=("Arial", 22, "bold"),
            command=self.toggle_menu_filtro,
        )
        self.btn_filtro.pack(side="left", padx=(0, 18))

        self.btn_anadir = ctk.CTkButton(
            self.search_bar_frame,
            text="Añadir Medicamento",
            width=195,
            height=42,
            corner_radius=14,
            fg_color=VERDE_OLIVA,
            hover_color=VERDE_OLIVA_HOVER,
            border_color=NEGRO_BORDE,
            border_width=1.5,
            text_color="#FFFFFF",
            font=("Arial", 15, "bold"),
            command=self.abrir_modal_agregar,
        )
        self.btn_anadir.pack(side="right")

        self.tabla_outer = tk.Frame(
            self,
            bg=VERDE_BORDE_TABLA,
            bd=0,
            highlightthickness=1,
            highlightbackground=VERDE_BORDE_TABLA,
        )
        self.tabla_outer.pack(fill="both", expand=True, padx=45, pady=(0, 12))

        self.header_tabla = tk.Frame(
            self.tabla_outer,
            bg=VERDE_HEADER_TABLA,
            height=38,
        )
        self.header_tabla.pack(fill="x", pady=(0, 1))
        self.header_tabla.pack_propagate(False)

        self.pesos_columnas = [1, 2, 4, 3, 3, 2, 2]
        encabezados = ["N°", "Código", "Nombre", "Tipo", "Laboratorio", "Stock", "Acciones"]

        for col_idx, texto in enumerate(encabezados):
            self.header_tabla.grid_columnconfigure(
                col_idx, weight=self.pesos_columnas[col_idx], uniform="col"
            )
            self.header_tabla.grid_rowconfigure(0, weight=1)
            alineacion = "center" if col_idx in (0, 6) else "w"
            lbl = tk.Label(
                self.header_tabla,
                text=texto,
                font=("Arial", 15, "bold"),
                fg="#111111",
                bg=VERDE_HEADER_TABLA,
                anchor=alineacion,
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
            for c in range(6):
                fila_frame.grid_columnconfigure(
                    c, weight=self.pesos_columnas[c], uniform="col"
                )
                fila_frame.grid_rowconfigure(0, weight=1)
                lbl = tk.Label(
                    fila_frame,
                    text="",
                    font=("Arial", 15, "bold" if c == 0 else "normal"),
                    fg="#111111",
                    bg=FONDO_BLANCO,
                    anchor="w" if c > 0 else "center",
                )
                lbl.grid(row=0, column=c, sticky="ew", padx=10)
                celdas.append(lbl)

            fila_frame.grid_columnconfigure(
                6, weight=self.pesos_columnas[6], uniform="col"
            )
            acciones_box = tk.Frame(fila_frame, bg=FONDO_BLANCO)
            acciones_box.grid(row=0, column=6, sticky="nsew")

            inner_icons = tk.Frame(acciones_box, bg=FONDO_BLANCO)
            inner_icons.place(relx=0.5, rely=0.5, anchor="center")

            lbl_ver = tk.Label(
                inner_icons,
                text="👁",
                font=("Segoe UI Symbol", 15),
                fg="#111111",
                bg=FONDO_BLANCO,
            )
            lbl_ver.pack(side="left", padx=5)

            lbl_del = tk.Label(
                inner_icons,
                text="🗑",
                font=("Segoe UI Symbol", 15),
                fg="#111111",
                bg=FONDO_BLANCO,
            )
            lbl_del.pack(side="left", padx=5)

            lbl_edit = tk.Label(
                inner_icons,
                text="📝",
                font=("Segoe UI Symbol", 15),
                fg="#111111",
                bg=FONDO_BLANCO,
            )
            lbl_edit.pack(side="left", padx=5)

            celdas.append((lbl_ver, lbl_del, lbl_edit))
            self.filas_widgets.append(celdas)

        self.paginacion_frame = ctk.CTkFrame(self, fg_color=FONDO_BLANCO, height=34)
        self.paginacion_frame.pack(pady=(6, 16))

        self.puntos_btn = []
        for i in range(3):
            btn_p = ctk.CTkButton(
                self.paginacion_frame,
                text="",
                width=22,
                height=22,
                corner_radius=11,
                fg_color="#A8A8A8" if i == 0 else "#555555",
                hover_color=VERDE_OLIVA,
                command=lambda idx=i: self.cambiar_pagina(idx),
            )
            btn_p.pack(side="left", padx=6)
            self.puntos_btn.append(btn_p)

        self.cargar_datos()

    def accion_regresar(self):
        if self.menu_filtro and self.menu_filtro.winfo_exists():
            self.menu_filtro.destroy()
            self.menu_filtro = None

        if self.volver_menu:
            self.volver_menu()
        else:
            from main import MenuPrincipal
            root = self.winfo_toplevel()
            self.destroy()
            MenuPrincipal(root)

    def toggle_menu_filtro(self):
        if self.menu_filtro and self.menu_filtro.winfo_exists():
            self.menu_filtro.destroy()
            self.menu_filtro = None
            return

        self.menu_filtro = ctk.CTkFrame(
            self,
            fg_color=FONDO_BLANCO,
            border_color=NEGRO_BORDE,
            border_width=2,
            corner_radius=14,
        )

        opciones = [
            ("Código: Ascendente (1 → 9)", "id_asc"),
            ("Código: Descendente (9 → 1)", "id_desc"),
            ("Nombre: A → Z", "nom_asc"),
            ("Nombre: Z → A", "nom_desc"),
            ("Stock: Menor a Mayor", "stk_asc"),
            ("Stock: Mayor a Menor", "stk_desc"),
        ]

        for texto, clave in opciones:
            activo = self.orden_actual == clave
            btn = ctk.CTkButton(
                self.menu_filtro,
                text=texto,
                width=235,
                height=32,
                corner_radius=8,
                anchor="w",
                fg_color=VERDE_HEADER_TABLA if activo else FONDO_BLANCO,
                hover_color="#EEF5D8",
                text_color="#111111",
                font=("Arial", 15, "bold" if activo else "normal"),
                command=lambda c=clave: self.aplicar_orden(c),
            )
            btn.pack(padx=8, pady=4)

        self.update_idletasks()
        y_debajo_barra = self.search_bar_frame.winfo_y() + self.search_bar_frame.winfo_height() + 4
        self.menu_filtro.place(relx=1.0, x=-245, y=y_debajo_barra, anchor="ne")
        self.menu_filtro.lift()

    def aplicar_orden(self, clave):
        self.orden_actual = clave
        if self.menu_filtro and self.menu_filtro.winfo_exists():
            self.menu_filtro.destroy()
            self.menu_filtro = None
        self.ordenar_registros()
        self.pagina_actual = 0
        self.renderizar_tabla()

    def ordenar_registros(self):
        def clave_id(x):
            val = str(x[0])
            return (0, int(val)) if val.isdigit() else (1, val.lower())

        if self.orden_actual == "id_asc":
            self.registros_filtrados.sort(key=clave_id)
        elif self.orden_actual == "id_desc":
            self.registros_filtrados.sort(key=clave_id, reverse=True)
        elif self.orden_actual == "nom_asc":
            self.registros_filtrados.sort(key=lambda x: str(x[1]).lower())
        elif self.orden_actual == "nom_desc":
            self.registros_filtrados.sort(key=lambda x: str(x[1]).lower(), reverse=True)
        elif self.orden_actual == "stk_asc":
            self.registros_filtrados.sort(key=lambda x: int(x[4]))
        elif self.orden_actual == "stk_desc":
            self.registros_filtrados.sort(key=lambda x: int(x[4]), reverse=True)

    def cargar_datos(self):
        self.registros_filtrados = list(Medicamentos.mostrar())
        self.ordenar_registros()
        self.pagina_actual = 0
        self.renderizar_tabla()

    def filtrar_tabla(self, event=None):
        criterio = self.entry_buscar.get().strip()
        self.registros_filtrados = list(
            Medicamentos.filtrar(criterio) if criterio else Medicamentos.mostrar()
        )
        self.ordenar_registros()
        self.pagina_actual = 0
        self.renderizar_tabla()

    def cambiar_pagina(self, idx):
        self.pagina_actual = idx
        for i, b in enumerate(self.puntos_btn):
            b.configure(fg_color="#A8A8A8" if i == idx else "#555555")
        self.renderizar_tabla()

    def renderizar_tabla(self):
        inicio = self.pagina_actual * self.filas_por_pagina
        pagina_datos = self.registros_filtrados[inicio : inicio + self.filas_por_pagina]

        for idx_fila in range(self.filas_por_pagina):
            celdas = self.filas_widgets[idx_fila]
            lbl_ver, lbl_del, lbl_edit = celdas[6]

            if idx_fila < len(pagina_datos):
                med = pagina_datos[idx_fila]
                num_global = inicio + idx_fila + 1
                valores = [
                    str(num_global),
                    str(med[0]),
                    str(med[1]),
                    str(med[2]),
                    str(med[3]),
                    str(med[4]),
                ]
                for c_idx, val in enumerate(valores):
                    celdas[c_idx].configure(text=val)

                lbl_ver.configure(text="👁", cursor="hand2")
                lbl_del.configure(text="🗑", cursor="hand2")
                lbl_edit.configure(text="📝", cursor="hand2")

                lbl_ver.bind("<Button-1>", lambda e, m=med: self.abrir_modal_info(m))
                lbl_del.bind("<Button-1>", lambda e, m=med: self.confirmar_eliminar(m))
                lbl_edit.bind("<Button-1>", lambda e, m=med: self.abrir_modal_modificar(m))
            else:
                for c_idx in range(6):
                    celdas[c_idx].configure(text="")
                for ic in (lbl_ver, lbl_del, lbl_edit):
                    ic.configure(text="", cursor="")
                    ic.unbind("<Button-1>")

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
        alerta = self._crear_ventana_redondeada(padre, 400, 195)

        caja = ctk.CTkFrame(
            alerta,
            fg_color=FONDO_BLANCO,
            border_color=NEGRO_BORDE,
            border_width=2,
            corner_radius=22,
            bg_color=COLOR_TRANSPARENTE,
        )
        caja.pack(fill="both", expand=True)

        lbl = ctk.CTkLabel(
            caja,
            text=mensaje,
            font=("Arial", 17),
            text_color="#111111",
            fg_color=FONDO_BLANCO,
            wraplength=330,
            justify="center",
        )
        lbl.pack(expand=True, padx=24, pady=(22, 8))

        btns = ctk.CTkFrame(caja, fg_color=FONDO_BLANCO)
        btns.pack(pady=(0, 20))

        def aceptar():
            alerta.destroy()
            if al_aceptar:
                al_aceptar()

        ctk.CTkButton(
            btns,
            text="Aceptar",
            width=96,
            height=32,
            corner_radius=16,
            fg_color=VERDE_LIMA_BTN,
            hover_color=VERDE_LIMA_HOVER,
            border_color=NEGRO_BORDE,
            border_width=1,
            text_color="#111111",
            font=("Arial", 17, "bold"),
            command=aceptar,
        ).pack(side="left", padx=12)

        if tipo == "confirmar":
            ctk.CTkButton(
                btns,
                text="Cancelar",
                width=96,
                height=32,
                corner_radius=16,
                fg_color=FONDO_BLANCO,
                hover_color="#FFEBEB",
                border_color=ROJO_PILDORA,
                border_width=1,
                text_color="#111111",
                font=("Arial", 17),
                command=alerta.destroy,
            ).pack(side="left", padx=12)

    def _construir_formulario_modal(self, parent, titulo_modal, subtitulo_modal, valores=None, modo="agregar"):
        top = ctk.CTkFrame(parent, fg_color=FONDO_CREMA_MODAL)
        top.pack(fill="x", padx=24, pady=(16, 8))

        ctk.CTkButton(
            top,
            text="✕",
            width=32,
            height=32,
            corner_radius=16,
            fg_color=ROJO_PILDORA,
            hover_color=ROJO_OSCURO,
            border_color=NEGRO_BORDE,
            border_width=1,
            text_color="#111111",
            font=("Arial", 15),
            command=parent.master.destroy,
        ).pack(side="right", anchor="n")

        titulos_box = ctk.CTkFrame(top, fg_color=FONDO_CREMA_MODAL)
        titulos_box.pack(expand=True, padx=(32, 0))

        ctk.CTkLabel(
            titulos_box,
            text=titulo_modal,
            font=("Arial", 26),
            text_color="#111111",
            fg_color=FONDO_CREMA_MODAL,
        ).pack()

        ctk.CTkLabel(
            titulos_box,
            text=subtitulo_modal,
            font=("Arial", 15),
            text_color="#111111",
            fg_color=FONDO_CREMA_MODAL,
        ).pack()

        campos_frame = tk.Frame(parent, bg=FONDO_CREMA_MODAL)
        campos_frame.pack(fill="x", padx=40, pady=(10, 10))
        campos_frame.grid_columnconfigure(0, weight=1)
        campos_frame.grid_columnconfigure(1, weight=1)

        col_izq = tk.Frame(campos_frame, bg=FONDO_CREMA_MODAL)
        col_izq.grid(row=0, column=0, sticky="nw", padx=(0, 16))

        col_der = tk.Frame(campos_frame, bg=FONDO_CREMA_MODAL)
        col_der.grid(row=0, column=1, sticky="nw", padx=(16, 0))

        v = valores or ("", "", "", "", "", "")
        solo_lectura = modo == "info"
        bloquear_id = modo in ("info", "modificar")

        def crear_campo(contenedor, fila, etiqueta, valor, bloqueado=False):
            tk.Label(
                contenedor,
                text=etiqueta,
                font=("Arial", 15),
                fg="#111111",
                bg=FONDO_CREMA_MODAL,
                anchor="w",
            ).grid(row=fila, column=0, sticky="w", pady=6, padx=(0, 8))

            ent = tk.Entry(
                contenedor,
                width=19,
                font=("Arial", 15),
                bg=FONDO_BLANCO,
                disabledbackground=FONDO_BLANCO,
                disabledforeground="#111111",
                fg="#111111",
                bd=1,
                relief="solid",
            )
            ent.grid(row=fila, column=1, sticky="w", pady=6, ipady=3)
            if valor != "":
                ent.insert(0, str(valor))
            if bloqueado:
                ent.configure(state="disabled")
            return ent

        e_id = crear_campo(col_izq, 0, "Código:", v[0], bloqueado=bloquear_id)
        e_nombre = crear_campo(col_izq, 1, "Nombre:", v[1], bloqueado=solo_lectura)
        e_tipo = crear_campo(col_izq, 2, "Tipo:", v[2], bloqueado=solo_lectura)

        e_lab = crear_campo(col_der, 0, "Laboratorio:", v[3], bloqueado=solo_lectura)
        e_stock = crear_campo(col_der, 1, "Stock:", v[4], bloqueado=solo_lectura)

        tk.Label(
            parent,
            text="Información:",
            font=("Arial", 15, "bold"),
            fg="#111111",
            bg=FONDO_CREMA_MODAL,
            anchor="w",
        ).pack(fill="x", padx=40, pady=(4, 2))

        desc_box = ctk.CTkFrame(
            parent,
            fg_color=FONDO_BLANCO,
            border_color=BORDE_CAFE_OSCURO,
            border_width=2,
            corner_radius=16,
            bg_color=FONDO_CREMA_MODAL,
        )
        desc_box.pack(fill="x", padx=40, pady=(0, 14))

        txt_desc = tk.Text(
            desc_box,
            height=4,
            bd=0,
            highlightthickness=0,
            bg=FONDO_BLANCO,
            fg="#111111",
            font=("Arial", 15),
            wrap="word",
        )
        txt_desc.pack(fill="x", padx=12, pady=8)
        if v[5]:
            txt_desc.insert("1.0", str(v[5]))
        if solo_lectura:
            txt_desc.configure(state="disabled")

        return e_id, e_nombre, e_tipo, e_lab, e_stock, txt_desc

    def abrir_modal_agregar(self):
        modal = self._crear_ventana_redondeada(self.winfo_toplevel(), 600, 440)

        marco = ctk.CTkFrame(
            modal,
            fg_color=FONDO_CREMA_MODAL,
            border_color=BORDE_CAFE_OSCURO,
            border_width=3,
            corner_radius=18,
            bg_color=COLOR_TRANSPARENTE,
        )
        marco.pack(fill="both", expand=True)

        e_id, e_nombre, e_tipo, e_lab, e_stock, txt_desc = self._construir_formulario_modal(
            marco, "Añadir", "Nuevo Medicamento", modo="agregar"
        )

        btns = ctk.CTkFrame(marco, fg_color=FONDO_CREMA_MODAL)
        btns.pack(anchor="e", padx=40, pady=(2, 18))

        def guardar():
            id_m = e_id.get().strip()
            nom = e_nombre.get().strip()
            tip = e_tipo.get().strip()
            lab = e_lab.get().strip()
            stk = e_stock.get().strip()
            desc = txt_desc.get("1.0", "end").strip()

            if not all([id_m, nom, tip, lab, stk, desc]) or not id_m.isdigit() or not stk.isdigit():
                self.mostrar_alerta_figma(
                    modal, "Datos incorrectos. Verifique la información ingresada."
                )
                return

            nuevo = Medicamentos(int(id_m), nom, tip, lab, int(stk), desc)
            if nuevo.insertar():
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
            width=96,
            height=32,
            corner_radius=16,
            fg_color=VERDE_LIMA_BTN,
            hover_color=VERDE_LIMA_HOVER,
            border_color=NEGRO_BORDE,
            border_width=1,
            text_color="#111111",
            font=("Arial", 15, "bold"),
            command=guardar,
        ).pack(side="left", padx=6)

        ctk.CTkButton(
            btns,
            text="Cancelar",
            width=96,
            height=32,
            corner_radius=16,
            fg_color=FONDO_BLANCO,
            hover_color="#FFEBEB",
            border_color=ROJO_PILDORA,
            border_width=1,
            text_color="#111111",
            font=("Arial", 15),
            command=modal.destroy,
        ).pack(side="left", padx=6)

    def abrir_modal_info(self, med):
        modal = self._crear_ventana_redondeada(self.winfo_toplevel(), 600, 410)

        marco = ctk.CTkFrame(
            modal,
            fg_color=FONDO_CREMA_MODAL,
            border_color=BORDE_CAFE_OSCURO,
            border_width=3,
            corner_radius=18,
            bg_color=COLOR_TRANSPARENTE,
        )
        marco.pack(fill="both", expand=True)

        self._construir_formulario_modal(
            marco, "Información", f"Medicamento: {med[0]}", valores=med, modo="info"
        )

    def abrir_modal_modificar(self, med):
        modal = self._crear_ventana_redondeada(self.winfo_toplevel(), 600, 440)

        marco = ctk.CTkFrame(
            modal,
            fg_color=FONDO_CREMA_MODAL,
            border_color=BORDE_CAFE_OSCURO,
            border_width=3,
            corner_radius=18,
            bg_color=COLOR_TRANSPARENTE,
        )
        marco.pack(fill="both", expand=True)

        e_id, e_nombre, e_tipo, e_lab, e_stock, txt_desc = self._construir_formulario_modal(
            marco, "Modificar", f"Medicamento: {med[0]}", valores=med, modo="modificar"
        )

        btns = ctk.CTkFrame(marco, fg_color=FONDO_CREMA_MODAL)
        btns.pack(anchor="e", padx=40, pady=(2, 18))

        def ejecutar_modificar():
            nom = e_nombre.get().strip()
            tip = e_tipo.get().strip()
            lab = e_lab.get().strip()
            stk = e_stock.get().strip()
            desc = txt_desc.get("1.0", "end").strip()

            if not all([nom, tip, lab, stk, desc]) or not stk.isdigit():
                self.mostrar_alerta_figma(
                    modal, "Datos incorrectos. Verifique la información ingresada."
                )
                return

            def guardar_cambios():
                actualizado = Medicamentos(med[0], nom, tip, lab, int(stk), desc)
                if actualizado.actualizar():
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

        ctk.CTkButton(
            btns,
            text="Guardar",
            width=96,
            height=32,
            corner_radius=16,
            fg_color=VERDE_LIMA_BTN,
            hover_color=VERDE_LIMA_HOVER,
            border_color=NEGRO_BORDE,
            border_width=1,
            text_color="#111111",
            font=("Arial", 13, "bold"),
            command=ejecutar_modificar,
        ).pack(side="left", padx=6)

        ctk.CTkButton(
            btns,
            text="Cancelar",
            width=96,
            height=32,
            corner_radius=16,
            fg_color=FONDO_BLANCO,
            hover_color="#FFEBEB",
            border_color=ROJO_PILDORA,
            border_width=1,
            text_color="#111111",
            font=("Arial", 13),
            command=modal.destroy,
        ).pack(side="left", padx=6)

    def confirmar_eliminar(self, med):
        def borrar_registro():
            if Medicamentos.eliminar(med[0]):
                def refrescar():
                    self.cargar_datos()

                self.mostrar_alerta_figma(
                    self.winfo_toplevel(),
                    "Acción realizada con éxito",
                    al_aceptar=refrescar,
                )
            else:
                self.mostrar_alerta_figma(
                    self.winfo_toplevel(),
                    "En este momento no se pudo realizar la acción. Por favor, inténtelo de nuevo más tarde.",
                )

        self.mostrar_alerta_figma(
            self.winfo_toplevel(),
            "¿Estas seguro que deseas eliminar este registro?",
            tipo="confirmar",
            al_aceptar=borrar_registro,
        )


if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Parque Ecológico El Tecuán - Medicamentos")
    app.geometry("1280x760")
    VistaMedicamentos(app)
    app.mainloop()