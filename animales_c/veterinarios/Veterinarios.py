

import sqlite3
from conexionBD import conectar


class Veterinarios:
    def __init__(self, num_empleado, nombre, apellido1, apellido2, cargo,
                 calle, col, num, codigo_postal, telefono, correo):
        registros_prueba = []
        self.num_empleado = num_empleado
        self.nombre = nombre
        self.apellido1 = apellido1
        self.apellido2 = apellido2
        self.cargo = cargo
        self.calle = calle
        self.col = col
        self.num = num
        self.codigo_postal = codigo_postal
        self.telefono = telefono
        self.correo = correo

    @property
    def num_empleado(self):
        return self._num_empleado

    @num_empleado.setter
    def num_empleado(self, num_empleado):
        self._num_empleado = num_empleado

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        self._nombre = nombre

    @property
    def apellido1(self):
        return self._apellido1

    @apellido1.setter
    def apellido1(self, apellido1):
        self._apellido1 = apellido1

    @property
    def apellido2(self):
        return self._apellido2

    @apellido2.setter
    def apellido2(self, apellido2):
        self._apellido2 = apellido2

    @property
    def cargo(self):
        return self._cargo

    @cargo.setter
    def cargo(self, cargo):
        self._cargo = cargo

    @property
    def calle(self):
        return self._calle

    @calle.setter
    def calle(self, calle):
        self._calle = calle

    @property
    def col(self):
        return self._col

    @col.setter
    def col(self, col):
        self._col = col

    @property
    def num(self):
        return self._num

    @num.setter
    def num(self, num):
        self._num = num

    @property
    def codigo_postal(self):
        return self._codigo_postal

    @codigo_postal.setter
    def codigo_postal(self, codigo_postal):
        self._codigo_postal = codigo_postal

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, telefono):
        self._telefono = telefono

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, correo):
        self._correo = correo

    def insertar(self):
        conexion = conectar()

        if conexion:
            try:
                cursor = conexion.cursor()

                cursor.execute("""
                    INSERT INTO veterinarios (
                        num_empleado, nombre, apellido1, apellido2,
                        cargo, calle, col, num, codigo_postal,
                        telefono, correo
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    self._num_empleado,
                    self._nombre,
                    self._apellido1,
                    self._apellido2,
                    self._cargo,
                    self._calle,
                    self._col,
                    self._num,
                    self._codigo_postal,
                    self._telefono,
                    self._correo
                ))

                conexion.commit()
                return True

            except sqlite3.Error as e:
                print("Error al insertar veterinario:", e)
                return False

            finally:
                conexion.close()

        return False

    def actualizar(self):
        conexion = conectar()

        if conexion:
            try:
                cursor = conexion.cursor()

                cursor.execute("""
                    UPDATE veterinarios
                    SET nombre = ?,
                        apellido1 = ?,
                        apellido2 = ?,
                        cargo = ?,
                        calle = ?,
                        col = ?,
                        num = ?,
                        codigo_postal = ?,
                        telefono = ?,
                        correo = ?
                    WHERE num_empleado = ?
                """, (
                    self._nombre,
                    self._apellido1,
                    self._apellido2,
                    self._cargo,
                    self._calle,
                    self._col,
                    self._num,
                    self._codigo_postal,
                    self._telefono,
                    self._correo,
                    self._num_empleado
                ))

                conexion.commit()

                if cursor.rowcount > 0:
                    return True
                else:
                    return False

            except sqlite3.Error as e:
                print("Error al actualizar veterinario:", e)
                return False

            finally:
                conexion.close()

        return False

    @staticmethod
    def eliminar(num_empleado):
        conexion = conectar()

        if conexion:
            try:
                cursor = conexion.cursor()

                cursor.execute("""
                    DELETE FROM veterinarios
                    WHERE num_empleado = ?
                """, (num_empleado,))

                conexion.commit()

                if cursor.rowcount > 0:
                    return True
                else:
                    return False

            except sqlite3.Error as e:
                print("Error al eliminar veterinario:", e)
                return False

            finally:
                conexion.close()

        return False

    @staticmethod
    def mostrar():
        conexion = conectar()

        if conexion:
            try:
                cursor = conexion.cursor()

                cursor.execute("""
                    SELECT * FROM veterinarios
                    ORDER BY num_empleado
                """)

                return cursor.fetchall()

            except sqlite3.Error as e:
                print("Error al mostrar veterinarios:", e)
                return []

            finally:
                conexion.close()

        return []

    @staticmethod
    def buscar(valor):
        conexion = conectar()

        if conexion:
            try:
                cursor = conexion.cursor()

                cursor.execute("""
                    SELECT * FROM veterinarios
                    WHERE num_empleado = ? OR nombre = ?
                """, (valor, valor))

                return cursor.fetchone()

            except sqlite3.Error as e:
                print("Error al buscar veterinario:", e)
                return None

            finally:
                conexion.close()

        return None

    @staticmethod
    def filtrar(criterio):
        conexion = conectar()

        if conexion:
            try:
                cursor = conexion.cursor()

                cursor.execute("""
                    SELECT * FROM veterinarios
                    WHERE CAST(num_empleado AS TEXT) LIKE ?
                    OR nombre LIKE ?
                    OR apellido1 LIKE ?
                    OR apellido2 LIKE ?
                    OR cargo LIKE ?
                    OR correo LIKE ?
                    ORDER BY num_empleado
                """, (
                    f"%{criterio}%",
                    f"%{criterio}%",
                    f"%{criterio}%",
                    f"%{criterio}%",
                    f"%{criterio}%",
                    f"%{criterio}%"
                ))

                return cursor.fetchall()

            except sqlite3.Error as e:
                print("ERROR SQLITE AL INSERTAR:", repr(e))
                return False
            finally:
                conexion.close()

        return []
