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
        self._talla = talla

    @observaciones.setter
    def observaciones(self, observaciones):
        self._observaciones = observaciones

    def insertar(self):
        try:
            cursor.execute(
                "insert into animales_c values(%s,%s,%s,%s,%s,%s,%s,%s)",
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
        try:
            cursor.execute(
                "UPDATE animales_c SET especie=%s, sexo=%s, fNacimiento=%s, fIngreso=%s, pesoInicial=%s, estado_salud=%s, observaciones=%s WHERE codigo=%s",
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
    def eliminar():
        try:
            cursor.execute("delete from animales_c where codigo=%s", (self._codigo,))
            conexion.commit()
            return True
        except:
            return False

    @staticmethod
    def mostrar():
        try:
            cursor.execute("select * from animales_c")
            return cursor.fetchall()
        except:
            return []

    def buscar(self):
        pass

    def limpiar(self):
        pass

    def filtrar(self):
        pass
