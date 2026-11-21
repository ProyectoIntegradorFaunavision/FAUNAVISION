import sys
import os
import tkinter as tk
import customtkinter as ctk

# Ruta para conectar con la raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

ctk.set_appearance_mode("Light")

VERDE_OLIVA = "#84A91C"
VERDE_OLIVA_HOVER = "#6E8E14"
VERDE_HEADER_TABLA = "#C5D88A"
VERDE_BORDE_TABLA = "#9BB354"
VERDE_LIMA_BTN = "#A3D900"
VERDE_LIMA_HOVER = "#8AB800"
FONDO_BLANCO = "#FFFFFF"
NEGRO_BORDE = "#1A1A1A"


class AnimalesCautiverioView(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        
        # 1. Configuración de la ventana principal
        self.title("FaunaVision - Animales en Cautiverio")
        self.geometry("980x670")
        self.configure(fg_color=FONDO_BLANCO)

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
            font=("Inder", 22, "bold"), text_color="#000000"
        )
        self.lbl_titulo.pack(side="left", padx=10)

        # Botones de navegación superior
        for item in ["Menú", "Especies", "Veterinarios", "Expediente", "Medicamentos"]:
            ctk.CTkButton(
                self.menuSuperiorFrame, text=item, width=50, height=30,
                fg_color="transparent", font=("Inder", 11, "normal"), text_color="#000000",
                hover_color="#EFEFEF", command=""
            ).pack(side="right", padx=5)

    def crear_barra_acciones(self):
        self.acciones_frame = ctk.CTkFrame(self, fg_color=FONDO_BLANCO)
        self.acciones_frame.pack(fill="x", padx=45, pady=(5, 15))

        self.acciones_frame.grid_columnconfigure(0, weight=1)
        self.acciones_frame.grid_columnconfigure(1, weight=0)

        # Barra de búsqueda
        self.entry_buscar = ctk.CTkEntry(
            self.acciones_frame, placeholder_text="Buscar", 
            width=500, height=42, corner_radius=21,
            fg_color="white", border_color=NEGRO_BORDE, border_width=2,
            font=("Poppins", 12, "normal"), text_color="#757575"
        )
        self.entry_buscar.grid(row=0, column=0, sticky="ew", padx=(0, 15), pady=5)

        # Botón Añadir Animal
        self.btn_añadir = ctk.CTkButton(
            self.acciones_frame, text="Añadir Animal", 
            width=180, height=42, corner_radius=21,
            fg_color="#95A330", hover_color="#6D8927",
            font=("Poppins", 12, "bold"),
            command=""
        )
        self.btn_añadir.grid(row=0, column=1, sticky="ew", padx=(0, 0), pady=5)

    def crear_tabla(self):
        self.tabla_outer = tk.Frame(
            self, bg=VERDE_BORDE_TABLA, bd=0,
            highlightthickness=1, highlightbackground=VERDE_BORDE_TABLA,
        )
        self.tabla_outer.pack(fill="both", expand=True, padx=45, pady=(0, 10))

        self.header_tabla = tk.Frame(self.tabla_outer, bg=VERDE_HEADER_TABLA, height=35)
        self.header_tabla.pack(fill="x", pady=(0, 1))
        self.header_tabla.pack_propagate(False)

        # Columnas según tus atributos
        pesos_columnas = [1, 2, 3, 2, 2, 2, 2, 2]
        encabezados = ["N°", "Código", "Especie", "Sexo", "Peso", "Edad", "Estado de salud", ""]

        for col_idx, texto in enumerate(encabezados):
            self.header_tabla.grid_columnconfigure(col_idx, weight=pesos_columnas[col_idx], uniform="col")
            self.header_tabla.grid_rowconfigure(0, weight=1)
            tk.Label(
                self.header_tabla, text=texto, font=("Poppins", 10, "bold"),
                fg="#111111", bg=VERDE_HEADER_TABLA, anchor="w" if col_idx > 0 else "center",
            ).grid(row=0, column=col_idx, sticky="ew", padx=8)

        self.cuerpo_tabla = tk.Frame(self.tabla_outer, bg=VERDE_BORDE_TABLA)
        self.cuerpo_tabla.pack(fill="both", expand=True)

        # Filas estáticas de ejemplo vacías para la estructura
        for r in range(10):
            self.cuerpo_tabla.grid_rowconfigure(r, weight=1)
            self.cuerpo_tabla.grid_columnconfigure(0, weight=1)

            fila_frame = tk.Frame(self.cuerpo_tabla, bg=FONDO_BLANCO)
            fila_frame.grid(row=r, column=0, sticky="nsew", pady=(0, 1 if r < 9 else 0))

            for c in range(8):
                fila_frame.grid_columnconfigure(c, weight=pesos_columnas[c], uniform="col")
                fila_frame.grid_rowconfigure(0, weight=1)
                lbl = tk.Label(
                    fila_frame, text="" if c > 0 else ("1" if r == 0 else ""), 
                    font=("Poppins", 9), fg=VERDE_OLIVA if c == 7 else "#111111", 
                    bg=FONDO_BLANCO, anchor="w" if c > 0 else "center",
                )
                if r == 0 and c == 1: lbl.configure(text="AV9567")
                if r == 0 and c == 2: lbl.configure(text="Lobo Mexicano")
                if r == 0 and c == 3: lbl.configure(text="Masculino")
                if r == 0 and c == 4: lbl.configure(text="25 Kilos")
                if r == 0 and c == 5: lbl.configure(text="3 años")
                if r == 0 and c == 6: lbl.configure(text="Excelente")
                if r == 0 and c == 7: lbl.configure(text="Ver más", cursor="hand2")
                lbl.grid(row=0, column=c, sticky="ew", padx=8)

        # Barra inferior de paginación simulada
        self.paginacion_frame = ctk.CTkFrame(self, fg_color="transparent", height=40)
        self.paginacion_frame.pack(pady=(5, 10))

        for i in range(3):
            ctk.CTkButton(
                self.paginacion_frame, text=str(i + 1), width=30, height=30,
                corner_radius=15, fg_color="#84A91C" if i == 0 else "#757575",
                hover_color=VERDE_OLIVA, font=("Poppins", 11, "bold"),
                command=""
            ).pack(side="left", padx=3)


if __name__ == "__main__":
    app = AnimalesCautiverioView()
    app.mainloop()