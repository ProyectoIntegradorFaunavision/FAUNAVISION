import sys
import os
import math
import CTkMessagebox
import re

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from Veterinarios import Veterinarios

class VeterinariosController:

    PATRON_NUM_EMPLEADO = re.compile(r"^\d{1,8}$")

    PATRON_NOMBRES = re.compile(
        r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+(?: [A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+)*$"
    )

    PATRON_CARGO = re.compile(
        r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+(?:[ A-Za-zÁÉÍÓÚÜÑáéíóúüñ]*)$"
    )

    PATRON_DIRECCION = re.compile(
        r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9 #.,\-]+$"
    )

    PATRON_NUMERO = re.compile(r"^\d{1,6}$")
    PATRON_CP = re.compile(r"^\d{5}$")
    PATRON_TELEFONO = re.compile(r"^\d{10}$")
    PATRON_CORREO = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )

    def __init__(self, vista, filas_por_pagina):
        self.vista = vista
        self.registros_mostrar = []
        self.registros_filtrados = []
        self.pagina_actual = 0
        self.filas_por_pagina = filas_por_pagina

    def limpiar_espacios(self, texto=""):
        texto_limpio = " ".join((str(texto) if texto is not None else "").strip().split())
        return texto_limpio

    def validar_campos_veterinarios(
        self,
        num_empleado,
        nombre,
        apellido1,
        apellido2,
        cargo,
        calle,
        col,
        num,
        codigo_postal,
        telefono,
        correo
    ):

        num_empleado_limpio = (num_empleado or "").strip()
        nombre_limpio = self.limpiar_espacios(nombre).title()
        apellido1_limpio = self.limpiar_espacios(apellido1).title()
        apellido2_limpio = self.limpiar_espacios(apellido2).title()
        cargo_limpio = self.limpiar_espacios(cargo).title()
        calle_limpia = self.limpiar_espacios(calle).title()
        col_limpia = self.limpiar_espacios(col).title()
        num_limpio = (num or "").strip()
        codigo_postal_limpio = (codigo_postal or "").strip()
        telefono_limpio = (telefono or "").strip()
        correo_limpio = (correo or "").strip().lower()

        campos_obligatorios = (
            num_empleado_limpio,
            nombre_limpio,
            apellido1_limpio,
            apellido2_limpio,
            cargo_limpio,
            calle_limpia,
            col_limpia,
            num_limpio,
            codigo_postal_limpio,
            telefono_limpio,
            correo_limpio
        )

        if not all(campos_obligatorios):
            return False, "Todos los campos son obligatorios.", None

        if not self.PATRON_NUM_EMPLEADO.fullmatch(num_empleado_limpio):
            return False, "El número de empleado debe contener solamente números (máximo 8 dígitos).", None

        if not self.PATRON_NOMBRES.fullmatch(nombre_limpio):
            return False, "El nombre solo debe contener letras y espacios.", None

        if not self.PATRON_NOMBRES.fullmatch(apellido1_limpio):
            return False, "El primer apellido solo debe contener letras y espacios.", None

        if not self.PATRON_NOMBRES.fullmatch(apellido2_limpio):
            return False, "El segundo apellido solo debe contener letras y espacios.", None

        if not self.PATRON_CARGO.fullmatch(cargo_limpio):
            return False, "El cargo contiene caracteres no permitidos.", None

        if not self.PATRON_DIRECCION.fullmatch(calle_limpia):
            return False, "La calle contiene caracteres no permitidos.", None

        if not self.PATRON_DIRECCION.fullmatch(col_limpia):
            return False, "La colonia contiene caracteres no permitidos.", None

        if not self.PATRON_NUMERO.fullmatch(num_limpio):
            return False, "El número del domicilio debe contener solamente números.", None

        if not self.PATRON_CP.fullmatch(codigo_postal_limpio):
            return False, "El código postal debe contener exactamente 5 números.", None

        if not self.PATRON_TELEFONO.fullmatch(telefono_limpio):
            return False, "El teléfono debe contener exactamente 10 números.", None

        if not self.PATRON_CORREO.fullmatch(correo_limpio):
            return False, "Ingrese un correo electrónico válido.", None

        datos_validados = (
            int(num_empleado_limpio),
            nombre_limpio,
            apellido1_limpio,
            apellido2_limpio,
            cargo_limpio,
            calle_limpia,
            col_limpia,
            int(num_limpio),
            int(codigo_postal_limpio),
            telefono_limpio,
            correo_limpio
        )

        return True, "", datos_validados

    def alerta_validacion(self, mensaje):
        CTkMessagebox.CTkMessagebox(
            title="Formato inválido",
            message=mensaje,
            icon="warning"
        )

    def confirmacion(self, accion):
        elemento = "este registro"

        msg = CTkMessagebox.CTkMessagebox(
            title="Confirmación",
            message=f"¿Está seguro que desea {accion} {elemento}?",
            icon="question",
            option_1="Cancelar",
            option_2="Aceptar"
        )

        return msg.get() == "Aceptar"

    def respuesta_sql(self, mensaje, padre=None, tipo="info"):
        if mensaje:
            CTkMessagebox.CTkMessagebox(
                master=padre,
                title="Exitoso",
                message="La acción se realizó correctamente.",
                icon="check"
            )
        else:
            CTkMessagebox.CTkMessagebox(
                master=padre,
                title="Verifica por favor",
                message="La acción no se pudo realizar. Verifique los datos.",
                icon="warning"
            )

    def insertarController(self):

        num_empleado = self.limpiar_espacios(self.vista.num_empleado.get())
        nombre = self.limpiar_espacios(self.vista.nombre.get())
        apellido1 = self.limpiar_espacios(self.vista.apellido1.get())
        apellido2 = self.limpiar_espacios(self.vista.apellido2.get())
        cargo = self.limpiar_espacios(self.vista.cargo.get())
        calle = self.limpiar_espacios(self.vista.calle.get())
        col = self.limpiar_espacios(self.vista.col.get())
        num = self.limpiar_espacios(self.vista.num.get())
        codigo_postal = self.limpiar_espacios(self.vista.codigo_postal.get())
        telefono = self.limpiar_espacios(self.vista.telefono.get())
        correo = self.limpiar_espacios(self.vista.correo.get())

        valido, mensaje, datos = self.validar_campos_veterinarios(
            num_empleado, nombre, apellido1, apellido2, cargo,
            calle, col, num, codigo_postal, telefono, correo
        )

        if not valido:
            self.alerta_validacion(mensaje)
            return

        (
            num_empleado_ok,
            nombre_ok,
            apellido1_ok,
            apellido2_ok,
            cargo_ok,
            calle_ok,
            col_ok,
            num_ok,
            codigo_postal_ok,
            telefono_ok,
            correo_ok
        ) = datos

        nuevo_veterinario = Veterinarios(
            num_empleado_ok,
            nombre_ok,
            apellido1_ok,
            apellido2_ok,
            cargo_ok,
            calle_ok,
            col_ok,
            num_ok,
            codigo_postal_ok,
            telefono_ok,
            correo_ok
        )

        respuesta = nuevo_veterinario.insertar()

        self.respuesta_sql(respuesta)

        if respuesta:
            self.refrescar_tabla(ir_a_ultima_pagina=False)
            self.vista.limpiar_campos_anadir()

    def eliminarController(self, num_empleado):

        resp = self.confirmacion("eliminar")

        if resp:
            respuesta = Veterinarios.eliminar(num_empleado)
            self.respuesta_sql(respuesta)
        else:
            respuesta = False

        self.refrescar_tabla(False)

    def modificarController(self):

        num_empleado = self.limpiar_espacios(self.vista.num_empleado.get())
        nombre = self.limpiar_espacios(self.vista.nombre.get())
        apellido1 = self.limpiar_espacios(self.vista.apellido1.get())
        apellido2 = self.limpiar_espacios(self.vista.apellido2.get())
        cargo = self.limpiar_espacios(self.vista.cargo.get())
        calle = self.limpiar_espacios(self.vista.calle.get())
        col = self.limpiar_espacios(self.vista.col.get())
        num = self.limpiar_espacios(self.vista.num.get())
        codigo_postal = self.limpiar_espacios(self.vista.codigo_postal.get())
        telefono = self.limpiar_espacios(self.vista.telefono.get())
        correo = self.limpiar_espacios(self.vista.correo.get())

        valido, mensaje, datos = self.validar_campos_veterinarios(
            num_empleado, nombre, apellido1, apellido2, cargo,
            calle, col, num, codigo_postal, telefono, correo
        )

        if not valido:
            self.alerta_validacion(mensaje)
            return

        (
            num_empleado_ok,
            nombre_ok,
            apellido1_ok,
            apellido2_ok,
            cargo_ok,
            calle_ok,
            col_ok,
            num_ok,
            codigo_postal_ok,
            telefono_ok,
            correo_ok
        ) = datos

        veterinario_actualizado = Veterinarios(
            num_empleado_ok,
            nombre_ok,
            apellido1_ok,
            apellido2_ok,
            cargo_ok,
            calle_ok,
            col_ok,
            num_ok,
            codigo_postal_ok,
            telefono_ok,
            correo_ok
        )

        respuesta = veterinario_actualizado.actualizar()

        self.respuesta_sql(respuesta)

        if respuesta:
            self.refrescar_tabla(ir_a_ultima_pagina=False)

    def mostrarController(self):

        datos = Veterinarios.mostrar() or []

        self.registros_mostrar = datos
        self.registros_filtrados = list(datos)
        self.pagina_actual = 0

        pagina_datos, inicio, info_pag = self.obtener_pagina_actual()

        self.vista.registros_filtrados = self.registros_filtrados
        self.vista.pagina_actual = self.pagina_actual
        self.vista.renderizar_tabla()

        return datos

    def buscarController(self, criterio):

        criterio_limpio = (criterio or "").strip()

        if criterio_limpio:
            self.registros_filtrados = Veterinarios.filtrar(criterio_limpio) or []
        else:
            if not self.registros_mostrar:
                self.registros_mostrar = Veterinarios.mostrar() or []

            self.registros_filtrados = list(self.registros_mostrar)

        self.pagina_actual = 0

        self.vista.registros_filtrados = self.registros_filtrados
        self.vista.pagina_actual = 0
        self.vista.renderizar_tabla()

        return self.registros_filtrados

    def obtener_pagina_actual(self):

        total_registros = len(self.registros_filtrados)

        total_paginas = max(
            1,
            math.ceil(total_registros / self.filas_por_pagina)
        )

        if self.pagina_actual > total_paginas - 1:
            self.pagina_actual = max(0, total_paginas - 1)

        inicio = self.pagina_actual * self.filas_por_pagina
        fin = inicio + self.filas_por_pagina

        pagina_datos = self.registros_filtrados[inicio:fin]

        return pagina_datos, inicio, total_paginas

    def refrescar_tabla(self, ir_a_ultima_pagina=False):

        datos_actualizados = Veterinarios.mostrar() or []

        self.registros_mostrar = datos_actualizados
        self.registros_filtrados = list(datos_actualizados)

        filas_por_pagina = getattr(self, "filas_por_pagina", 15)

        total_registros = len(self.registros_filtrados)

        total_paginas = max(
            1,
            math.ceil(total_registros / filas_por_pagina)
        )

        if total_registros == 0 or not ir_a_ultima_pagina:
            pagina_destino = min(
                getattr(self, "pagina_actual", 0),
                total_paginas - 1
            )
            pagina_destino = max(0, pagina_destino)
        else:
            pagina_destino = total_paginas - 1

        self.pagina_actual = pagina_destino

        self.vista.registros_filtrados = self.registros_filtrados
        self.vista.pagina_actual = pagina_destino
        self.vista.renderizar_tabla()
