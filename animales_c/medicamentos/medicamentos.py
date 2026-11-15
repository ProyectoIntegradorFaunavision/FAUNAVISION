from conexionBD import conectar


class Medicamentos:
    def __init__(self, id_medicamento, nombre_medicamento, tipo, laboratorio, stock, descripcion):
        self.id_medicamento = id_medicamento
        self.nombre_medicamento = nombre_medicamento
        self.tipo = tipo
        self.laboratorio = laboratorio
        self.stock = stock
        self.descripcion = descripcion

    @property
    def id_medicamento(self):
        return self._id_medicamento

    @id_medicamento.setter
    def id_medicamento(self, id_medicamento):
        self._id_medicamento = id_medicamento

    @property
    def nombre_medicamento(self):
        return self._nombre_medicamento

    @nombre_medicamento.setter
    def nombre_medicamento(self, nombre_medicamento):
        self._nombre_medicamento = nombre_medicamento

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, tipo):
        self._tipo = tipo

    @property
    def laboratorio(self):
        return self._laboratorio

    @laboratorio.setter
    def laboratorio(self, laboratorio):
        self._laboratorio = laboratorio

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, stock):
        self._stock = stock

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, descripcion):
        self._descripcion = descripcion

    def insertar(self):
        conexion = conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute(
                    "INSERT INTO medicamentos VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        self._id_medicamento,
                        self._nombre_medicamento,
                        self._tipo,
                        self._laboratorio,
                        self._stock,
                        self._descripcion,
                    ),
                )
                conexion.commit()
                return True
            except Exception as e:
                print("Error al insertar medicamento:", e)
                return False
        return False

    def actualizar(self):
        conexion = conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute(
                    """UPDATE medicamentos 
                       SET nombre_medicamento=?, tipo=?, laboratorio=?, stock=?, descripcion=? 
                       WHERE id_medicamento=?""",
                    (
                        self._nombre_medicamento,
                        self._tipo,
                        self._laboratorio,
                        self._stock,
                        self._descripcion,
                        self._id_medicamento,
                    ),
                )
                conexion.commit()
                return True
            except Exception as e:
                print("Error al actualizar medicamento:", e)
                return False
        return False

    @staticmethod
    def eliminar(id_medicamento):
        conexion = conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute(
                    "DELETE FROM medicamentos WHERE id_medicamento=?",
                    (id_medicamento,),
                )
                conexion.commit()
                return True
            except Exception as e:
                print("Error al eliminar medicamento:", e)
                return False
        return False

    @staticmethod
    def mostrar():
        conexion = conectar()
        if not conexion:
            return []
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT * FROM medicamentos")
            return cursor.fetchall()
        except Exception as e:
            print("Error al mostrar medicamentos:", e)
            return []

    @staticmethod
    def buscar(valor):
        conexion = conectar()
        if not conexion:
            return None
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "SELECT * FROM medicamentos WHERE id_medicamento=? OR nombre_medicamento=?",
                (valor, valor),
            )
            return cursor.fetchone()
        except Exception as e:
            print("Error al buscar medicamento:", e)
            return None

    @staticmethod
    def filtrar(criterio):
        conexion = conectar()
        if not conexion:
            return []
        cursor = conexion.cursor()
        try:
            cursor.execute(
                """SELECT * FROM medicamentos 
                   WHERE id_medicamento LIKE ? OR nombre_medicamento LIKE ? OR tipo LIKE ? OR laboratorio LIKE ?""",
                (f"%{criterio}%", f"%{criterio}%", f"%{criterio}%", f"%{criterio}%"),
            )
            return cursor.fetchall()
        except Exception as e:
            print("Error al filtrar medicamentos:", e)
            return []