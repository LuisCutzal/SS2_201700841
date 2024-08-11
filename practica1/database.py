import pyodbc

def limpiar_modelo(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
        tablas = cursor.fetchall()
        #quitar restricciones de las llaves forameas
        for tabla in tablas:
            tabla_nombre = tabla[0]
            try:
                cursor.execute(f"ALTER TABLE {tabla_nombre} NOCHECK CONSTRAINT ALL")
            except pyodbc.Error as e:
                print(f"Error al deshabilitar las claves foráneas en la tabla {tabla_nombre}: {e}")
        for tabla in tablas:
            tabla_nombre = tabla[0]
            try:
                cursor.execute(f"TRUNCATE TABLE {tabla_nombre}")
            except pyodbc.Error as e:
                try:
                    cursor.execute(f"DELETE FROM {tabla_nombre}")
                except pyodbc.Error as e:
                    print(f"Error al eliminar datos de la tabla {tabla_nombre}: {e}")
        # agregar las restricciones de las llaves foraneas
        for tabla in tablas:
            tabla_nombre = tabla[0]
            try:
                cursor.execute(f"ALTER TABLE {tabla_nombre} WITH CHECK CHECK CONSTRAINT ALL")
            except pyodbc.Error as e:
                print(f"Error al rehabilitar las claves foráneas en la tabla {tabla_nombre}: {e}")
        conexion.commit()
        print("Se limpiaron los datos de las tablas correctamente")
    except pyodbc.Error as e:
        print(f"Error al limpiar los datos: {e}")
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
                       CREATE TABLE Pasajero(
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
                       CREATE TABLE Aeropuerto(
                           Id_aeropuerto INT IDENTITY(1,1) PRIMARY KEY,
                           Nombre VARCHAR(100) NOT NULL,
                           Codigo_aeropuerto VARCHAR(50) NOT NULL,
                           Pais VARCHAR(50) NOT NULL,
                           Continente_aeropuerto VARCHAR(50) NOT NULL
                       )
                       """)
        
        cursor.execute("""
                       CREATE TABLE Piloto(
                           Id_piloto INT IDENTITY(1,1) PRIMARY KEY,
                           Nombre VARCHAR(255) NOT NULL
                       )
                       """)
                
        cursor.execute("""
                       CREATE TABLE Vuelo(
                           Id_vuelo INT IDENTITY(1,1) PRIMARY KEY,
                           Estado VARCHAR(50) NOT NULL,
                           Fecha DATE NOT NULL,
                           Id_pasajero INT NOT NULL,
                           Id_aeropuerto INT NOT NULL,
                           FOREIGN KEY (Id_pasajero) REFERENCES Pasajero(Id_pasajero),
                           FOREIGN KEY (Id_aeropuerto) REFERENCES Aeropuerto(Id_aeropuerto)
                       )
                       """)
        conexion.commit()
        print("Modelo creado con éxito.")        
    except pyodbc.Error as e:
        print(f"Error al crear la tabla: {e} del modelo")
    finally:
        cursor.close()