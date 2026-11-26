
import customtkinter as ctk
from tkinter import messagebox
import os
print("LOGIN QUE SE ESTA EJECUTANDO:", os.path.abspath(__file__))

class LoginView:

    def __init__(self, ventana, controlador, abrir_registro=None):
        self.ventana = ventana
        self.controlador = controlador
        self.abrir_registro = abrir_registro

        self.usuario = ctk.StringVar()
        self.contrasena = ctk.StringVar()

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
            pady=25
        )

        ctk.CTkLabel(
            self.contenedor,
            text="FAUNAVISION",
            font=("Arial", 28, "bold"),
            text_color="#4A3B2C"
        ).pack(pady=(25, 5))

        ctk.CTkLabel(
            self.contenedor,
            text="Sistema de gestión de fauna silvestre",
            font=("Arial", 13),
            text_color="#666666"
        ).pack(pady=(0, 20))

        ctk.CTkLabel(
            self.contenedor,
            text="Usuario",
            font=("Arial", 14, "bold"),
            text_color="#4A3B2C"
        ).pack(anchor="w", padx=45, pady=(10, 5))

        self.entrada_usuario = ctk.CTkEntry(
            self.contenedor,
            textvariable=self.usuario,
            width=320,
            height=40,
            placeholder_text="Ingresa tu usuario",
            corner_radius=10,
            border_color="#84A91C"
        )
        self.entrada_usuario.pack()

        ctk.CTkLabel(
            self.contenedor,
            text="Contraseña",
            font=("Arial", 14, "bold"),
            text_color="#4A3B2C"
        ).pack(anchor="w", padx=45, pady=(15, 5))

        self.entrada_contrasena = ctk.CTkEntry(
            self.contenedor,
            textvariable=self.contrasena,
            width=320,
            height=40,
            placeholder_text="Ingresa tu contraseña",
            show="*",
            corner_radius=10,
            border_color="#84A91C"
        )
        self.entrada_contrasena.pack()

        ctk.CTkButton(
            self.contenedor,
            text="Iniciar sesión",
            width=320,
            height=42,
            corner_radius=20,
            fg_color="#84A91C",
            hover_color="#6E8E14",
            font=("Arial", 15, "bold"),
            command=self.iniciar_sesion
        ).pack(pady=(25, 12))

        ctk.CTkLabel(
            self.contenedor,
            text="¿No tienes una cuenta?",
            font=("Arial", 12),
            text_color="#555555"
        ).pack(pady=(5, 2))

        ctk.CTkButton(
            self.contenedor,
            text="Registrarse",
            width=180,
            height=35,
            corner_radius=18,
            fg_color="transparent",
            hover_color="#F0F4E5",
            text_color="#6E8E14",
            border_width=1,
            border_color="#84A91C",
            command=self.ir_registro
        ).pack(pady=(2, 15))

    def iniciar_sesion(self):

        usuario = self.usuario.get().strip()
        contrasena = self.contrasena.get()

        if usuario == "" or contrasena == "":
            messagebox.showwarning(
                "Advertencia",
                "Debes ingresar usuario y contraseña."
            )
            return

        self.controlador.validar_login(usuario, contrasena)

    def ir_registro(self):

        if self.abrir_registro is not None:
            self.abrir_registro()
