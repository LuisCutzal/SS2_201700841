import pyodbc
import os
from database import crearModelo, limpiar_modelo, eliminar_base_de_datos
from elt import extract_information, clean_and_load_data
server = 'CUTZALL\\SQLEXPRESS'
username = 'luisc'
password = 'C0malap@123'

def connect_to_sql_server():
    try:
        # Conexión al servidor SQL con autenticación de Windows y autocommit=True
        conexion = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};Trusted_Connection=yes;', autocommit=True)
        #coneccion con usuario y password
        #conexion = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};UID={username};PWD={password}', autocommit=True)
        return conexion
    except pyodbc.Error as e:
        print(f"Error al conectar a SQL Server: {e}")
        return None

def connect_to_database(nombre_bd):
    try:
        conexion = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={nombre_bd};Trusted_Connection=yes;', autocommit=True)
        return conexion
    except pyodbc.Error as e:
        print(f"Error al conectar a la base de datos '{nombre_bd}': {e}")
        return None


def crear_base_datos(nombre_bd):
    try:
        conexion = connect_to_sql_server()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute(f"CREATE DATABASE {nombre_bd}")
            print(f"Base de datos '{nombre_bd}' creada exitosamente.")  
            cursor.close()
            conexion.close()
    except pyodbc.Error as e:
        print(f"Error al crear la base de datos: {e}")

def get_relative_path(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)
    return file_path

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
            print("Opción 1 seleccionada.")
            nombre_bd = input("Ingresa el nombre del Modelo: ")
            conexion = connect_to_database(nombre_bd)
            limpiar_modelo(conexion)
            #eliminar_base_de_datos(conexion, nombre_bd)
            conexion.close()
        elif eleccion == '2':
            nombre_bd = input("Ingresa el nombre del Modelo: ")
            crear_base_datos(nombre_bd)
            conexion = connect_to_database(nombre_bd)
            crearModelo(conexion)
            conexion.close()
        elif eleccion == '3':
            print("Opción 3 seleccionada.")
            nombre_bd = input("Ingresa el nombre del Modelo: ")
            conexion = connect_to_database(nombre_bd)
            file_name = 'VuelosDataSet.csv'
            relative_path = get_relative_path(file_name)
            extract_information(relative_path, conexion)
            conexion.close()
        elif eleccion == '4':
            print("Opción 4 seleccionada.")
            nombre_bd = input("Ingresa el nombre del Modelo: ")
            conexion = connect_to_database(nombre_bd)
            clean_and_load_data(conexion)
            conexion.close()
        elif eleccion == '5':
            print("Opción 5 seleccionada.")            
        elif eleccion == '6':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, elige una opción entre 1 y 6.")

if __name__ == "__main__":
    menu()
