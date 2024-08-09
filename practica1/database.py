import pyodbc

def limpiar_modelo(conexion):
    try:
        cursor = conexion.cursor()
        # Obtener una lista de todas las tablas en la base de datos
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
        tablas = cursor.fetchall()
        for tabla in tablas:
            tabla_nombre = tabla[0]
            try:
                cursor.execute(f"TRUNCATE TABLE {tabla_nombre}")
                print(f"Datos eliminados de la tabla: {tabla_nombre}")
            except pyodbc.Error as e:
                try:
                    cursor.execute(f"DELETE FROM {tabla_nombre}")
                    print(f"Datos eliminados de la tabla (usando DELETE): {tabla_nombre}")
                except pyodbc.Error as e:
                    print(f"Error al eliminar datos de la tabla {tabla_nombre}: {e}")
        for tabla in tablas:
            tabla_nombre = tabla[0]
            try:
                cursor.execute(f"DROP TABLE {tabla_nombre}")
                print(f"Tabla eliminada: {tabla_nombre}")
            except pyodbc.Error as e:
                print(f"Error al eliminar la tabla {tabla_nombre}: {e}")
        conexion.commit()
        print("Se limpiaron y eliminaron las tablas correctamente")
    except pyodbc.Error as e:
        print(f"Error al limpiar las tablas: {e}")
    finally:
        cursor.close()

def eliminar_base_de_datos(conexion, nombre_bd):
    try:
        cursor = conexion.cursor()
        cursor.execute("USE master") #se debe de cambiar a la base de datos master   
        cursor.execute(f"DROP DATABASE [{nombre_bd}]")
        conexion.commit()
        print(f"Se eliminó la base de datos '{nombre_bd}' correctamente")
    except pyodbc.Error as e:
        print(f"Error al eliminar la base de datos: {e}")
    finally:
        cursor.close()

def crearModelo(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute("""
                       CREATE TABLE pasajero(
                           Id_pasajero INT IDENTITY(1,1) PRIMARY KEY,
                           Identificacion VARCHAR(50) NOT NULL,
                           Nombre VARCHAR(50) NOT NULL,
                           Apellido VARCHAR(50) NOT NULL,
                           Sexo VARCHAR(10) NOT NULL,
                           Edad INT NOT NULL,
                           Nacionalidad VARCHAR(50) NOT NULL
                       )
                       """)
        
        cursor.execute("""
                       CREATE TABLE aeropuerto(
                           Id_aeropuerto INT IDENTITY(1,1) PRIMARY KEY,
                           Codigo_aeropuerto VARCHAR(15) NOT NULL,
                           Nombre VARCHAR(100) NOT NULL,
                           Pais VARCHAR(50) NOT NULL,
                           Continente_aeropuerto VARCHAR(50) NOT NULL
                       )
                       """)
        
        cursor.execute("""
                       CREATE TABLE piloto(
                           Id_piloto INT IDENTITY(1,1) PRIMARY KEY,
                           Nombre VARCHAR(50) NOT NULL
                       )
                       """)
        
        cursor.execute("""
                       CREATE TABLE vuelo(
                           Id_vuelo INT IDENTITY(1,1) PRIMARY KEY,
                           Fecha_salida DATE NOT NULL,
                           Estado VARCHAR(50) NOT NULL,
                           Id_pasajero INT NOT NULL, 
                           Id_aeropuerto INT NOT NULL,
                           Id_piloto INT NOT NULL,
                           FOREIGN KEY (Id_pasajero) REFERENCES pasajero(Id_pasajero),
                           FOREIGN KEY (Id_aeropuerto) REFERENCES aeropuerto(Id_aeropuerto),
                           FOREIGN KEY (Id_piloto) REFERENCES piloto(Id_piloto)
                       )
                       """)
        conexion.commit()
        print("Modelo creado con éxito.")        
    except pyodbc.Error as e:
        print(f"Error al crear la tabla: {e} del modelo")
    finally:
        cursor.close()