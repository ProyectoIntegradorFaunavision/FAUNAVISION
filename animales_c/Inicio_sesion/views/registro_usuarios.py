
import customtkinter as ctk
from tkinter import messagebox


class RegistroUsuariosView:

    def __init__(self, ventana, controlador, volver_login):
        self.ventana = ventana
        self.controlador = controlador
        self.volver_login = volver_login

        self.nombre = ctk.StringVar()
        self.usuario = ctk.StringVar()
        self.contrasena = ctk.StringVar()
        self.confirmar_contrasena = ctk.StringVar()
        self.tipo_usuario = ctk.StringVar(value="Veterinario")

        self.crear_interfaz()

    def crear_interfaz(self):

        self.contenedor = ctk.CTkFrame(
            self.ventana,
            fg_color="#FFFFFF",
            corner_radius=20
        )
        self.contenedor.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=20
        )

        ctk.CTkLabel(
            self.contenedor,
            text="Crear cuenta",
            font=("Arial", 27, "bold"),
            text_color="#4A3B2C"
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            self.contenedor,
            text="Registro de usuarios FAUNAVISION",
            font=("Arial", 13),
            text_color="#666666"
        ).pack(pady=(0, 12))

        self.crear_campo("Nombre completo", self.nombre)
        self.crear_campo("Nombre de usuario", self.usuario)
        self.crear_campo("Contraseña", self.contrasena, ocultar=True)
        self.crear_campo(
            "Confirmar contraseña",
            self.confirmar_contrasena,
            ocultar=True
        )

        ctk.CTkLabel(
            self.contenedor,
            text="Tipo de usuario",
            font=("Arial", 13, "bold"),
            text_color="#4A3B2C"
        ).pack(anchor="w", padx=45, pady=(10, 5))

        ctk.CTkOptionMenu(
            self.contenedor,
            variable=self.tipo_usuario,
            values=["Administrador", "Veterinario"],
            width=320,
            height=38,
            fg_color="#84A91C",
            button_color="#6E8E14",
            button_hover_color="#5D7912",
            dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#333333"
        ).pack()

        ctk.CTkButton(
            self.contenedor,
            text="Crear cuenta",
            width=320,
            height=42,
            corner_radius=20,
            fg_color="#84A91C",
            hover_color="#6E8E14",
            font=("Arial", 15, "bold"),
            command=self.registrar
        ).pack(pady=(20, 8))

        ctk.CTkButton(
            self.contenedor,
            text="Volver al inicio de sesión",
            width=220,
            height=35,
            corner_radius=18,
            fg_color="transparent",
            hover_color="#F0F4E5",
            text_color="#6E8E14",
            border_width=1,
            border_color="#84A91C",
            command=self.volver_login
        ).pack(pady=(3, 12))

    def crear_campo(self, titulo, variable, ocultar=False):

        ctk.CTkLabel(
            self.contenedor,
            text=titulo,
            font=("Arial", 13, "bold"),
            text_color="#4A3B2C"
        ).pack(anchor="w", padx=45, pady=(5, 4))

        ctk.CTkEntry(
            self.contenedor,
            textvariable=variable,
            width=320,
            height=36,
            corner_radius=10,
            border_color="#84A91C",
            show="*" if ocultar else ""
        ).pack()

    def registrar(self):

        nombre = self.nombre.get().strip()
        usuario = self.usuario.get().strip()
        contrasena = self.contrasena.get()
        confirmar = self.confirmar_contrasena.get()
        tipo = self.tipo_usuario.get()

        if (
            nombre == "" or
            usuario == "" or
            contrasena == "" or
            confirmar == ""
        ):
            messagebox.showwarning(
                "Campos incompletos",
                "Debes completar todos los campos."
            )
            return

        if contrasena != confirmar:
            messagebox.showwarning(
                "Contraseñas diferentes",
                "Las contraseñas no coinciden."
            )
            return

        if len(contrasena) < 8:
            messagebox.showwarning(
                "Contraseña no válida",
                "La contraseña debe tener al menos 8 caracteres."
            )
            return

        resultado = self.controlador.registrar_usuario(
            nombre,
            usuario,
            contrasena,
            tipo
        )

        if resultado:
            messagebox.showinfo(
                "Registro exitoso",
                "El usuario se registró correctamente.\nAhora puedes iniciar sesión."
            )
            self.volver_login()
