import pyodbc
from database import borrarModelo, crearModelo

server = 'CUTZALL\\SQLEXPRESS'
database = 'practica1'
username = 'luisc'
password = 'C0malap@123'

def connect_to_db():
    try:
        # Intenta conectarte a la base de datos especificada
        conexion = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
        return conexion
    except pyodbc.Error as e:
        if 'Cannot open database' in str(e):
            print(f"La base de datos '{database}' no existe. Creándola...")
            # Conéctate a 'master' para crear la base de datos
            conexion = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE=master;UID={username};PWD={password}')
            crear_base_datos(conexion, database)
            conexion.close()
            # Intenta conectarte nuevamente a la base de datos recién creada
            conexion = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
            return conexion
        else:
            print(f"Error al conectar a la base de datos: {e}")
            return None

def crear_base_datos(conexion, nombre_bd):
    try:
        cursor = conexion.cursor()
        # Ejecuta el comando CREATE DATABASE sin transacción
        cursor.execute(f"USE master; CREATE DATABASE {nombre_bd};")
        print(f"Base de datos '{nombre_bd}' creada exitosamente.")
    except pyodbc.Error as e:
        print(f"Error al crear la base de datos: {e}")
    finally:
        cursor.close()

def menu():
    while True:
        print("***************************")
        print("* 1. Borrar modelo        *")
        print("* 2. Crear modelo         *")
        print("* 3. Extraer información  *")
        print("* 4. Cargar información   *")
        print("* 5. Realizar Consultas   *")
        print("* 6. Salir                *")
        print("***************************")
        
        eleccion = input("Selecciona una opción (1-6): ")
        
        if eleccion == '1':
            conexion = connect_to_db()
            if conexion:
                borrarModelo(conexion)
                conexion.close()
        elif eleccion == '2':
            conexion = connect_to_db()
            
        elif eleccion == '3':
            print("3")
        elif eleccion == '4':
            print("4")
        elif eleccion == '5':
            print("5")
        elif eleccion == '6':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, elige una opción entre 1 y 6.")

if __name__ == "__main__":
    menu()
