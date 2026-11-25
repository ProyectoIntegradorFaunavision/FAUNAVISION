from animales_cautiverio.animales_cautiverio import AnimalesC
import math
import CTkMessagebox
import re
from datetime import date, datetime


class AnimalesController:
    PATRON_CODIGO = re.compile(r"^\d{1,8}$")
    PATRON_NOMBRES = re.compile(
        r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+(?: [A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+)*$"
    )
    PATRON_SEXO = re.compile(
        r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]*$"
    )
    PATRON_OBSERVACIONES= re.compile(
        r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9]+(?:[ \t\r\n]+[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9.,;:()\-]+)*$"
    )
    PATRON_FECHA = re.compile(
        r"^(?:0[1-9]|[12]\d|3[01])/(?:0[1-9]|1[0-2])/\d{4}$"  
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

    def validar_campos_animales(    
            self,
            codigo,
            especie,
            sexo,
            fNacimiento,
            fIngreso,
            pesoInicial,
            estado_salud,
            observaciones,
        ):
        codigo_limpio = (codigo or "").strip()
        especie_limpia = self.limpiar_espacios(especie).capitalize()
        sexo_limpio = self.limpiar_espacios(sexo).capitalize()
        fNacimiento_limpia = (fNacimiento or "").strip()
        fIngreso_limpia = (fIngreso or "").strip()
        pesoInicial_limpio = (pesoInicial or "").strip()
        estado_salud_limpio = self.limpiar_espacios(estado_salud).capitalize()
        observaciones_limpias = self.limpiar_espacios(observaciones)

        campos_obligatorios = (
            codigo_limpio,
            especie_limpia,
            sexo_limpio,
            fNacimiento_limpia,
            fIngreso_limpia,
            pesoInicial_limpio,
        )

        if not all(campos_obligatorios):
            return (
                False,
                "Todos los campos son obligatorios.",
                None,
            )

        if not self.PATRON_CODIGO.fullmatch(codigo_limpio):
            return False, "El código debe contener solo números (1 a 8 dígitos).", None

        if not self.PATRON_NOMBRES.fullmatch(especie_limpia):
            return (
                False,
                "La especie solo debe contener letras y espacios.",
                None,
            )

        if not self.PATRON_SEXO.fullmatch(sexo_limpio):
            return (
                False,
                "El campo de sexo solo debe contener letras (Hembra-Macho).",
                None,
            )

        if not (
            self.PATRON_FECHA.fullmatch(fIngreso_limpia)
            and self.PATRON_FECHA.fullmatch(fNacimiento_limpia)
        ):
            return (
                False,
                "Ingrese una fecha en el formato correcto (DD/MM/AAAA).",
                None,
            )

        if observaciones_limpias and not self.PATRON_OBSERVACIONES.fullmatch(
            observaciones_limpias
        ):
            return (
                False,
                "Ingrese una observación de no más de 250 caracteres.",
                None,
            )

        datos_validados = (
            codigo_limpio,
            especie_limpia,
            sexo_limpio,
            fNacimiento_limpia,
            fIngreso_limpia,
            pesoInicial_limpio,
            estado_salud_limpio,
            observaciones_limpias,
        )
        return True, "", datos_validados

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
        especie = self.limpiar_espacios(self.vista.especie.get())
        sexo = self.limpiar_espacios(self.vista.sexo.get())
        fNacimiento = self.limpiar_espacios(self.vista.fNacimiento.get())
        fIngreso = self.limpiar_espacios(self.vista.fIngreso.get())
        pesoInicial= self.limpiar_espacios(self.vista.pesoInicial.get())
        estado_salud = self.limpiar_espacios(self.vista.estado_salud.get())
        observaciones = self.limpiar_espacios(self.vista.observaciones.get("1.0", "end"))
        valido, mensaje, datos = self.validar_campos_animales(
            codigo, especie,sexo,fNacimiento,fIngreso,pesoInicial,estado_salud,observaciones 
        )
        if not valido:
            CTkMessagebox.CTkMessagebox(
                title="Validación",
                message=mensaje,
                icon="warning",
            )
            return
           

        codigo_ok, especie_ok, sexo_ok,fNacimiento_ok,fIngreso_ok,pesoInicial_ok,estado_salud_ok,observaciones_ok= datos

        nuevo_animal = AnimalesC(codigo, especie,sexo,fNacimiento,fIngreso,pesoInicial,estado_salud,observaciones)
        respuesta = nuevo_animal.insertar()
        
        self.respuesta_sql(respuesta)
        if respuesta:
            self.refrescar_tabla(ir_a_ultima_pagina=False)    
            self.vista.limpiar_campos_anadir()

    def eliminarController(self,codigo):
        codigo = self.vista.codigo_eliminar
        resp= self.confirmacion("eliminar")
        if resp:
            respuesta=AnimalesC.eliminar(codigo)
            self.respuesta_sql(respuesta)
        else:
            respuesta=False
            self.respuesta_sql(respuesta)
        self.refrescar_tabla(False)

    def modificarController(self):
        codigo = self.limpiar_espacios(self.vista.codigo.get())
        especie = self.limpiar_espacios(self.vista.especie.get())
        sexo = self.limpiar_espacios(self.vista.sexo.get())
        fNacimiento = self.limpiar_espacios(self.vista.fNacimiento.get())
        fIngreso = self.limpiar_espacios(self.vista.fIngreso.get())
        pesoInicial= self.limpiar_espacios(self.vista.pesoInicial.get())
        estado_salud = self.limpiar_espacios(self.vista.estado_salud.get())
        observaciones = self.limpiar_espacios(self.vista.observaciones.get("1.0", "end"))
        valido, mensaje, datos = self.validar_campos_animales(
            codigo, especie,sexo,fNacimiento, fIngreso, pesoInicial,estado_salud, observaciones
        )

        if not valido:
            CTkMessagebox.CTkMessagebox(
                title="Validación",
                message=mensaje,
                icon="warning",
            )
            return
        (
            codigo_ok,
            especie_ok,
            sexo_ok,
            fNacimiento_ok,
            fIngreso_ok,
            pesoInicial_ok,
            estado_salud_ok,
            observaciones_ok,
        ) = datos

        try:
            peso_num = float(str(pesoInicial_ok).replace(",", "."))
            if peso_num <= 0:
                raise ValueError
        except ValueError:
            CTkMessagebox.CTkMessagebox(
                title="Validación",
                message="El peso debe ser un número mayor que 0.",
                icon="warning",
            )
            return

        animal_actualizado = AnimalesC(
            codigo_ok,
            especie_ok,
            sexo_ok,
            fNacimiento_ok,
            fIngreso_ok,
            peso_num,
            estado_salud_ok,
            observaciones_ok,
        )

        respuesta = animal_actualizado.actualizar()
        self.respuesta_sql(respuesta)
        if respuesta:
            if hasattr(self.vista, "vModificar") and self.vista.vModificar.winfo_exists():
                self.vista.vModificar.destroy()
            self.refrescar_tabla(ir_a_ultima_pagina=False)
   


    def mostrarController(self):
        datos = AnimalesC.mostrar() or []
        self.registros_mostrar = datos
        self.registros_filtrados = list(datos)
        self.pagina_actual = 0
        pagina_datos, inicio, info_pag = self.obtener_pagina_actual()
        self.vista.renderizar_tabla()
        return datos

    def buscarController(self, criterio):
        criterio_limpio = (criterio or "").strip()
        if criterio_limpio:
            self.registros_filtrados = AnimalesC.filtrar(criterio_limpio) or []
        else:
            if not self.registros_mostrar:
                self.registros_mostrar = AnimalesC.mostrar() or []
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
        datos_actualizados = AnimalesC.mostrar() or []
        datos_actualizados = AnimalesC.mostrar() or []
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

    def calcular_edad(self, fecha_nacimiento):
        try:
            nacimiento = datetime.strptime(
                (fecha_nacimiento or "").strip(), "%d/%m/%Y"
            ).date()
        except ValueError:
            return "N/D"

        hoy = date.today()
        if nacimiento > hoy:
            return "0 meses"

        meses_totales = (hoy.year - nacimiento.year) * 12 + (hoy.month - nacimiento.month)
        if hoy.day < nacimiento.day:
            meses_totales -= 1

        meses_totales = max(0, meses_totales)

        if meses_totales < 12:
            return "1 mes" if meses_totales == 1 else f"{meses_totales} meses"

        anios = meses_totales // 12
        return "1 año" if anios == 1 else f"{anios} años"