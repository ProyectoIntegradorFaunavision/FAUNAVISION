import customtkinter as ctk
import sqlite3

# Configurar interfaz base
ctk.set_appearance_mode("System") 
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Usuarios")
        self.geometry("400x300")
        
        # Conectar e inicializar la Base de Datos (SQLite)
        self.conn = sqlite3.connect("datos.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, nombre TEXT)")
        self.conn.commit()

        # Componentes Visuales
        self.label = ctk.CTkLabel(self, text="Nombre del Usuario:")
        self.label.pack(pady=10)

        self.entry = ctk.CTkEntry(self, placeholder_text="Escribe aquí...")
        self.entry.pack(pady=10)

        self.btn = ctk.CTkButton(self, text="Guardar en Base de Datos", command=self.guardar_datos)
        self.btn.pack(pady=10)

    def guardar_datos(self):
        nombre = self.entry.get()
        if nombre:
            self.cursor.execute("INSERT INTO usuarios (nombre) VALUES (?)", (nombre,))
            self.conn.commit()
            self.entry.delete(0, 'end')
            print("¡Guardado con éxito!")

if __name__ == "__main__":
    app = App()
    app.mainloop()