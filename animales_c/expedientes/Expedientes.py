import sqlite3
import customtkinter as ctk
from tkinter import messagebox
import conexionBD  # Módulo de base de datos

# Configuración inicial del tema visual
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class Expedientes:
    """Clase encargada de la lógica de negocio y operaciones CRUD con la Base de Datos."""
    def __init__(
        self,
        id_historial=None,
        animal=None,
        veterinario=None,
        medicamento=None,
        fechaAplicacion=None,
        fechaProxima=None,
        tipo_evento=None,
        peso_actual=None,
        diagnostico_motivo=None,
    ):
        self._id_historial = id_historial
        self._animal = animal
        self._veterinario = veterinario
        self._medicamento = medicamento
        self._fechaAplicacion = fechaAplicacion
        self._fechaProxima = fechaProxima
        self._tipo_evento = tipo_evento
        self._peso_actual = peso_actual
        self._diagnostico_motivo = diagnostico_motivo

    # Propiedades (Getters)
    @property
    def id_historial(self):
        return self._id_historial

    @property
    def animal(self):
        return self._animal

    @property
    def veterinario(self):
        return self._veterinario

    @property
    def medicamento(self):
        return self._medicamento

    @property
    def fechaAplicacion(self):
        return self._fechaAplicacion

    @property
    def fechaProxima(self):
        return self._fechaProxima

    @property
    def tipo_evento(self):
        return self._tipo_evento

    @property
    def peso_actual(self):
        return self._peso_actual

    @property
    def diagnostico_motivo(self):
        return self._diagnostico_motivo

    # Setters
    @id_historial.setter
    def id_historial(self, id_historial):
        self._id_historial = id_historial

    @animal.setter
    def animal(self, animal):
        self._animal = animal

    @veterinario.setter
    def veterinario(self, veterinario):
        self._veterinario = veterinario

    @medicamento.setter
    def medicamento(self, medicamento):
        self._medicamento = medicamento

    @fechaAplicacion.setter
    def fechaAplicacion(self, fechaAplicacion):
        self._fechaAplicacion = fechaAplicacion

    @fechaProxima.setter
    def fechaProxima(self, fechaProxima):
        self._fechaProxima = fechaProxima

    @tipo_evento.setter
    def tipo_evento(self, tipo_evento):
        self._tipo_evento = tipo_evento

    @peso_actual.setter
    def peso_actual(self, peso_actual):
        self._peso_actual = peso_actual

    @diagnostico_motivo.setter
    def diagnostico_motivo(self, diagnostico_motivo):
        self._diagnostico_motivo = diagnostico_motivo

    def agregar(self):
        """Método CRUD interno para insertar el registro en la base de datos."""
        conexion = conexionBD.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("""
                    INSERT INTO expedientes 
                    (id_historial, animal, veterinario, medicamento, fechaAplicacion, fechaProxima, tipo_evento, peso_actual, diagnostico_motivo) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (self._id_historial, self._animal, self._veterinario, self._medicamento, 
                      self._fechaAplicacion, self._fechaProxima, self._tipo_evento, self._peso_actual, self._diagnostico_motivo))
                conexion.commit()
                conexion.close()
                return True
            except sqlite3.Error as e:
                conexion.close()
                raise e
        return False

    def actualizar(self):
        """Método CRUD interno para actualizar el registro en la base de datos."""
        conexion = conexionBD.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("""
                    UPDATE expedientes SET 
                    animal = ?, veterinario = ?, medicamento = ?, fechaAplicacion = ?, 
                    fechaProxima = ?, tipo_evento = ?, peso_actual = ?, diagnostico_motivo = ? 
                    WHERE id_historial = ?
                """, (self._animal, self._veterinario, self._medicamento, self._fechaAplicacion, 
                      self._fechaProxima, self._tipo_evento, self._peso_actual, self._diagnostico_motivo, self._id_historial))
                conexion.commit()
                conexion.close()
                return True
            except sqlite3.Error as e:
                conexion.close()
                raise e
        return False

    def borrar(self, id_historial=None):
        """Método CRUD interno para eliminar el registro de la base de datos."""
        target_id = id_historial if id_historial is not None else self._id_historial
        conexion = conexionBD.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM expedientes WHERE id_historial = ?", (target_id,))
                conexion.commit()
                conexion.close()
                return True
            except sqlite3.Error as e:
                conexion.close()
                raise e
        return False

    @staticmethod
    def mostrar(busqueda=""):
        """Método CRUD interno para consultar registros de la base de datos.
        Devuelve todas las columnas (la tabla solo muestra algunas, pero el
        formulario de edición y la ventana de detalle necesitan el registro completo)."""
        conexion = conexionBD.conectar()
        if not conexion:
            return []
        cursor = conexion.cursor()
        if busqueda:
            query = """
                SELECT id_historial, animal, veterinario, medicamento, fechaAplicacion, fechaProxima, tipo_evento, peso_actual, diagnostico_motivo 
                FROM expedientes WHERE tipo_evento LIKE ? OR diagnostico_motivo LIKE ? OR id_historial LIKE ?
            """
            param = f"%{busqueda}%"
            cursor.execute(query, (param, param, param))
        else:
            cursor.execute("SELECT id_historial, animal, veterinario, medicamento, fechaAplicacion, fechaProxima, tipo_evento, peso_actual, diagnostico_motivo FROM expedientes")
        registros = cursor.fetchall()
        conexion.close()
        return registros

    @staticmethod
    def obtener_detalle(id_historial):
        """Consulta un expediente completo junto con los nombres relacionados
        (especie del animal, nombre del veterinario y nombre del medicamento)."""
        conexion = conexionBD.conectar()
        if not conexion:
            return None
        try:
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT e.id_historial, e.animal, es.nombre_especie,
                       e.veterinario, v.nombre, v.apellido1, v.apellido2,
                       e.medicamento, m.nombre_medicamento,
                       e.fechaAplicacion, e.fechaProxima, e.tipo_evento,
                       e.peso_actual, e.diagnostico_motivo
                FROM expedientes e
                LEFT JOIN animales_c a ON a.codigo = e.animal
                LEFT JOIN especies es ON es.codigo = a.especie
                LEFT JOIN veterinarios v ON v.num_empleado = e.veterinario
                LEFT JOIN medicamentos m ON m.id_medicamento = e.medicamento
                WHERE e.id_historial = ?
            """, (id_historial,))
            fila = cursor.fetchone()
        finally:
            conexion.close()

        if not fila:
            return None

        partes_vet = [p for p in (fila[4], fila[5], fila[6]) if p]
        return {
            "id_historial": fila[0],
            "animal": fila[1],
            "especie": fila[2],
            "veterinario": fila[3],
            "nombre_vet": " ".join(partes_vet) if partes_vet else None,
            "medicamento": fila[7],
            "nombre_med": fila[8],
            "fechaAplicacion": fila[9],
            "fechaProxima": fila[10],
            "tipo_evento": fila[11],
            "peso_actual": fila[12],
            "diagnostico_motivo": fila[13],
        }

    def limpiar(self):
        """Limpia los atributos del objeto."""
        self._id_historial = None
        self._animal = None
        self._veterinario = None
        self._medicamento = None
        self._fechaAplicacion = None
        self._fechaProxima = None
        self._tipo_evento = None
        self._peso_actual = None
        self._diagnostico_motivo = None


