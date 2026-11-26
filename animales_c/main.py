import os
import sys
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageTk

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if os.path.basename(BASE_DIR) == "views":
    ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
else:
    ROOT_DIR = BASE_DIR

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

ASSETS_DIR = os.path.join(ROOT_DIR, "assets")

try:
    from views.vista_medicamentos.vista_medicamentos import VistaMedicamentos
except ImportError:
    VistaMedicamentos = None

ctk.set_appearance_mode("Light")

VERDE_OLIVA = "#84A91C"
VERDE_OLIVA_HOVER = "#6E8E14"
FONDO_BLANCO = "#FFFFFF"
FONDO_CREMA_MODAL = "#FBF8F1"
BORDE_CAFE_OSCURO = "#3B2618"
CAFE_TITULO = "#4A3B2C"
ROJO_PILDORA = "#E60000"
ROJO_OSCURO = "#B80000"
NEGRO_BORDE = "#1A1A1A"
COLOR_TRANSPARENTE = "#010101"


class MenuPrincipal(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=FONDO_BLANCO)
        self.master = master
        self.pack(fill="both", expand=True)
        self.imagenes_cache = []

        self._construir_header()
        self._construir_cuerpo()

    def _cargar_imagen_circular(self, nombre_archivo, diametro, emoji_respaldo="🐾"):
        nombre_sin_ext = os.path.splitext(nombre_archivo)[0]
        ruta = None
        for ext in (".png", ".jpg", ".jpeg", ".webp"):
            posible = os.path.join(ASSETS_DIR, nombre_sin_ext + ext)
            if os.path.exists(posible):
                ruta = posible
                break

        tam_lienzo = diametro + 14
        lienzo = Image.new("RGBA", (tam_lienzo, tam_lienzo), (255, 255, 255, 0))

        # Sombra suave circular
        sombra = Image.new("RGBA", (tam_lienzo, tam_lienzo), (255, 255, 255, 0))
        draw_sombra = ImageDraw.Draw(sombra)
        draw_sombra.ellipse((9, 11, diametro + 9, diametro + 11), fill=(0, 0, 0, 42))
        lienzo = Image.alpha_composite(lienzo, sombra)

        if ruta:
            img = Image.open(ruta).convert("RGBA")
            ancho, alto = img.size
            lado = min(ancho, alto)
            izq = (ancho - lado) // 2
            sup = (alto - lado) // 2
            img = img.crop((izq, sup, izq + lado, sup + lado))
            img = img.resize((diametro, diametro), Image.Resampling.LANCZOS)

            mascara = Image.new("L", (diametro, diametro), 0)
            draw_mask = ImageDraw.Draw(mascara)
            draw_mask.ellipse((0, 0, diametro, diametro), fill=255)

            circulo = Image.new("RGBA", (diametro, diametro), (255, 255, 255, 255))
            circulo.paste(img, (0, 0), mascara)
            lienzo.paste(circulo, (4, 4), mascara)
            foto = ImageTk.PhotoImage(lienzo)
            self.imagenes_cache.append(foto)
            return foto, None
        else:
            draw = ImageDraw.Draw(lienzo)
            draw.ellipse(
                (4, 4, diametro + 4, diametro + 4),
                fill=(248, 249, 244, 255),
                outline=(210, 220, 180, 255),
                width=3,
            )
            foto = ImageTk.PhotoImage(lienzo)
            self.imagenes_cache.append(foto)
            return foto, emoji_respaldo

    def _construir_header(self):
        header = tk.Frame(self, bg=FONDO_BLANCO, height=155)
        header.pack(fill="x", padx=55, pady=(26, 5))
        header.pack_propagate(False)

        # Botón circular de interrogación (?) grande
        btn_ayuda = ctk.CTkButton(
            header,
            text="?",
            width=52,
            height=52,
            corner_radius=26,
            fg_color=FONDO_BLANCO,
            hover_color="#F2F2F2",
            border_color=NEGRO_BORDE,
            border_width=2.5,
            text_color="#111111",
            font=("Arial", 26, "bold"),
            command=self.abrir_modal_ayuda,
        )
        btn_ayuda.place(x=10, y=14)

        # Título central grande para proyector
        titulo_box = tk.Frame(header, bg=FONDO_BLANCO)
        titulo_box.place(relx=0.5, rely=0.52, anchor="center")

        tk.Label(
            titulo_box,
            text="Parque Ecológico",
            font=("Arial", 40, "bold"),
            fg=CAFE_TITULO,
            bg=FONDO_BLANCO,
        ).pack()

        tk.Label(
            titulo_box,
            text="“El Tecúan”",
            font=("Georgia", 50),
            fg=CAFE_TITULO,
            bg=FONDO_BLANCO,
        ).pack()

        # Logo superior derecho grande
        ruta_logo = None
        for ext in (".png", ".jpg", ".jpeg", ".webp"):
            posible = os.path.join(ASSETS_DIR, "logo_tecuan" + ext)
            if os.path.exists(posible):
                ruta_logo = posible
                break

        if ruta_logo:
            diam = 110
            lienzo = Image.new("RGBA", (diam + 14, diam + 14), (255, 255, 255, 0))
            sombra = Image.new("RGBA", (diam + 14, diam + 14), (255, 255, 255, 0))
            ImageDraw.Draw(sombra).ellipse((9, 11, diam + 9, diam + 11), fill=(0, 0, 0, 42))
            lienzo = Image.alpha_composite(lienzo, sombra)

            img_logo = Image.open(ruta_logo).convert("RGBA")
            img_logo.thumbnail((diam - 16, diam - 16), Image.Resampling.LANCZOS)

            circulo = Image.new("RGBA", (diam, diam), (255, 255, 255, 255))
            pos_x = (diam - img_logo.width) // 2
            pos_y = (diam - img_logo.height) // 2
            circulo.paste(img_logo, (pos_x, pos_y), img_logo)

            mascara = Image.new("L", (diam, diam), 0)
            ImageDraw.Draw(mascara).ellipse((0, 0, diam, diam), fill=255)
            lienzo.paste(circulo, (4, 4), mascara)

            foto_logo = ImageTk.PhotoImage(lienzo)
            self.imagenes_cache.append(foto_logo)
            lbl_logo = tk.Label(header, image=foto_logo, bg=FONDO_BLANCO)
            lbl_logo.place(relx=1.0, x=-10, y=8, anchor="ne")

    def _crear_tarjeta_modulo(self, parent, relx, rely, texto_boton, archivo_img, emoji, comando, multilinea=False):
        contenedor = tk.Frame(parent, bg=FONDO_BLANCO)
        contenedor.place(relx=relx, rely=rely, anchor="center")

        diametro = 270
        foto, fallback = self._cargar_imagen_circular(archivo_img, diametro, emoji)

        lbl_img = tk.Label(contenedor, image=foto, bg=FONDO_BLANCO, cursor="hand2")
        lbl_img.pack(side="left", padx=(0, 12))
        lbl_img.bind("<Button-1>", lambda e: comando())

        if fallback:
            lbl_emoji = tk.Label(
                lbl_img,
                text=fallback,
                font=("Segoe UI Emoji", 60),
                bg="#F8F9F4",
                fg="#222222",
                cursor="hand2",
            )
            lbl_emoji.place(relx=0.48, rely=0.48, anchor="center")
            lbl_emoji.bind("<Button-1>", lambda e: comando())

        btn = ctk.CTkButton(
            contenedor,
            text=texto_boton,
            width=185,
            height=64 if multilinea else 56,
            corner_radius=28,
            fg_color=VERDE_OLIVA,
            hover_color=VERDE_OLIVA_HOVER,
            text_color="#FFFFFF",
            font=("Arial", 22, "bold"),
            command=comando,
        )
        btn.pack(side="left")

    def _construir_cuerpo(self):
        cuerpo = tk.Frame(self, bg=FONDO_BLANCO)
        cuerpo.pack(fill="both", expand=True, padx=25, pady=(0, 25))

        # Columna izquierda: Veterinarios (arriba) y Expedientes (abajo)
        self._crear_tarjeta_modulo(
            cuerpo,
            relx=0.19,
            rely=0.25,
            texto_boton="Veterinarios",
            archivo_img="veterinarios",
            emoji="🩺",
            comando=lambda: self.abrir_modulo("Veterinarios"),
        )

        self._crear_tarjeta_modulo(
            cuerpo,
            relx=0.19,
            rely=0.74,
            texto_boton="Expedientes",
            archivo_img="expedientes",
            emoji="📋",
            comando=lambda: self.abrir_modulo("Expedientes"),
        )

        # Centro: Animales en Cautiverio
        self._crear_tarjeta_modulo(
            cuerpo,
            relx=0.50,
            rely=0.52,
            texto_boton="Animales en\nCautiverio",
            archivo_img="cautiverio",
            emoji="🦌",
            comando=lambda: self.abrir_modulo("Animales en Cautiverio"),
            multilinea=True,
        )

        # Columna derecha: Medicamentos (arriba) y Especies (abajo)
        self._crear_tarjeta_modulo(
            cuerpo,
            relx=0.81,
            rely=0.25,
            texto_boton="Medicamentos",
            archivo_img="medicamentos",
            emoji="💊",
            comando=lambda: self.abrir_modulo("Medicamentos"),
        )

        self._crear_tarjeta_modulo(
            cuerpo,
            relx=0.81,
            rely=0.74,
            texto_boton="Especies",
            archivo_img="especies",
            emoji="🦓",
            comando=lambda: self.abrir_modulo("Especies"),
        )

    def abrir_modulo(self, nombre_modulo):
        if nombre_modulo == "Medicamentos" and VistaMedicamentos is not None:
            self.pack_forget()
            VistaMedicamentos(self.master, volver_menu=self.regresar_al_menu)
        else:
            self.mostrar_aviso_modulo(nombre_modulo)

    def regresar_al_menu(self):
        for widget in self.master.winfo_children():
            if widget is not self:
                widget.destroy()
        self.pack(fill="both", expand=True)

    def _crear_ventana_redondeada(self, ancho, alto):
        padre = self.winfo_toplevel()
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

    def mostrar_aviso_modulo(self, nombre_modulo):
        modal = self._crear_ventana_redondeada(450, 220)
        caja = ctk.CTkFrame(
            modal,
            fg_color=FONDO_BLANCO,
            border_color=NEGRO_BORDE,
            border_width=2.5,
            corner_radius=22,
            bg_color=COLOR_TRANSPARENTE,
        )
        caja.pack(fill="both", expand=True)

        ctk.CTkLabel(
            caja,
            text=f"Módulo de {nombre_modulo}\n\nEsta vista se conectará cuando el equipo integre su rama.",
            font=("Arial", 15),
            text_color="#111111",
            fg_color=FONDO_BLANCO,
            wraplength=380,
            justify="center",
        ).pack(expand=True, padx=24, pady=(22, 10))

        ctk.CTkButton(
            caja,
            text="Aceptar",
            width=115,
            height=38,
            corner_radius=19,
            fg_color=VERDE_OLIVA,
            hover_color=VERDE_OLIVA_HOVER,
            text_color="#FFFFFF",
            font=("Arial", 14, "bold"),
            command=modal.destroy,
        ).pack(pady=(0, 22))

    def abrir_modal_ayuda(self):
        modal = self._crear_ventana_redondeada(620, 420)

        marco = ctk.CTkFrame(
            modal,
            fg_color=FONDO_CREMA_MODAL,
            border_color=BORDE_CAFE_OSCURO,
            border_width=3,
            corner_radius=20,
            bg_color=COLOR_TRANSPARENTE,
        )
        marco.pack(fill="both", expand=True)

        top = ctk.CTkFrame(marco, fg_color=FONDO_CREMA_MODAL)
        top.pack(fill="x", padx=24, pady=(18, 6))

        ctk.CTkButton(
            top,
            text="✕",
            width=36,
            height=36,
            corner_radius=18,
            fg_color=ROJO_PILDORA,
            hover_color=ROJO_OSCURO,
            border_color=NEGRO_BORDE,
            border_width=1.5,
            text_color="#111111",
            font=("Arial", 20, "bold"),
            command=modal.destroy,
        ).pack(side="right")

        ctk.CTkLabel(
            top,
            text="Ayuda e Información",
            font=("Arial", 26, "bold"),
            text_color="#111111",
            fg_color=FONDO_CREMA_MODAL,
        ).pack(side="left", padx=(20, 0))

        caja_texto = ctk.CTkFrame(
            marco,
            fg_color=FONDO_BLANCO,
            border_color=BORDE_CAFE_OSCURO,
            border_width=2,
            corner_radius=18,
            bg_color=FONDO_CREMA_MODAL,
        )
        caja_texto.pack(fill="both", expand=True, padx=32, pady=(10, 26))

        info = (
            "Sistema de Gestión de registro - FAUNAVISION\n"
            "Parque Ecológico “El Tecuán”\n\n"
            "• Selecciona cualquiera de los 5 módulos principales para consultar, "
            "registrar, modificar o eliminar información.\n\n"
            "• Usa la barra de búsqueda y el botón de filtros (☰) dentro de cada "
            "sección para localizar registros rápidamente.\n\n"
            "• Presiona la flecha verde (←) en la esquina superior izquierda de "
            "cualquier módulo para regresar a este menú."
        )

        ctk.CTkLabel(
            caja_texto,
            text=info,
            font=("Arial", 16),
            text_color="#111111",
            fg_color=FONDO_BLANCO,
            wraplength=510,
            justify="left",
        ).pack(expand=True, padx=22, pady=18)


if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Parque Ecológico El Tecuán - Menú Principal")
    app.geometry("1280x760")
    MenuPrincipal(app)
    app.mainloop()