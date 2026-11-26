
from conexionBD import crear_db
from models.usuarios import Usuarios
#usuarios y contraseñas por defecto para el primer inicio de sesión
#Tipo	        Usuario	    Contraseña
#Administrador	admin	    Admin123*
#Veterinario	veterinario	Veterinario123*

# Inicializar la base de datos
crear_db()

usuarios = Usuarios()

# Crear tabla de usuarios
usuarios.crear_tabla()

# Crear administrador
resultado = usuarios.registrar_usuario(
    "admin",
    "Admin123*",
    "Administrador"
)

if resultado:
    print("Administrador creado correctamente.")
else:
    print("El administrador ya existe.")

# Crear veterinario
resultado = usuarios.registrar_usuario(
    "veterinario",
    "Veterinario123*",
    "Veterinario"
)

if resultado:
    print("Veterinario creado correctamente.")
else:
    print("El veterinario ya existe.")
