from especies.especies import Especies
import math
import CTkMessagebox
import re


class EspeciesController:
    PATRON_CODIGO = re.compile(r"^\d{1,8}$")
    PATRON_NOMBRE_ESPECIE = re.compile(
        r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+(?: [A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+)*$"
    )
    PATRON_NOMBRE_CIENTIFICO = re.compile(
        r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+(?: [A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+)*$"
    )

    def __init__(self, vista, filas_por_pagina):
        self.vista = vista
        self.registros_mostrar = []
        self.registros_filtrados = []
        self.pagina_actual = 0
        self.filas_por_pagina = filas_por_pagina

    def limpiar_espacios(self, texto: str = ""):
        texto_limpio = " ".join((texto or "").strip().split())
        return texto_limpio

    def validar_campos_especie(self, codigo, especie_nombre, nombre_cientifico):
        codigo_limpio = (codigo or "").strip()
        nombre_limpio = self.limpiar_espacios(especie_nombre).capitalize()
        cientifico_limpio = self.limpiar_espacios(nombre_cientifico).capitalize()

        if not codigo_limpio or not nombre_limpio or not cientifico_limpio:
            return (
                False,
                "Todos los campos (código, nombre de la especie y nombre científico) son obligatorios.",
                None,
            )


        if not self.PATRON_CODIGO.fullmatch(codigo_limpio):
            return False, "El código debe contener solo números (1 a 8 dígitos).", None

        if not self.PATRON_NOMBRE_ESPECIE.fullmatch(nombre_limpio):
            return (
                False,
                "El nombre de la especie solo debe contener letras y espacios.",
                None,
            )

        if not self.PATRON_NOMBRE_CIENTIFICO.fullmatch(cientifico_limpio):
            return (
                False,
                "El nombre científico debe llevar formato binomial (ej. Panthera onca).",
                None,
            )

        return True, "", (codigo_limpio, nombre_limpio, cientifico_limpio)

    def alerta_validacion(self, mensaje):
        CTkMessagebox.CTkMessagebox(
            title="Formato inválido",
            message=mensaje,
            icon="warning",
        )

    def confirmacion(self,accion):
        elemento="este registro"
        msg = CTkMessagebox.CTkMessagebox(
            title="Confirmación",
            message=f"¿Está seguro que desea {accion} {elemento}?",
            icon="question",
            option_1="Cancelar",
            option_2="Aceptar",
        )
        return msg.get() == "Aceptar"

    def respuesta_sql(self, mensaje, padre=None, tipo="info"):
        if mensaje:
            CTkMessagebox.CTkMessagebox(
                master=padre,
                title="Exitoso",
                message="Acción realizada con éxito",
            )
        else:
            CTkMessagebox.CTkMessagebox(
                master=padre,
                title="Verifica por favor",
                message="Esta acción no se pudo realizar con éxito",
            )

    def insertarController(self):
        codigo = self.limpiar_espacios(self.vista.codigo.get())
        especie_nombre = self.limpiar_espacios(self.vista.nombre_especie.get())
        nombre_cientifico = self.limpiar_espacios(self.vista.nombre_cientifico.get())
        valido, mensaje, datos = self.validar_campos_especie(
            codigo, especie_nombre, nombre_cientifico
        )
        # if not codigo or not especie_nombre:
        #     self.respuesta_sql(False)
        #     return
        if not valido:
            CTkMessagebox.CTkMessagebox(
                title="Validación",
                message=mensaje,
                icon="warning",
            )
            return
           

        codigo_ok, especie_ok, cientifico_ok = datos

        nueva_especie = Especies(codigo, especie_nombre, nombre_cientifico)
        respuesta = nueva_especie.insertar()
        
        self.respuesta_sql(respuesta)
        if respuesta:
            self.refrescar_tabla(ir_a_ultima_pagina=False)    
            self.vista.limpiar_campos_anadir()

    def eliminarController(self,codigo):
        codigo = self.vista.codigo_eliminar
        resp= self.confirmacion("eliminar")
        if resp:
            respuesta=Especies.eliminar(codigo)
            self.respuesta_sql(respuesta)
        else:
            respuesta=False
            self.respuesta_sql(respuesta)
        self.refrescar_tabla(False)

    def modificarController(self):
        codigo = self.vista.codigo.get().strip()
        nombre_especie = self.vista.nombre_especie.get().strip()
        nombre_cientifico = self.vista.nombre_cientifico.get().strip()

        if not codigo:
            self.respuesta_sql(False)
            return

        especie_actualizada = Especies(codigo,nombre_especie, nombre_cientifico)
        respuesta = especie_actualizada.actualizar()
        self.respuesta_sql(respuesta)
        if respuesta:
            self.refrescar_tabla(ir_a_ultima_pagina=False)
    
    def mostrarController(self):
        """Carga todos los registros desde la BD y actualiza la tabla y paginación."""
        datos = Especies.mostrar() or []
        self.registros_mostrar = datos
        self.registros_filtrados = list(datos)
        self.pagina_actual = 0
        pagina_datos, inicio, info_pag = self.obtener_pagina_actual()
        self.vista.renderizar_tabla()
        return datos

    def buscarController(self, criterio):
        criterio_limpio = (criterio or "").strip()
        if criterio_limpio:
            self.registros_filtrados = Especies.filtrar(criterio_limpio) or []
        else:
            if not self.registros_mostrar:
                self.registros_mostrar = Especies.mostrar() or []
            self.registros_filtrados = list(self.registros_mostrar)

        self.pagina_actual = 0
        self.vista.registros_filtrados = self.registros_filtrados
        self.vista.pagina_actual = 0
        self.vista.renderizar_tabla()
        return self.registros_filtrados
        
    def obtener_pagina_actual(self):
        total_registros = len(self.registros_filtrados)
        total_paginas = max(1, math.ceil(total_registros / self.filas_por_pagina))

        if self.pagina_actual > total_paginas - 1:
            self.pagina_actual = max(0, total_paginas - 1)

        inicio = self.pagina_actual * self.filas_por_pagina
        fin = inicio + self.filas_por_pagina
        pagina_datos = self.registros_filtrados[inicio:fin]

        return pagina_datos, inicio, total_paginas

    def refrescar_tabla(self, ir_a_ultima_pagina=False):
        datos_actualizados = Especies.mostrar() or []
        datos_actualizados = Especies.mostrar() or []
        self.registros_mostrar = datos_actualizados
        self.registros_filtrados = list(datos_actualizados)

        filas_por_pagina = getattr(self, "filas_por_pagina", 15)
        total_registros = len(self.registros_filtrados)
        total_paginas = max(1, math.ceil(total_registros / filas_por_pagina))

        if total_registros == 0 or not ir_a_ultima_pagina:
            pagina_destino = min(getattr(self, "pagina_actual", 0), total_paginas - 1)
            pagina_destino = max(0, pagina_destino)
        else:
            pagina_destino = total_paginas - 1

        self.pagina_actual = pagina_destino
        self.vista.registros_filtrados = self.registros_filtrados
        self.vista.pagina_actual = pagina_destino
        self.vista.renderizar_tabla()




