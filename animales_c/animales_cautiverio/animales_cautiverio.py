from conexionBD import conectar

class AnimalesC:

    def __init__(
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
        self._codigo = codigo
        # (Actualización de atributos, se agrego crud especies y animales cautiverio)
        self._especie = especie
        self._sexo = sexo
        self._fNacimiento = fNacimiento
        self._fIngreso = fIngreso
        self._pesoInicial = pesoInicial
        self._estado_salud = estado_salud
        self._observaciones = observaciones

    @property
    def codigo(self):
        return self._codigo

    @property
    def especie(self):
        return self._especie

    @property
    def sexo(self):
        return self._sexo

    @property
    def fNacimiento(self):
        return self._fNacimiento

    @property
    def fIngreso(self):
        return self._fIngreso

    @property
    def pesoInicial(self):
        return self._pesoInicial

    @property
    def estado_salud(self):
        return self._estado_salud

    @property
    def observaciones(self):
        return self._observaciones

    @codigo.setter
    def codigo(self, codigo):
        self._codigo = codigo

    @especie.setter
    def especie(self, especie):
        self._especie = especie

    @pesoInicial.setter
    def pesoInicial(self, pesoInicial):
        self._pesoInicial = pesoInicial

    @estado_salud.setter
    def estado_salud(self, estado_salud):
        self._estado_salud = estado_salud

    @fNacimiento.setter
    def fNacimiento(self, fNacimiento):
        self._fNacimiento = fNacimiento

    @fIngreso.setter
    def fIngreso(self, fIngreso):
        self._fIngreso = fIngreso

    @observaciones.setter
    def observaciones(self, observaciones):
        self._observaciones = observaciones

    def insertar(self):
        conexion = conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute(
                "insert into animales_c values(?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    self._codigo,
                    self._especie,
                    self._sexo,
                    self._fNacimiento,
                    self._fIngreso,
                    self._pesoInicial,
                    self._estado_salud,
                    self._observaciones,
                ),
            )
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error al insertar animal: {e}")
                return False
                #     if tipo == "ENTRADA" or tipo == "E":
                #         cursor.execute("UPDATE productos SET stock = stock + %s WHERE codigo = %s", (cantidad, codigo))
                #     elif tipo == "SALIDA" or tipo == "S":
                #         cursor.execute("UPDATE productos SET stock = stock - %s WHERE codigo = %s", (cantidad, codigo))

                #     cursor.execute("UPDATE productos SET precio_total = precio_neto * stock WHERE codigo = %s", (codigo,))

                #     conexionBD.commit()
                #     return True
                #     return False
                # except:
                #     return False

    def actualizar(self):
        conexion = conectar()
        if conexion:
                
            try:
                cursor = conexion.cursor()
                cursor.execute(
                "UPDATE animales_c SET especie=?, sexo=?, fNacimiento=?, fIngreso=?, pesoInicial=?, estado_salud=?, observaciones=? WHERE codigo=?",
                (
                    self._especie,
                    self._sexo,
                    self._fNacimiento,
                    self._fIngreso,
                    self._pesoInicial,
                    self._estado_salud,
                    self._observaciones,
                    self._codigo,
                ),
            )
                conexion.commit()
                return True
            except:
                return False
    @staticmethod
    def eliminar(criterio):
        conexion = conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM animales_c WHERE codigo=?", (criterio,))
                conexion.commit()
                return True
            except:
                return False
    @staticmethod
    def mostrar(criterio):
        conexion = conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM animales_c")
                return cursor.fetchall()
            except:
                return []
    @staticmethod
    def buscar(criterio):
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute(
                    "SELECT * FROM animales_c WHERE codigo=? OR especie=?",
                    (criterio,criterio)
                )
                return cursor.fetchone()
            except:
                return None
    @staticmethod
    def filtrar(criterio):
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("""
                    SELECT * FROM animales_c
                    WHERE cast (codigo as text) like?
                    OR nombre_especie like ?
                    or nombre_cientifico like ?
                    order by codigo
                    """,(
                        f"%{criterio}%",
                        f"%{criterio}%",

                    ))
                
                return cursor.fetchall()
            except:
                return []

