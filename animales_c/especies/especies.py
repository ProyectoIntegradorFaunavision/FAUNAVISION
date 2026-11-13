class Especies:
    def __init__(self, codigo, nombre_especie, nombre_cientifico):
        self.codigo = codigo
        self.nombre_especie = nombre_especie
        self.nombre_cientifico = nombre_cientifico

    @property
    def codigo(self):
        return self._codigo

    @property
    def nombre_especie(self):
        return self._nombre_especie

    @property
    def nombre_cientifico(self):
        return self._nombre_cientifico

    @codigo.setter
    def codigo(self, codigo):
        self._codigo = codigo

    @nombre_especie.setter
    def nombre_especie(self, nombre_especie):
        self._nombre_especie = nombre_especie

    @nombre_cientifico.setter
    def nombre_cientifico(self, nombre_cientifico):
        self._nombre_cientifico = nombre_cientifico

    def insertar(self):
        try:
            cursor.execute(
                "insert into especies values(%s,%s,%s)",
                (self._codigo, self._nombre_especie, self._nombre_cientifico),
            )
            conexion.commit()
            return True
        except Exception as e:
            print("Error al insertar especie:", e)
            return False

    def actualizar(self):
        try:
            cursor.execute(
                "update especies set nombre_especie=%s, nombre_cientifico=%s where codigo=%s",
                (self._nombre_especie, self._nombre_cientifico, self._codigo),
            )
            conexion.commit()
            return True
        except Exception as e:
            print("Error al actualizar especie:", e)
            return False
    #Eliminar especie por código
    @staticmethod
    def eliminar(codigo):
        try:
            cursor.execute("delete from especies where codigo=%s", (codigo,))
            conexion.commit()
            return True
        except Exception as e:
            print("Error al eliminar especie:", e)
            return False
    #Mostrar todas las especies
    @staticmethod
    def mostrar():
        try:
            cursor.execute("select * from especies")
            return cursor.fetchall()
        except Exception as e:
            print("Error al mostrar especies:", e)
            return []
    #Buscar especie por código o nombre
    @staticmethod
    def buscar(valor):
        try:
            cursor.execute(
                "select * from especies where codigo=%s or nombre_especie=%s",
                (valor, valor),
            )
            return cursor.fetchone()
        except Exception as e:
            print("Error al buscar especie:", e)
            return None
    def filtrar(self, criterio):
        try:
            cursor.execute(
                "select * from especies where codigo like %s or nombre_especie like %s or nombre_cientifico like %s",
                (f"%{criterio}%", f"%{criterio}%", f"%{criterio}%"),
            )
            return cursor.fetchall()
        except Exception as e:
            print("Error al filtrar especies:", e)
            return []
