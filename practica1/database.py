import pyodbc

def borrarModelo(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute('DROP TABLE IF EXIST vuelos')
        cursor.execute('DROP TABLE IF EXIST pasajero')
        cursor.execute('DROP TABLE IF EXIST piloto')
        cursor.execute('DROP TABLE IF EXIST aeropuerto')
        conexion.commit()
        print("Se elimino el modelo correctamente")
    except pyodbc.Error as e:
        print(f"Error al eliminar las tabla: {e}")
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
                           Estado VARCHAR(50), NOT NULL,
                           Id_pasajero INT NOT NULL, 
                           Id_aeropuerto INT NOT NULL,
                           Id_piloto INT NOT NULL,
                           FOREIGN KEY (Id_pasajero) REFERENCES pasajero(Id_pasajero),
                           FOREING KEY (Id_aeropuerto) REFERENCES aeropuerto(Id_aeropuerto),
                           FOREING KEY (Id_piloto) REFERENCES piloto(Id_piloto)
                       )
                       """)
        conexion.commit()
        print("Modelo creado con éxito.")        
    except pyodbc.Error as e:
        print(f"Error al crear la tabla: {e} del modelo")
    finally:
        cursor.close()