class ExpedientesApp(ctk.CTk):
    """Clase encargada de la Interfaz Visual (CustomTkinter)."""

    # Columnas visibles de la tabla: (título, ancho). Se usan tanto en el
    # encabezado como en las filas para que siempre queden alineadas.
    COLUMNAS = [
        ("ID Hist.", 120),
        ("Animal", 150),
        ("Veterinario", 150),
        ("Medicamento", 150),
        ("F. Aplicación", 200),
        ("F. Próxima", 200),
        ("Acciones", 190),
    ]

    def __init__(self):
        super().__init__()

        # Inicializar base de datos
        conexionBD.crear_db()

        self.title("Parque Ecológico El Tecuán - Expedientes Médicos")
        self.geometry("1350x720")
        self.configure(fg_color="#FFFFFF")

        self.primary_color = "#C29B38"
        self.dark_text = "#2C2C2C"

        self.crear_header()
        self.crear_barra_busqueda()
        self.crear_contenedor_tabla()
        self.cargar_datos_tabla()

    def crear_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent", height=80)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)

        btn_back = ctk.CTkButton(
            header_frame, text="←", font=("Arial", 22, "bold"),
            fg_color="#76B900", hover_color="#659F00", text_color="#FFFFFF",
            width=45, height=45, corner_radius=22,
            command=lambda: print("Volver atrás")
        )
        btn_back.pack(side="left", padx=(0, 20))

        lbl_titulo = ctk.CTkLabel(
            header_frame, text="Expedientes",
            font=("Arial", 26, "bold"), text_color=self.dark_text
        )
        lbl_titulo.pack(side="left")

        lbl_logo = ctk.CTkLabel(
            header_frame, text="🌿 EL TECUÁN\nParque Ecológico",
            font=("Arial", 10, "bold"), text_color="#4A5D3E", justify="center"
        )
        lbl_logo.pack(side="right", padx=(20, 0))

        nav_items = ["Veterinarios", "Medicamentos", "Animales Cautiverio", "Especies", "Menú"]
        nav_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        nav_frame.pack(side="right", padx=10)

        for item in nav_items:
            btn_nav = ctk.CTkButton(
                nav_frame, text=item, fg_color="transparent",
                text_color=self.dark_text, hover_color="#EAEAEA",
                font=("Arial", 13), width=len(item) * 8 + 10,
                command=lambda i=item: print(f"Navegando a: {i}")
            )
            btn_nav.pack(side="right", padx=5)

    def crear_barra_busqueda(self):
        search_frame = ctk.CTkFrame(self, fg_color="transparent", height=60)
        search_frame.pack(fill="x", padx=20, pady=10)
        search_frame.pack_propagate(False)

        self.entry_buscar = ctk.CTkEntry(
            search_frame, placeholder_text="Buscar por tipo de evento, diagnóstico o ID...",
            font=("Arial", 14), fg_color="#FFFFFF", text_color=self.dark_text,
            border_color="#2C2C2C", border_width=2, corner_radius=25,
            height=45, width=450
        )
        self.entry_buscar.pack(side="left")
        self.entry_buscar.bind("<KeyRelease>", self.filtrar_tabla)

        btn_añadir = ctk.CTkButton(
            search_frame, text="Añadir Expediente", font=("Arial", 14, "bold"),
            fg_color=self.primary_color, hover_color="#A9842F", text_color="#FFFFFF",
            corner_radius=10, height=40, width=170,
            command=self.view_agregar  # <--- Llama al método visual view_agregar
        )
        btn_añadir.pack(side="right")

    def crear_contenedor_tabla(self):
        table_container = ctk.CTkFrame(
            self, fg_color="#FFFFFF", border_color=self.primary_color,
            border_width=2, corner_radius=6
        )
        table_container.pack(fill="both", expand=True, padx=20, pady=10)

        header_table = ctk.CTkFrame(table_container, fg_color=self.primary_color, corner_radius=0, height=40)
        header_table.pack(fill="x")
        header_table.pack_propagate(False)

        for col, width in self.COLUMNAS:
            lbl = ctk.CTkLabel(
                header_table, text=col, font=("Arial", 12, "bold"),
                text_color="#FFFFFF", width=width, anchor="center"
            )
            lbl.pack(side="left", padx=5)

        self.scroll_tabla = ctk.CTkScrollableFrame(
            table_container, fg_color="#FFFFFF", corner_radius=0
        )
        self.scroll_tabla.pack(fill="both", expand=True)

    def cargar_datos_tabla(self, busqueda=""):
        for widget in self.scroll_tabla.winfo_children():
            widget.destroy()

        registros = Expedientes.mostrar(busqueda)

        # Anchos de las columnas de datos (todas menos "Acciones")
        widths = [w for _, w in self.COLUMNAS[:-1]]
        ancho_acciones = self.COLUMNAS[-1][1]

        for reg in registros:
            # El registro trae los 9 campos; la tabla solo muestra los primeros 6.
            # El registro completo se usa para el detalle y la edición.
            id_hist, animal, vet, med, f_apli, f_prox = reg[:6]

            row_frame = ctk.CTkFrame(self.scroll_tabla, fg_color="#FFFFFF", corner_radius=0, height=40)
            row_frame.pack(fill="x")
            row_frame.pack_propagate(False)

            datos = [str(id_hist), str(animal), str(vet), str(med), str(f_apli), str(f_prox)]

            for i, val in enumerate(datos):
                lbl = ctk.CTkLabel(
                    row_frame, text=val, font=("Arial", 12),
                    text_color=self.dark_text, width=widths[i], anchor="center"
                )
                lbl.pack(side="left", padx=5)

            # --- Columna de acciones: ver / editar / eliminar ---
            actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent", width=ancho_acciones, height=40)
            actions_frame.pack(side="left", padx=5)
            actions_frame.pack_propagate(False)

            # Contenedor interno centrado para que los 3 botones queden al medio
            botones_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
            botones_frame.place(relx=0.5, rely=0.5, anchor="center")

            btn_ver = ctk.CTkButton(
                botones_frame, text="👁", font=("Arial", 15),
                fg_color="transparent", text_color="#2C2C2C",
                hover_color="#EAEAEA", width=34, height=30,
                command=lambda r=reg: self.view_detalle(r)  # <--- Abre la pantalla emergente
            )
            btn_ver.pack(side="left", padx=3)

            btn_editar = ctk.CTkButton(
                botones_frame, text="✏", font=("Arial", 15),
                fg_color="transparent", text_color="#2C2C2C",
                hover_color="#EAEAEA", width=34, height=30,
                command=lambda r=reg: self.view_actualizar(r)  # <--- Llama al método visual de actualización
            )
            btn_editar.pack(side="left", padx=3)

            btn_eliminar = ctk.CTkButton(
                botones_frame, text="🗑", font=("Arial", 15),
                fg_color="transparent", text_color="#2C2C2C",
                hover_color="#EAEAEA", width=34, height=30,
                command=lambda id_h=id_hist: self.view_borrar(id_h)  # <--- Llama al método visual de borrado
            )
            btn_eliminar.pack(side="left", padx=3)

            sep = ctk.CTkFrame(self.scroll_tabla, fg_color=self.primary_color, height=1, corner_radius=0)
            sep.pack(fill="x")

    def filtrar_tabla(self, event):
        texto = self.entry_buscar.get()
        self.cargar_datos_tabla(texto)

    # -------------------------------------------------------------
    # MÉTODOS DE VISTA (CustomTkinter UI)
    # -------------------------------------------------------------
    def view_agregar(self):
        """Área visual de CustomTkinter para añadir un nuevo expediente."""
        self.ventana_formulario("Añadir Expediente", guardar_cb=self._procesar_guardar_nuevo)

    def view_actualizar(self, registro):
        """Área visual de CustomTkinter para editar un expediente existente."""
        self.ventana_formulario("Editar Expediente", registro=registro, guardar_cb=self._procesar_guardar_actualizar)

    def view_borrar(self, id_historial):
        """Área visual de confirmación para borrar un expediente."""
        if messagebox.askyesno("Confirmar eliminación", f"¿Estás seguro de eliminar el expediente con ID {id_historial}?"):
            try:
                exp = Expedientes(id_historial=id_historial)
                exp.borrar()  # Llama al método CRUD interno
                self.cargar_datos_tabla()
                exp.limpiar()
                messagebox.showinfo("Éxito", "Expediente eliminado correctamente.")
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {e}")

    def view_detalle(self, registro):
        """Pantalla emergente (solo lectura) con la información completa del expediente,
        acomodada en forma de lista."""
        try:
            d = Expedientes.obtener_detalle(registro[0])
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo consultar el expediente: {e}")
            return

        if not d:
            messagebox.showerror("Error", "No se encontró el expediente seleccionado.")
            return

        def con_nombre(identificador, nombre):
            """Devuelve 'ID - Nombre' si existe el nombre, o solo el ID."""
            return f"{identificador} - {nombre}" if nombre else str(identificador)

        filas = [
            ("ID Historial:", str(d["id_historial"])),
            ("Animal:", con_nombre(d["animal"], d["especie"])),
            ("Veterinario:", con_nombre(d["veterinario"], d["nombre_vet"])),
            ("Medicamento:", con_nombre(d["medicamento"], d["nombre_med"])),
            ("Fecha de Aplicación:", str(d["fechaAplicacion"])),
            ("Fecha Próxima:", str(d["fechaProxima"])),
            ("Tipo de Evento:", str(d["tipo_evento"])),
            ("Peso Actual:", f"{d['peso_actual']} kg"),
            ("Diagnóstico / Motivo:", str(d["diagnostico_motivo"])),
        ]

        top = ctk.CTkToplevel(self)
        top.title("Detalle del Expediente")
        top.geometry("540x620")
        top.grab_set()
        top.configure(fg_color="#FFFFFF")

        # Encabezado con el mismo color de la tabla
        header = ctk.CTkFrame(top, fg_color=self.primary_color, corner_radius=0, height=55)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header, text=f"Expediente #{d['id_historial']}",
            font=("Arial", 18, "bold"), text_color="#FFFFFF"
        ).pack(side="left", padx=20)

        # Lista de datos (con scroll por si el diagnóstico es muy largo)
        lista = ctk.CTkScrollableFrame(top, fg_color="#FFFFFF", corner_radius=0)
        lista.pack(fill="both", expand=True, padx=15, pady=(10, 0))

        for etiqueta, valor in filas:
            fila = ctk.CTkFrame(lista, fg_color="transparent")
            fila.pack(fill="x", pady=6)

            ctk.CTkLabel(
                fila, text=etiqueta, font=("Arial", 12, "bold"),
                text_color=self.primary_color, width=160, anchor="nw", justify="left"
            ).pack(side="left", anchor="n", padx=(5, 10))

            ctk.CTkLabel(
                fila, text=valor, font=("Arial", 13),
                text_color=self.dark_text, anchor="w", justify="left", wraplength=290
            ).pack(side="left", anchor="n", fill="x", expand=True)

            ctk.CTkFrame(lista, fg_color="#E6E6E6", height=1, corner_radius=0).pack(fill="x")

        btn_cerrar = ctk.CTkButton(
            top, text="Cerrar", font=("Arial", 14, "bold"),
            fg_color=self.primary_color, hover_color="#A9842F", text_color="#FFFFFF",
            width=200, height=40, command=top.destroy
        )
        btn_cerrar.pack(pady=15)

    def ventana_formulario(self, titulo, registro=None, guardar_cb=None):
        """Construye la ventana flotante (Toplevel) con los campos de entrada en dos columnas."""
        top = ctk.CTkToplevel(self)
        top.title(titulo)
        top.geometry("760x640")
        top.grab_set()
        top.configure(fg_color="#FFFFFF")

        lbl_title = ctk.CTkLabel(top, text=titulo, font=("Arial", 18, "bold"), text_color=self.dark_text)
        lbl_title.pack(pady=15)

        # Columna izquierda: de ID Historial a Medicamento
        campos_izq = [
            ("ID Historial (Numérico):", str(registro[0]) if registro else ""),
            ("Animal (ID código):", str(registro[1]) if registro else ""),
            ("Veterinario (Núm. Empleado):", str(registro[2]) if registro else ""),
            ("Medicamento (ID):", str(registro[3]) if registro else ""),
        ]

        # Columna derecha: de Fecha Aplicación a Peso Actual
        campos_der = [
            ("Fecha Aplicación (AAAA-MM-DD):", str(registro[4]) if registro else ""),
            ("Fecha Próxima (AAAA-MM-DD):", str(registro[5]) if registro else ""),
            ("Tipo de Evento:", str(registro[6]) if registro else ""),
            ("Peso Actual (kg):", str(registro[7]) if registro else ""),
        ]

        # El diagnóstico va debajo de ambas columnas, en un recuadro de texto grande
        diag_default = str(registro[8]) if registro else ""

        contenedor = ctk.CTkFrame(top, fg_color="transparent")
        contenedor.pack(fill="x", padx=40)
        contenedor.grid_columnconfigure((0, 1), weight=1, uniform="columnas")

        col_izq = ctk.CTkFrame(contenedor, fg_color="transparent")
        col_izq.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

        col_der = ctk.CTkFrame(contenedor, fg_color="transparent")
        col_der.grid(row=0, column=1, sticky="nsew", padx=(15, 0))

        entries = {}
        for columna, campos in ((col_izq, campos_izq), (col_der, campos_der)):
            for label_text, default_val in campos:
                lbl = ctk.CTkLabel(columna, text=label_text, font=("Arial", 11), text_color=self.dark_text)
                lbl.pack(anchor="w")
                entry = ctk.CTkEntry(columna, font=("Arial", 12), height=32)
                entry.pack(fill="x", pady=(0, 10))
                entry.insert(0, default_val)

                if titulo == "Editar Expediente" and label_text.startswith("ID Historial"):
                    entry.configure(state="disabled")

                # Los campos de fecha ponen los separadores automáticamente mientras se escribe
                if label_text.startswith("Fecha"):
                    entry.bind("<KeyRelease>", lambda e, en=entry: self._formatear_fecha(en, e))

                entries[label_text] = entry

        lbl_diag = ctk.CTkLabel(top, text="Diagnóstico / Motivo:", font=("Arial", 11), text_color=self.dark_text)
        lbl_diag.pack(anchor="w", padx=40)

        txt_diag = ctk.CTkTextbox(
            top, font=("Arial", 12), height=140, wrap="word",
            border_width=2, border_color="#979DA2"
        )
        txt_diag.insert("1.0", diag_default)

        def ejecutar_accion():
            try:
                id_h = int(entries["ID Historial (Numérico):"].get().strip())
                animal = int(entries["Animal (ID código):"].get().strip())
                vet = int(entries["Veterinario (Núm. Empleado):"].get().strip())
                med = int(entries["Medicamento (ID):"].get().strip())
                f_apli = entries["Fecha Aplicación (AAAA-MM-DD):"].get().strip()
                f_prox = entries["Fecha Próxima (AAAA-MM-DD):"].get().strip()
                t_evento = entries["Tipo de Evento:"].get().strip()
                peso = float(entries["Peso Actual (kg):"].get().strip())
                diag = txt_diag.get("1.0", "end").strip()

                if not f_apli or not f_prox or not t_evento or not diag:
                    messagebox.showerror("Error", "Todos los campos de texto son obligatorios.")
                    return

                guardar_cb(id_h, animal, vet, med, f_apli, f_prox, t_evento, peso, diag, top)

            except ValueError:
                messagebox.showerror("Error", "Verifica que los IDs sean enteros y el peso sea un número válido.")

        btn_guardar = ctk.CTkButton(
            top, text="Guardar", font=("Arial", 14, "bold"),
            fg_color=self.primary_color, hover_color="#A9842F", text_color="#FFFFFF",
            width=300, height=40, command=ejecutar_accion
        )
        # Se empaqueta primero el botón (abajo) y luego el cuadro de texto, para que el
        # diagnóstico ocupe todo el espacio sobrante sin empujar el botón fuera de la ventana.
        btn_guardar.pack(side="bottom", pady=(5, 20))
        txt_diag.pack(fill="both", expand=True, padx=40, pady=(0, 10))

    @staticmethod
    def _formatear_fecha(entry, event=None):
        """Da formato AAAA-MM-DD mientras se escribe: solo acepta dígitos (máximo 8)
        y agrega los guiones automáticamente."""
        texto = entry.get()
        pos = entry.index("insert")
        digitos_antes = sum(c.isdigit() for c in texto[:pos])  # dígitos a la izquierda del cursor
        digitos = "".join(c for c in texto if c.isdigit())[:8]

        formato = digitos[:4]
        if len(digitos) > 4:
            formato += "-" + digitos[4:6]
        if len(digitos) > 6:
            formato += "-" + digitos[6:8]

        # El guion se agrega al terminar el año o el mes, solo al teclear un dígito
        # (así no estorba al borrar con retroceso ni al mover el cursor)
        if event is not None and event.char.isdigit() and len(digitos) in (4, 6):
            formato += "-"

        if formato == texto:
            return

        entry.delete(0, "end")
        entry.insert(0, formato)

        # Restaurar la posición del cursor
        if digitos_antes >= len(digitos):
            nueva_pos = len(formato)
        else:
            nueva_pos, contados = 0, 0
            while nueva_pos < len(formato) and contados < digitos_antes:
                if formato[nueva_pos].isdigit():
                    contados += 1
                nueva_pos += 1
        entry.icursor(nueva_pos)

    def _procesar_guardar_nuevo(self, id_h, animal, vet, med, f_apli, f_prox, t_evento, peso, diag, ventana):
        try:
            # Conecta la vista con el método CRUD 'agregar' de la clase de lógica
            exp = Expedientes(id_h, animal, vet, med, f_apli, f_prox, t_evento, peso, diag)
            exp.agregar()
            
            ventana.destroy()
            self.cargar_datos_tabla()
            exp.limpiar()
            messagebox.showinfo("Éxito", "Expediente añadido correctamente.")
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Error de Integridad", f"Verifica que existan el animal, veterinario y medicamento relacionados.\nDetalle: {e}")

    def _procesar_guardar_actualizar(self, id_h, animal, vet, med, f_apli, f_prox, t_evento, peso, diag, ventana):
        try:
            # Conecta la vista con el método CRUD 'actualizar' de la clase de lógica
            exp = Expedientes(id_h, animal, vet, med, f_apli, f_prox, t_evento, peso, diag)
            exp.actualizar()
            
            ventana.destroy()
            self.cargar_datos_tabla()
            exp.limpiar()
            messagebox.showinfo("Éxito", "Expediente actualizado correctamente.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo actualizar: {e}")

if __name__ == "__main__":
    app = ExpedientesApp()
    app.mainloop()