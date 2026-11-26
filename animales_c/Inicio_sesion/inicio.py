
import os
import sys
import customtkinter as ctk

# Ruta principal del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Importaciones del proyecto
from views.login import LoginView
from views.registro_usuarios import RegistroUsuariosView
from controllers.usuariosController import LoginController

# Importamos el menú original de tu amiga
from main import MenuPrincipal


class Aplicacion:

    def __init__(self):
        self.ventana = ctk.CTk()

        self.ventana.title("FAUNAVISION - Inicio de sesión")
        self.ventana.geometry("500x400")
        self.ventana.resizable(False, False)

        # Controlador de usuarios
        self.controlador = LoginController()

        # Conectamos el controlador con el menú
        self.controlador.abrir_menu = self.abrir_menu

        # Mostramos el login al iniciar
        self.mostrar_login()

    # Elimina los elementos de la ventana actual
    def limpiar_ventana(self):
        for widget in self.ventana.winfo_children():
            widget.destroy()

    # Muestra el inicio de sesión
    def mostrar_login(self):
       
        self.limpiar_ventana()

        self.ventana.title("FAUNAVISION - Inicio de sesión")
        self.ventana.geometry("500x550")
        self.ventana.resizable(False, False)

        self.login = LoginView(
            self.ventana,
            self.controlador,
            self.mostrar_registro
        )
        print("FUNCION DE REGISTRO:", self.login.abrir_registro)
    # Muestra el formulario de registro
    def mostrar_registro(self):
        self.limpiar_ventana()

        self.ventana.title("FAUNAVISION - Registro de usuarios")
        self.ventana.geometry("600x760")
        self.ventana.resizable(False, False)

        self.registro = RegistroUsuariosView(
            self.ventana,
            self.controlador,
            self.mostrar_login
        )

    # Abre el menú original de tu amiga
    def abrir_menu(self, nombre_usuario, tipo_usuario):
        self.limpiar_ventana()

        self.ventana.title(
            "Parque Ecológico El Tecuán - Menú Principal"
        )
        self.ventana.geometry("1280x760")
        self.ventana.resizable(True, True)

        self.menu = MenuPrincipal(self.ventana)

    # Inicia la aplicación
    def iniciar(self):
        self.ventana.mainloop()


if __name__ == "__main__":
    aplicacion = Aplicacion()
    aplicacion.iniciar()
