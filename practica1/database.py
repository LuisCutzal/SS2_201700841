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
        
        
        
    except pyodbc.Error as e:
        print(f"Error al crear la tabla: {e} del modelo")
    finally:
        cursor.close()