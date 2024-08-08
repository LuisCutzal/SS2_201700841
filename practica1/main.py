import pyodbc


server = 'CUTZALL\\SQLEXPRESS'
database = 'practica1'
username = 'luisc'
password = 'C0malap@123'

def connect_to_db():
    try:
        conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
        return conn
    except pyodbc.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

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
            print("1")
        elif eleccion == '2':
            print("2")
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
