
import sqlite3
import hashlib
import secrets

from conexionBD import conectar


class Usuarios:

    def crear_tabla(self):
        conexion = conectar()

        if conexion is None:
            print("No se pudo conectar a la base de datos.")
            return

        try:
            cursor = conexion.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios(
                    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre_completo TEXT NOT NULL DEFAULT '',
                    usuario TEXT NOT NULL UNIQUE,
                    contrasena TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    tipo_usuario TEXT NOT NULL
                )
            ''')

            # Comprobar si la columna ya existe
            cursor.execute("PRAGMA table_info(usuarios)")
            columnas = [columna[1] for columna in cursor.fetchall()]

            # Agregarla si la tabla ya existía sin ella
            if "nombre_completo" not in columnas:
                cursor.execute('''
                    ALTER TABLE usuarios
                    ADD COLUMN nombre_completo TEXT NOT NULL DEFAULT ''
                ''')

            conexion.commit()

        except sqlite3.Error as e:
            print("Error al crear la tabla de usuarios:", e)

        finally:
            conexion.close()

    def registrar_usuario(self, usuario, contrasena, tipo_usuario, nombre_completo=""):

        salt = secrets.token_hex(16)

        contrasena_hash = hashlib.pbkdf2_hmac(
            'sha256',
            contrasena.encode(),
            salt.encode(),
            100000
        ).hex()

        conexion = conectar()

        if conexion is None:
            print("No se pudo conectar a la base de datos.")
            return False

        try:
            cursor = conexion.cursor()

            cursor.execute('''
                INSERT INTO usuarios
                (nombre_completo, usuario, contrasena, salt, tipo_usuario)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                nombre_completo,
                usuario,
                contrasena_hash,
                salt,
                tipo_usuario
            ))

            conexion.commit()
            return True

        except sqlite3.IntegrityError:
            return False

        except sqlite3.Error as e:
            print("Error al registrar usuario:", e)
            return False

        finally:
            conexion.close()

    def buscar_usuario(self, usuario):

        conexion = conectar()

        if conexion is None:
            return None

        try:
            cursor = conexion.cursor()

            cursor.execute('''
                SELECT id_usuario, nombre_completo, usuario, contrasena, salt, tipo_usuario
                FROM usuarios
                WHERE usuario = ?
            ''', (usuario,))

            resultado = cursor.fetchone()
            return resultado

        except sqlite3.Error as e:
            print("Error al buscar usuario:", e)
            return None

        finally:
            conexion.close()

    def verificar_contrasena(self, contrasena, salt, contrasena_hash):

        nueva_contrasena = hashlib.pbkdf2_hmac(
            'sha256',
            contrasena.encode(),
            salt.encode(),
            100000
        ).hex()

        return secrets.compare_digest(
            nueva_contrasena,
            contrasena_hash
        )
