
from models.usuarios import Usuarios
from tkinter import messagebox


class LoginController:

    def __init__(self):
        self.modelo = Usuarios()
        self.vista = None
        self.abrir_menu = None

    def validar_login(self, usuario, contrasena):

        usuario = usuario.strip()

        if usuario == "" or contrasena == "":
            messagebox.showwarning(
                "Advertencia",
                "Debes ingresar usuario y contraseña."
            )
            return

        datos_usuario = self.modelo.buscar_usuario(usuario)

        if datos_usuario is None:
            messagebox.showerror(
                "Error",
                "El usuario no existe."
            )
            return

        id_usuario, nombre_completo, nombre_usuario, hash_guardado, salt, tipo_usuario = datos_usuario

        contraseña_correcta = self.modelo.verificar_contrasena(
            contrasena,
            salt,
            hash_guardado
        )

        if not contraseña_correcta:
            messagebox.showerror(
                "Error",
                "La contraseña es incorrecta."
            )
            return

        if tipo_usuario not in ("Administrador", "Veterinario"):
            messagebox.showerror(
                "Error",
                "El tipo de usuario no es válido."
            )
            return

        messagebox.showinfo(
            "Bienvenido",
            "Inicio de sesión correcto."
        )

        print("Inicio de sesión correcto")
        print("Usuario:", nombre_usuario)
        print("Tipo:", tipo_usuario)

        if self.abrir_menu is not None:
            self.abrir_menu(nombre_usuario, tipo_usuario)

    def registrar_usuario(self, nombre, usuario, contrasena, tipo):

        resultado = self.modelo.registrar_usuario(
            usuario,
            contrasena,
            tipo,
            nombre
        )

        if resultado:
            return True

        messagebox.showerror(
            "Error de registro",
            "Ese nombre de usuario ya existe o no se pudo registrar."
        )

        return False
