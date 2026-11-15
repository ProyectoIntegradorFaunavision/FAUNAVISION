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
VERDE_LIMA_BTN = "#A3D900"
VERDE_LIMA_HOVER = "#8AB800"
FONDO_BLANCO = "#FFFFFF"
FONDO_CREMA_MODAL = "#FBF8F1"
BORDE_CAFE_OSCURO = "#3B2618"
ROJO_PILDORA = "#FF0000"
ROJO_OSCURO = "#CC0000"
NEGRO_BORDE = "#1A1A1A"
COLOR_TRANSPARENTE = "#010101"


class VistaMedicamentos(ctk.CTkFrame):
    def __init__(self, master, volver_menu=None):
        super().__init__(master, fg_color=FONDO_BLANCO)
        self.volver_menu = volver_menu
        self.pack(fill="both", expand=True)

        self.registros_filtrados = []
        self.pagina_actual = 0
        self.filas_por_pagina = 13

        self.header = ctk.CTkFrame(self, fg_color=FONDO_BLANCO, height=65)
        self.header.pack(fill="x", padx=35, pady=(18, 8))

        self.btn_regresar = ctk.CTkButton(
            self.header,
            text="←",
            width=36,
            height=36,
            corner_radius=18,
            fg_color=VERDE_OLIVA,
            hover_color=VERDE_OLIVA_HOVER,
            text_color="#FFFFFF",
            font=("Arial", 18, "bold"),
            command=self.accion_regresar,
        )
        self.btn_regresar.pack(side="left", padx=(0, 18))

        self.lbl_titulo = ctk.CTkLabel(
            self.header,
            text="Medicamentos",
            font=("Arial", 22),
            text_color="#111111",
            fg_color=FONDO_BLANCO,
        )
        self.lbl_titulo.pack(side="left")

        self.nav_frame = ctk.CTkFrame(self.header, fg_color=FONDO_BLANCO)
        self.nav_frame.pack(side="right")

        for item in ["Menú", "Especies", "Animales Cautiverio", "Expediente", "Veterinarios"]:
            lbl = ctk.CTkLabel(
                self.nav_frame,
                text=item,
                font=("Arial", 11),
                text_color="#222222",
                fg_color=FONDO_BLANCO,
            )
            lbl.pack(side="left", padx=10)

        self.search_bar_frame = ctk.CTkFrame(self, fg_color=FONDO_BLANCO)
        self.search_bar_frame.pack(fill="x", padx=45, pady=(10, 18))

        self.entry_buscar = ctk.CTkEntry(
            self.search_bar_frame,
            placeholder_text="Buscar",
            height=36,
            corner_radius=18,
            border_color=NEGRO_BORDE,
            border_width=2,
            fg_color=FONDO_BLANCO,
            text_color="#111111",
            placeholder_text_color="#666666",
            font=("Arial", 12),
        )
        self.entry_buscar.pack(side="left", fill="x", expand=True, padx=(0, 22))
        self.entry_buscar.bind("<KeyRelease>", self.filtrar_tabla)

        self.btn_anadir = ctk.CTkButton(
            self.search_bar_frame,
            text="Añadir Medicamento",
            width=155,
            height=34,
            corner_radius=12,
            fg_color=VERDE_OLIVA,
            hover_color=VERDE_OLIVA_HOVER,
            text_color="#111111",
            font=("Arial", 12),
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
        self.tabla_outer.pack(fill="both", expand=True, padx=45, pady=(0, 10))

        self.header_tabla = tk.Frame(
            self.tabla_outer,
            bg=VERDE_HEADER_TABLA,
            height=30,
        )
        self.header_tabla.pack(fill="x", pady=(0, 1))
        self.header_tabla.pack_propagate(False)

        self.pesos_columnas = [1, 2, 4, 3, 3, 2, 2]
        encabezados = ["N°", "ID", "Nombre / Vacuna", "Tipo", "Laboratorio", "Stock", ""]

        for col_idx, texto in enumerate(encabezados):
            self.header_tabla.grid_columnconfigure(
                col_idx, weight=self.pesos_columnas[col_idx], uniform="col"
            )
            self.header_tabla.grid_rowconfigure(0, weight=1)
            lbl = tk.Label(
                self.header_tabla,
                text=texto,
                font=("Arial", 10),
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
            for c in range(7):
                fila_frame.grid_columnconfigure(
                    c, weight=self.pesos_columnas[c], uniform="col"
                )
                fila_frame.grid_rowconfigure(0, weight=1)
                lbl = tk.Label(
                    fila_frame,
                    text="",
                    font=("Arial", 10),
                    fg=VERDE_OLIVA if c == 6 else "#111111",
                    bg=FONDO_BLANCO,
                    anchor="w" if c > 0 else "center",
                )
                lbl.grid(row=0, column=c, sticky="ew", padx=10)
                celdas.append(lbl)

            self.filas_widgets.append(celdas)

        self.paginacion_frame = ctk.CTkFrame(self, fg_color=FONDO_BLANCO, height=30)
        self.paginacion_frame.pack(pady=(4, 14))

        self.puntos_btn = []
        for i in range(3):
            btn_p = ctk.CTkButton(
                self.paginacion_frame,
                text="",
                width=18,
                height=18,
                corner_radius=9,
                fg_color="#84A91C" if i == 0 else "#556614",
                hover_color=VERDE_OLIVA,
                command=lambda idx=i: self.cambiar_pagina(idx),
            )
            btn_p.pack(side="left", padx=5)
            self.puntos_btn.append(btn_p)

        self.cargar_datos()

    def accion_regresar(self):
        if self.volver_menu:
            self.volver_menu()
        else:
            self.winfo_toplevel().destroy()

    def cargar_datos(self):
        self.registros_filtrados = Medicamentos.mostrar()
        self.pagina_actual = 0
        self.renderizar_tabla()

    def filtrar_tabla(self, event=None):
        criterio = self.entry_buscar.get().strip()
        self.registros_filtrados = (
            Medicamentos.filtrar(criterio) if criterio else Medicamentos.mostrar()
        )
        self.pagina_actual = 0
        self.renderizar_tabla()

    def cambiar_pagina(self, idx):
        self.pagina_actual = idx
        for i, b in enumerate(self.puntos_btn):
            b.configure(fg_color="#84A91C" if i == idx else "#556614")
        self.renderizar_tabla()

    def renderizar_tabla(self):
        inicio = self.pagina_actual * self.filas_por_pagina
        pagina_datos = self.registros_filtrados[inicio : inicio + self.filas_por_pagina]

        for idx_fila in range(self.filas_por_pagina):
            celdas = self.filas_widgets[idx_fila]
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
                    "Ver más",
                ]
                for c_idx, val in enumerate(valores):
                    celdas[c_idx].configure(text=val)
                    if c_idx == 6:
                        celdas[c_idx].configure(cursor="hand2")
                        celdas[c_idx].bind(
                            "<Button-1>", lambda e, m=med: self.abrir_modal_detalle(m)
                        )
                    else:
                        celdas[c_idx].configure(cursor="")
                        celdas[c_idx].unbind("<Button-1>")
            else:
                for c_idx in range(7):
                    celdas[c_idx].configure(text="", cursor="")
                    celdas[c_idx].unbind("<Button-1>")

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
            font=("Arial", 11),
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
            font=("Arial", 10),
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
                font=("Arial", 10),
                command=alerta.destroy,
            ).pack(side="left", padx=8)

    def _crear_ficha_inputs(self, parent, valores=None, bloquear_id=False):
        grid_box = tk.Frame(
            parent,
            bg=NEGRO_BORDE,
            bd=0,
            highlightthickness=1,
            highlightbackground=NEGRO_BORDE,
        )
        grid_box.pack(fill="x", padx=28, pady=(8, 14))

        def celda(row, col, colspan, label_txt, val="", readonly=False):
            cell = tk.Frame(
                grid_box,
                bg=FONDO_BLANCO,
                height=25,
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
                font=("Arial", 9),
                fg="#666666" if not val else "#111111",
                bg=FONDO_BLANCO,
            )
            lbl.pack(side="left", padx=(6, 2))

            entry = tk.Entry(
                cell,
                bd=0,
                highlightthickness=0,
                bg=FONDO_BLANCO,
                disabledbackground=FONDO_BLANCO,
                disabledforeground="#111111",
                fg="#111111",
                font=("Arial", 9),
            )
            entry.pack(side="left", fill="both", expand=True, padx=(0, 6))
            if val != "":
                entry.insert(0, str(val))
            if readonly:
                entry.configure(state="disabled")
            return entry

        for c in range(6):
            grid_box.grid_columnconfigure(c, weight=1, uniform="ficha")

        v = valores or ("", "", "", "", "", "")
        e_id = celda(0, 0, 2, "ID:", v[0], readonly=bloquear_id)
        e_nombre = celda(0, 2, 4, "Nombre:", v[1])
        e_tipo = celda(1, 0, 3, "Tipo:", v[2])
        e_stock = celda(1, 3, 3, "Stock:", v[4])
        e_lab = celda(2, 0, 6, "Laboratorio:", v[3])

        desc_box = ctk.CTkFrame(
            parent,
            fg_color=FONDO_BLANCO,
            border_color=NEGRO_BORDE,
            border_width=2,
            corner_radius=16,
            bg_color=FONDO_CREMA_MODAL,
        )
        desc_box.pack(fill="x", padx=28, pady=(0, 14))

        ctk.CTkLabel(
            desc_box,
            text="Descripción:",
            font=("Arial", 10),
            text_color="#666666" if not v[5] else "#111111",
            fg_color=FONDO_BLANCO,
        ).pack(anchor="w", padx=12, pady=(6, 0))

        txt_desc = tk.Text(
            desc_box,
            height=4,
            bd=0,
            highlightthickness=0,
            bg=FONDO_BLANCO,
            fg="#111111",
            font=("Arial", 9),
            wrap="word",
        )
        txt_desc.pack(fill="x", padx=12, pady=(2, 10))
        if v[5]:
            txt_desc.insert("1.0", str(v[5]))

        return e_id, e_nombre, e_tipo, e_lab, e_stock, txt_desc

    def abrir_modal_agregar(self):
        modal = self._crear_ventana_redondeada(self.winfo_toplevel(), 470, 355)

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
            text="Ingresar nuevo Medicamento",
            font=("Arial", 13),
            text_color="#111111",
            fg_color=FONDO_CREMA_MODAL,
        ).pack(side="left", padx=(25, 0))

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
            font=("Arial", 12, "bold"),
            command=modal.destroy,
        ).pack(side="right")

        e_id, e_nombre, e_tipo, e_lab, e_stock, txt_desc = self._crear_ficha_inputs(marco)

        btns = ctk.CTkFrame(marco, fg_color=FONDO_CREMA_MODAL)
        btns.pack(pady=(2, 16))

        def guardar():
            id_m = e_id.get().strip()
            nom = e_nombre.get().strip()
            tip = e_tipo.get().strip()
            lab = e_lab.get().strip()
            stk = e_stock.get().strip()
            desc = txt_desc.get("1.0", "end").strip()

            if not all([id_m, nom, tip, lab, stk, desc]) or not stk.isdigit():
                self.mostrar_alerta_figma(
                    modal, "Datos incorrectos. Verifique la información ingresada."
                )
                return

            nuevo = Medicamentos(id_m, nom, tip, lab, int(stk), desc)
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
            width=85,
            height=24,
            corner_radius=12,
            fg_color=VERDE_LIMA_BTN,
            hover_color=VERDE_LIMA_HOVER,
            border_color=VERDE_OLIVA,
            border_width=1,
            text_color="#111111",
            font=("Arial", 10),
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
            font=("Arial", 10),
            command=modal.destroy,
        ).pack(side="left", padx=8)

    def abrir_modal_detalle(self, med):
        modal = self._crear_ventana_redondeada(self.winfo_toplevel(), 470, 355)

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
            text=f"Medicamento: {med[0]}",
            font=("Arial", 13),
            text_color="#111111",
            fg_color=FONDO_CREMA_MODAL,
        ).pack(side="left", padx=(25, 0))

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
            font=("Arial", 12, "bold"),
            command=modal.destroy,
        ).pack(side="right")

        e_id, e_nombre, e_tipo, e_lab, e_stock, txt_desc = self._crear_ficha_inputs(
            marco, valores=med, bloquear_id=True
        )

        btns = ctk.CTkFrame(marco, fg_color=FONDO_CREMA_MODAL)
        btns.pack(pady=(2, 16))

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

        def ejecutar_eliminar():
            def borrar_registro():
                if Medicamentos.eliminar(med[0]):
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
            font=("Arial", 10),
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
            font=("Arial", 10),
            command=ejecutar_eliminar,
        ).pack(side="left", padx=8)


if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Parque Ecológico El Tecuán - Medicamentos")
    app.geometry("950x600")
    VistaMedicamentos(app)
    app.mainloop()