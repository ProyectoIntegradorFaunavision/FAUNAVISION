from conexionBD import conectar


class Especies:
    def __init__(self, id_especie, nombre_especie, nombre_cientifico):
        self._id_especie = id_especie
        self._nombre_especie = nombre_especie
        self._nombre_cientifico = nombre_cientifico

    @property
    def id_especie(self):
        return self._id_especie

    @property
    def nombre_especie(self):
        return self._nombre_especie

    @property
    def nombre_cientifico(self):
        return self._nombre_cientifico

    @id_especie.setter
    def id_especie(self, _id_especie):
        self.__id_especie = _id_especie

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
                    (self.id_especie, self.nombre_especie, self.nombre_cientifico),
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
                    "update especies set nombre_especie=?, nombre_cientifico=? where id_especie=?",
                    (self.nombre_especie, self.nombre_cientifico, self.id_especie),
                )
                conexion.commit()
                return True
            except Exception as e:
                print("Error al actualizar especie:", e)
                return False
        return False    
    #Eliminar especie por código
    @staticmethod
    def eliminar(id_especie):
        conexion = conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("delete from especies where id_especie=?", (id_especie,))
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
        conexion = conectar()
        if not conexion:
            return []
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "select * from especies where id_especie=? or nombre_especie=? or nombre_cientifico" ,
                (valor, valor,valor),
            )
            return cursor.fetchone()
        except Exception as e:
            print("Error al buscar especie:", e)
            return None

    @staticmethod
    def filtrar(criterio):
        conexion = conectar()
        if not conexion:
            return []
        cursor = conexion.cursor()
        try:
            patron = f"%{criterio}%"
            cursor.execute(
                """
                SELECT * FROM especies
                WHERE LOWER(id_especie) LIKE LOWER(?)
                   OR LOWER(nombre_especie) LIKE LOWER(?)
                   OR LOWER(nombre_cientifico) LIKE LOWER(?)
                """,
                (patron, patron, patron),
            )
            return cursor.fetchall()
        except Exception as e:
            print("Error al filtrar especies:", e)
            return []
