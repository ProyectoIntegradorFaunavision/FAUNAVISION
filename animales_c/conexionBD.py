import sqlite3

def crear_db():
    try:
        conexion = sqlite3.connect('faunavision.db')
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS especies(
                codigo INTEGER PRIMARY KEY,
                nombre_especie TEXT NOT NULL,
                nombre_cientifico TEXT NOT NULL UNIQUE
            )
            ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS animales_c(
                codigo TEXT PRIMARY KEY,
                especie INTEGER NOT NULL,
                sexo TEXT NOT NULL,
                fNacimiento TEXT NOT NULL,
                fIngreso TEXT NOT NULL,
                pesoInicial REAL NOT NULL,
                estado_salud TEXT NOT NULL,
                observaciones TEXT,
                FOREIGN KEY (especie) REFERENCES especies(codigo)
            )
            ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medicamentos(
                id_medicamento INTEGER PRIMARY KEY,
                nombre_medicamento TEXT NOT NULL,
                tipo TEXT NOT NULL,
                laboratorio TEXT NOT NULL,
                stock INTEGER NOT NULL,
                descripcion TEXT
            )
            ''')
        cursor.execute('''

            CREATE TABLE IF NOT EXISTS veterinarios(
                num_empleado INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                apellido1 TEXT NOT NULL,
                apellido2 TEXT NOT NULL,
                cargo TEXT NOT NULL,
                calle TEXT NOT NULL,
                col TEXT NOT NULL,
                num INTEGER NOT NULL,
                codigo_postal INTEGER NOT NULL,
                telefono TEXT NOT NULL,
                correo TEXT NOT NULL UNIQUE
            )
            ''')
        cursor.execute('''

            CREATE TABLE IF NOT EXISTS expedientes(
                id_historial INTEGER PRIMARY KEY,
                animal INTEGER NOT NULL,
                veterinario INTEGER NOT NULL,
                medicamento INTEGER NOT NULL,
                fechaAplicacion TEXT NOT NULL,
                fechaProxima TEXT NOT NULL,
                tipo_evento TEXT NOT NULL,
                peso_actual REAL NOT NULL,
                diagnostico_motivo TEXT NOT NULL,
                FOREIGN KEY (animal) REFERENCES animales_c(codigo),
                FOREIGN KEY (veterinario) REFERENCES veterinarios(num_empleado),
                FOREIGN KEY (medicamento) REFERENCES medicamentos(id_medicamento)
            )

        ''')
        conexion.commit()
        conexion.close()
    except sqlite3.Error as e:
        print(f"Error al crear la base de datos: {e}")
        return None

def conectar():
    try:
        conexion = sqlite3.connect('faunavision.db')
        conexion.execute("PRAGMA foreign_keys = ON;")
        
        return conexion
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
