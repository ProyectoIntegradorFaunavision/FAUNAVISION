from conexionBD import conectar


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
        conexion = conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute(
                    "insert into especies values(?, ?, ?)",
                    (self._codigo, self._nombre_especie, self._nombre_cientifico),
                )
                conexion.commit()
                return True
            except Exception as e:
                print("Error al insertar especie:", e)
                return False
        return False

    def actualizar(self):
        conexion = conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute(
                    "update especies set nombre_especie=?, nombre_cientifico=? where codigo=?",
                    (self._nombre_especie, self._nombre_cientifico, self._codigo),
                )
                conexion.commit()
                return True
            except Exception as e:
                print("Error al actualizar especie:", e)
                return False
        return False    
    #Eliminar especie por código
    @staticmethod
    def eliminar(codigo):
        conexion = conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("delete from especies where codigo=?", (codigo,))
                conexion.commit()
                return True
            except Exception as e:
                print("Error al eliminar especie:", e)
                return False
        return False
    #Mostrar todas las especies
    @staticmethod
    def mostrar():
        conexion = conectar()
        if not conexion:
            return []
        cursor = conexion.cursor()
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
                "select * from especies where codigo=? or nombre_especie=?",
                (valor, valor),
            )
            return cursor.fetchone()
        except Exception as e:
            print("Error al buscar especie:", e)
            return None

    
    def filtrar(self, criterio):
        try:
            cursor.execute(
                "select * from especies where codigo like ? or nombre_especie like ? or nombre_cientifico like ?",
                (f"%{criterio}%", f"%{criterio}%", f"%{criterio}%"),
            )
            return cursor.fetchall()
        except Exception as e:
            print("Error al filtrar especies:", e)
            return []
