import pyodbc
import csv
import re
def preprocess_csv(input_file_path, output_file_path):
    with open(input_file_path, 'r', newline='', encoding='utf-8') as infile, \
         open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:
        
        # Leer el archivo línea por línea
        for line in infile:
            # Verificar si la línea contiene comillas dobles
            if '"' in line:
                # Si la línea contiene comillas dobles, omitirla
                continue

            # Escribir la línea en el archivo de salida si no contiene comillas dobles
            outfile.write(line)


def extract_information(file_path, conexion):
    try:
        cursor = conexion.cursor()
        
        # Crear o reemplazar la tabla temporal
        cursor.execute('''
        IF OBJECT_ID('TempData', 'U') IS NOT NULL
            DROP TABLE TempData;

        CREATE TABLE TempData (
            PassengerID VARCHAR(250),
            FirstName VARCHAR(250),
            LastName VARCHAR(250),
            Gender VARCHAR(250),
            Age INT,
            Nationality VARCHAR(250),
            AirportName VARCHAR(250),
            AirportCountryCode VARCHAR(250),
            CountryName VARCHAR(250),
            AirportContinent VARCHAR(250),
            Continents VARCHAR(250),
            DepartureDate VARCHAR(250),
            ArrivalAirport VARCHAR(250),
            PilotName VARCHAR(250),
            FlightStatus VARCHAR(250)
        );
        ''')

        # Usar la ruta del archivo CSV procesado
        processed_file_path = file_path.replace('.csv', '_processed.csv')

        # Ejecutar el preprocesamiento
        preprocess_csv(file_path, processed_file_path)
        
        # Cargar los datos desde el archivo CSV procesado
        cursor.execute(f'''
        BULK INSERT TempData
        FROM '{processed_file_path}'
        WITH (
            FIELDTERMINATOR = ',',
            ROWTERMINATOR = '\\n',
            FIRSTROW = 2,
            FIELDQUOTE = '"',
            CODEPAGE = '65001'
        );
        ''')

        conexion.commit()
        print("Extracción completada con éxito.")
    except Exception as e:
        print(f"Error al extraer la información en el archivo: {e}")
    finally:
        cursor.close()


def clean_and_load_data(conexion):
    try:
        cursor = conexion.cursor()

        # Limpiar datos
        cursor.execute("""
        UPDATE TempData
        SET
            FirstName = REPLACE(FirstName, ';', ''),
            LastName = REPLACE(LastName, ';', ''),
            Gender = REPLACE(Gender, ';', ''),
            Nationality = REPLACE(Nationality, ';', ''),
            AirportName = REPLACE(AirportName, ';', ''),
            AirportCountryCode = REPLACE(AirportCountryCode, ';', ''),
            CountryName = REPLACE(CountryName, ';', ''),
            AirportContinent = REPLACE(AirportContinent, ';', ''),
            Continents = REPLACE(Continents, ';', ''),
            DepartureDate = REPLACE(DepartureDate, ';', ''),
            ArrivalAirport = REPLACE(ArrivalAirport, ';', ''),
            PilotName = REPLACE(PilotName, ';', ''),
            FlightStatus = REPLACE(FlightStatus, ';', '');
        """)

        # Convertir fechas a formato YYYY-MM-DD
        cursor.execute("""
        UPDATE TempData
        SET DepartureDate = CASE
            WHEN TRY_CONVERT(DATE, DepartureDate, 101) IS NOT NULL THEN FORMAT(TRY_CONVERT(DATE, DepartureDate, 101), 'yyyy-MM-dd')
            ELSE NULL
        END;
        """)

        # Reemplazar valores nulos
        cursor.execute("""
        UPDATE TempData
        SET FirstName = ISNULL(FirstName, 'Unknown'),
            LastName = ISNULL(LastName, 'Unknown'),
            Gender = ISNULL(Gender, 'Unknown'),
            Age = ISNULL(Age, 0),
            Nationality = ISNULL(Nationality, 'Unknown'),
            AirportName = ISNULL(AirportName, 'Unknown'),
            AirportCountryCode = ISNULL(AirportCountryCode, 'Unknown'),
            CountryName = ISNULL(CountryName, 'Unknown'),
            AirportContinent = ISNULL(AirportContinent, 'Unknown'),
            Continents = ISNULL(Continents, 'Unknown'),
            DepartureDate = ISNULL(DepartureDate, '1900-01-01'),
            ArrivalAirport = ISNULL(ArrivalAirport, 'Unknown'),
            PilotName = ISNULL(PilotName, 'Unknown'),
            FlightStatus = ISNULL(FlightStatus, 'Unknown');
        """)

        # Eliminar filas duplicadas
        cursor.execute("""
        WITH CTE AS (
            SELECT *,
                   ROW_NUMBER() OVER (PARTITION BY PassengerID ORDER BY (SELECT NULL)) AS rn
            FROM TempData
        )
        DELETE FROM CTE
        WHERE rn > 1;
        """)

        

        # Insertar datos en las tablas de dimensiones
        cursor.execute("""
        INSERT INTO Pasajero (Identificacion, Nombre, Apellido, Sexo, Edad, Nacionalidad)
        SELECT DISTINCT PassengerID, FirstName, LastName, Gender, Age, Nationality
        FROM TempData;
        """)

        cursor.execute("""
        INSERT INTO Aeropuerto (Nombre, Codigo_aeropuerto, Pais, Continente_aeropuerto)
        SELECT DISTINCT AirportName, AirportCountryCode, CountryName, AirportContinent
        FROM TempData;
        """)

        cursor.execute("""
        INSERT INTO Piloto (Nombre)
        SELECT DISTINCT PilotName
        FROM TempData;
        """)

        # Insertar datos en la tabla hechos_vuelo
        cursor.execute("""
        INSERT INTO Vuelo (Estado, Fecha, Id_pasajero, Id_aeropuerto)
        SELECT 
            DISTINCT td.FlightStatus AS Estado, td.DepartureDate AS Fecha,
            p.Id_pasajero,
            a.Id_aeropuerto
        FROM TempData td
        LEFT JOIN Pasajero p ON p.Identificacion = td.PassengerID
        LEFT JOIN Aeropuerto a ON a.Nombre = td.AirportName;
        """)

        conexion.commit()
        print("Datos cargados y limpiados con éxito.")
    except Exception as e:
        print(f"Error al cargar y limpiar los datos: {e}")
    finally:
        cursor.close()
