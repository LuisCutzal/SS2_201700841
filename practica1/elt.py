import pyodbc

def extract_information(file_path, conexion):
    try:
        cursor = conexion.cursor()
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

        # Usar una ruta absoluta para el archivo CSV
        cursor.execute(f'''
        BULK INSERT TempData
        FROM '{file_path}'
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
            FirstName = REPLACE(REPLACE(REPLACE(FirstName, ';', ''), '"', ''), '''', ''),
            LastName = REPLACE(REPLACE(REPLACE(LastName, ';', ''), '"', ''), '''', ''),
            Gender = REPLACE(REPLACE(REPLACE(Gender, ';', ''), '"', ''), '''', ''),
            Nationality = REPLACE(REPLACE(REPLACE(Nationality, ';', ''), '"', ''), '''', ''),
            AirportName = REPLACE(REPLACE(REPLACE(AirportName, ';', ''), '"', ''), '''', ''),
            AirportCountryCode = REPLACE(REPLACE(REPLACE(AirportCountryCode, ';', ''), '"', ''), '''', ''),
            CountryName = REPLACE(REPLACE(REPLACE(CountryName, ';', ''), '"', ''), '''', ''),
            AirportContinent = REPLACE(REPLACE(REPLACE(AirportContinent, ';', ''), '"', ''), '''', ''),
            Continents = REPLACE(REPLACE(REPLACE(Continents, ';', ''), '"', ''), '''', ''),
            DepartureDate = REPLACE(REPLACE(REPLACE(DepartureDate, ';', ''), '"', ''), '''', ''),
            ArrivalAirport = REPLACE(REPLACE(REPLACE(ArrivalAirport, ';', ''), '"', ''), '''', ''),
            PilotName = REPLACE(REPLACE(REPLACE(PilotName, ';', ''), '"', ''), '''', ''),
            FlightStatus = REPLACE(REPLACE(REPLACE(FlightStatus, ';', ''), '"', ''), '''', '');
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

        # Insertar datos en la tabla Fecha
        cursor.execute("""
        INSERT INTO Fecha (Year, Month, Day)
        SELECT DISTINCT 
            YEAR(TRY_CONVERT(DATE, DepartureDate, 101)) AS Year,
            MONTH(TRY_CONVERT(DATE, DepartureDate, 101)) AS Month,
            DAY(TRY_CONVERT(DATE, DepartureDate, 101)) AS Day
        FROM TempData
        WHERE TRY_CONVERT(DATE, DepartureDate, 101) IS NOT NULL;
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
        INSERT INTO Vuelo (Estado, Id_pasajero, Id_aeropuerto, Id_piloto, Id_fecha)
        SELECT 
            DISTINCT td.FlightStatus AS Estado,
            (SELECT Id_pasajero FROM Pasajero WHERE identificacion = td.PassengerID) AS Id_pasajero,
            (SELECT Id_aeropuerto FROM Aeropuerto WHERE Nombre = td.ArrivalAirport) AS Id_aeropuerto,
            (SELECT Id_piloto FROM Piloto WHERE Nombre = td.PilotName) AS Id_piloto,
            (SELECT Id_fecha FROM Fecha 
            WHERE year = YEAR(TRY_CONVERT(DATE, td.DepartureDate, 101))
            AND month = MONTH(TRY_CONVERT(DATE, td.DepartureDate, 101))
            AND day = DAY(TRY_CONVERT(DATE, td.DepartureDate, 101))) AS Id_fecha
        FROM TempData td;
        """)

        conexion.commit()
        print("Datos cargados y limpiados con éxito.")
    except Exception as e:
        print(f"Error al cargar y limpiar los datos: {e}")
    finally:
        cursor.close()
