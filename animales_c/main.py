from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
from conexionBD import crear_db, conectar

# Configurar interfaz faunavision
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FaunaVision")
        self.geometry("800x600")
        crear_db()
        self.conexion = conectar()

    def response_sql(self, respuesta):
        if respuesta:
            CTkMessagebox(title="...Exitoso...", message="Acción realizada con éxito")
        else:
            CTkMessagebox(title="..Verifica por favor..", message="Esta acción no se pudo realizar con éxito")



if __name__ == "__main__":
    app = App()
    app.mainloop()
