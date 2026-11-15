#from especies.especies import Especies
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
import os
import sys


class EspeciesView(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # 1. Configuración de la ventana principal
        self.title("FaunaVision - Especies")
        self.geometry("800x600")
        self.configure(fg_color="#FFFFFF")  # Color de fondo de la ventana principal

        self.crear_interfaz()

#Método principal que organiza las secciones de la vista
    def crear_interfaz(self):
        self.crear_menu_superior()
        self.crear_barra_acciones()
        self.crear_tabla()

#Crea la barra de navegación superior (Botón atrás, Título y Menú)
    def crear_menu_superior(self):
        self.menuSuperiorFrame = ctk.CTkFrame(self, fg_color="lightblue", height=200)
        self.menuSuperiorFrame.pack(fill="both", padx=30, pady=20)

        # Botón de Regresar
        self.btn_Regresar = ctk.CTkButton(
            self.menuSuperiorFrame, text="←", width=30, height=30, 
            corner_radius=30, fg_color="#95BA00",
            command=""
        )
        self.btn_Regresar.pack(side="left",padx=20, pady=20)

        # Título de la vista
        self.lbl_titulo = ctk.CTkLabel(
            self.menuSuperiorFrame, text="Especies", 
            font=("Inder", 25, "bold"), text_color="#000000"
        )
        self.lbl_titulo.pack(side="left", padx=30)

        # Botones de navegación (Menú, Animales Cautiverio, Medicamentos, Expediente, Veterinarios)
        btn_animales = ctk.CTkButton(
            self.menuSuperiorFrame, text="Animales Cautiverio", width=50, height=30,
            fg_color="transparent", font=("Inder", 10, "normal"), text_color="#000000",
            command=""
        )
        btn_animales.pack(side="right", padx=5)

        btn_medicamentos = ctk.CTkButton(
            self.menuSuperiorFrame, text="Medicamentos", width=50, height=30,
            fg_color="transparent", font=("Inder", 10, "normal"), text_color="#000000",
            command=""
        )
        btn_medicamentos.pack(side="right", padx=5)

        btn_expediente = ctk.CTkButton(
            self.menuSuperiorFrame, text="Expediente", width=50, height=30,
            fg_color="transparent", font=("Inder", 10, "normal"), text_color="#000000",
            command=""
        )
        btn_expediente.pack(side="right", padx=5)

        btn_veterinarios = ctk.CTkButton(
            self.menuSuperiorFrame, text="Veterinarios", width=50, height=30,
            fg_color="transparent", font=("Inder", 10, "normal"), text_color="#000000",
            command=""
        )
        btn_veterinarios.pack(side="right", padx=5)
       
        btn_menu = ctk.CTkButton(
            self.menuSuperiorFrame, text="Menú", width=50, height=30,
            fg_color="transparent", font=("Inder", 10, "normal"), text_color="#000000",
            command=""
        )
        btn_menu.pack(side="right", padx=5)


# Frame para la barra de búsqueda y el botón de añadir especie
    def crear_barra_acciones(self):

        self.acciones_frame = ctk.CTkFrame(self, fg_color="pink")
        self.acciones_frame.pack(fill="x", padx=100, pady=20)

        self.acciones_frame.grid_columnconfigure(0, weight=1)
        self.acciones_frame.grid_columnconfigure(1, weight=0)

    # Barra de búsqueda
        self.entry_buscar = ctk.CTkEntry(
            self.acciones_frame, placeholder_text="Buscar, nombre de especie o código", 
            width=500, height=42, corner_radius=30,
            fg_color="white", border_color="#000000", border_width=2,
            font=("Poppins", 12, "normal"), text_color="#757575"
        )
        self.entry_buscar.grid(row=0, column=0, sticky="ew", padx=(10, 10), pady=10)

        # Botón Añadir Especie
        self.btn_añadir = ctk.CTkButton(
            self.acciones_frame, text="Añadir Especie", 
            width=180, height=42, corner_radius=30,
            fg_color="#95A330", hover_color="#6D8927",
            font=("Poppins", 12, "bold"),
            command=""
        )
        self.btn_añadir.grid(row=0, column=1, sticky="ew", padx=(10, 30), pady=10)

    #Frame de tabla
    def crear_tabla(self):
            pass

    def view_agregarEspecie(self):
        pass
    
if __name__ == "__main__":
    app = EspeciesView()
    app.mainloop()

   


