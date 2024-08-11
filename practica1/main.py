import pyodbc
import os
from database import crearModelo, limpiar_modelo, eliminar_base_de_datos
from elt import extract_information, clean_and_load_data
from querys import query1, query2, query3, query4, query5, query6,query7, query8, query9, query10
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
        print(f"Error al conectar a la base de datos '{nombre_bd}'.")
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

def menu_querys():
    while True:
        print("****************************")
        print("* 1.  Consulta 1           *")
        print("* 2.  Consulta 2           *")
        print("* 3.  Consulta 3           *")
        print("* 4.  Consulta 4           *")
        print("* 5.  Consulta 5           *")
        print("* 6.  Consulta 6           *")
        print("* 7.  Consulta 7           *")
        print("* 8.  Consulta 8           *")
        print("* 9.  Consulta 9           *")
        print("* 10. Consulta 10          *")
        print("* 11. Regresar             *")
        print("****************************")
        eleccion = input("Selecciona una opción (1-11): ")
        if eleccion == "11":
            break
        nombre_bd = input("Ingresa el nombre del Modelo: ")
        if connect_to_database(nombre_bd) == None:
            print("Verifique el nombre y vuelva a intentarlo")
        else:
            conexion = connect_to_database(nombre_bd)
            if eleccion == '1':
                query1(conexion)
                conexion.close()
            elif eleccion == "2":
                query2(conexion)
                conexion.close()
            elif eleccion == "3":
                query3(conexion)
                conexion.close()
            elif eleccion == "4":
                query4(conexion)
                conexion.close()
            elif eleccion == "5":
                query5(conexion)
                conexion.close()
            elif eleccion == "6":
                query6(conexion)
                conexion.close()
            elif eleccion == "7":
                query7(conexion)
                conexion.close()
            elif eleccion == "8":
                query8(conexion)
                conexion.close()
            elif eleccion == "9":
                query9(conexion)
                conexion.close()
            elif eleccion == "10":
                query10(conexion)
                conexion.close()
            elif eleccion == "11":
                print("Regresando al menu principal")
                break
            else:print("Opción no válida. Por favor, elige una opción entre 1 y 11.")
            
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
        if eleccion == "2":
            nombre_bd = input("Ingresa el nombre del Modelo: ")
            crear_base_datos(nombre_bd)
            conexion = connect_to_database(nombre_bd)
            crearModelo(conexion)
            conexion.close()
        elif eleccion == "5":
            menu_querys()
        elif eleccion == "6":
            print("Saliendo del programa...")
            break
        else:
            nombre_bd = input("Ingresa el nombre del Modelo: ")
            if connect_to_database(nombre_bd) == None:
                print("Verifique el nombre y vuelva a intentarlo")
            else:
                conexion = connect_to_database(nombre_bd)
                if eleccion == "1":
                    limpiar_modelo(conexion)
                    conexion.close()
                elif eleccion == "3":
                    file_name = input("Ingresa el nombre del Archivo: ") #'VuelosDataSet.csv'
                    relative_path = get_relative_path(file_name)
                    extract_information(relative_path, conexion)
                    conexion.close()
                elif eleccion == "4":
                    clean_and_load_data(conexion)
                    conexion.close()
                else: print("Opción no válida. Por favor, elige una opción entre 1 y 6.")
        
if __name__ == "__main__":
    menu()