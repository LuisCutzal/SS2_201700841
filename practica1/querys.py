import pyodbc

def query1(conexion):
    """
    Debe mostrar un SELECT COUNT(*) de todas las tablas para ver que si realizo la carga en las tablas del modelo.
    """
    cursor = conexion.cursor()
    query="""
    SELECT COUNT(*) FROM Vuelo;
    SELECT COUNT(*) FROM Pasajero;
    SELECT COUNT(*) FROM Aeropuerto;
    SELECT COUNT(*) FROM Piloto;
    """
    cursor.execute(query)
    tablas =["Vuelo", "Pasajero", "Aeropuerto", "Piloto"]
    for tabla in tablas:
        row = cursor.fetchall()
        print(f"{tabla}: {row[0][0]}")
        cursor.nextset()
    cursor.close()
    
def query2(conexion):
    """
    Porcentaje de pasajeros por género
    """
    cursor = conexion.cursor()
    query = """
    SELECT 
        Sexo,
        COUNT(*) AS TotalPasajerosPorGenero,
        (COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Pasajero)) AS PorcentajePorGenero
    FROM 
        Pasajero
    GROUP BY 
        Sexo;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(f"Sexo: {row.Sexo}, TotalPasajerosPorGenero: {row.TotalPasajerosPorGenero}, PorcentajePorGenero: {row.PorcentajePorGenero:.2f}%")
    cursor.close()
    
def query3(conexion):
    """
    Nacionalidades con su mes año de mayor fecha de salida
    """
    cursor = conexion.cursor()
    query = """
    SELECT 
        Nacionalidad,
        FORMAT(Fecha, 'MM-yyyy') AS MonthYear,
        COUNT(*) AS CountPerMonth
    FROM 
        Pasajero p
    JOIN 
        Vuelo v ON p.Id_pasajero = v.Id_pasajero
    GROUP BY 
        Nacionalidad,
        FORMAT(Fecha, 'MM-yyyy')
    ORDER BY 
        Nacionalidad, 
        FORMAT(Fecha, 'MM-yyyy');
    """
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    results = {}
    months_years = set()
    for row in data:
        nacionalidad, month_year, count = row
        if nacionalidad not in results:
            results[nacionalidad] = {}
        results[nacionalidad][month_year] = count
        months_years.add(month_year)
    months_years = sorted(months_years)
    header = ['Nacionalidad'] + months_years
    print("\t".join(header))
    for nacionalidad, counts in results.items():
        row = [nacionalidad]
        for month_year in months_years:
            row.append(str(counts.get(month_year, 0)))
        print("\t".join(row))
        
def query4(conexion):
    """
    Count de vuelos por país
    """
    cursor = conexion.cursor()
    query="""
    SELECT 
        a.Pais AS Pais,
        COUNT(v.Id_vuelo) AS TotalVuelos
    FROM 
        Vuelo v
    JOIN 
        Aeropuerto a ON v.Id_aeropuerto = a.Id_aeropuerto
    GROUP BY 
        a.Pais
    ORDER BY 
        TotalVuelos DESC;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(f"Pais: {row.Pais}, TotalVuelos: {row.TotalVuelos}")
    cursor.close()
    
def query5(conexion):
    """
    Top 5 aeropuertos con mayor número de pasajeros
    """
    cursor = conexion.cursor()
    query="""
    SELECT TOP 5
        a.Nombre AS Aeropuerto,
        COUNT(v.Id_pasajero) AS TotalPasajeros
    FROM 
        Vuelo v
    JOIN 
        Aeropuerto a ON v.Id_aeropuerto = a.Id_aeropuerto
    GROUP BY 
        a.Nombre
    ORDER BY 
        TotalPasajeros DESC;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(f"Aeropuerto: {row.Aeropuerto}, TotalPasajeros: {row.TotalPasajeros}")
    cursor.close()
    
def query6(conexion):
    """Count divido por estado de vuelo
    
    """
    cursor = conexion.cursor()
    query="""
    SELECT 
        Estado AS EstadoVuelo,
        COUNT(*) AS TotalVuelos
    FROM 
        Vuelo
    GROUP BY 
        Estado
    ORDER BY 
        TotalVuelos DESC;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(f"Estado Vuelo: {row.EstadoVuelo}, Total Vuelo: {row.TotalVuelos}")
    cursor.close()
    
def query7(conexion):
    """
    Top 5 de los países más visitados.
    """
    cursor = conexion.cursor()
    query="""
    SELECT TOP 5
        a.Pais AS Pais,
        COUNT(v.Id_vuelo) AS TotalVuelos
    FROM 
        Vuelo v
    JOIN 
        Aeropuerto a ON v.Id_aeropuerto = a.Id_aeropuerto
    GROUP BY 
        a.Pais
    ORDER BY 
        TotalVuelos DESC;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(f"Pais: {row.Pais}, Total Vuelos: {row.TotalVuelos}")
    cursor.close()
    
def query8(conexion):
    """
    Top 5 de los continentes más visitados
    """
    cursor = conexion.cursor()
    query="""
    SELECT TOP 5
        a.Continente_aeropuerto AS Continente,
        COUNT(v.Id_vuelo) AS TotalVuelos
    FROM 
        Vuelo v
    JOIN 
        Aeropuerto a ON v.Id_aeropuerto = a.Id_aeropuerto
    GROUP BY 
        a.Continente_aeropuerto
    ORDER BY 
        TotalVuelos DESC;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(f"Continente: {row.Continente}, Total Vuelos: {row.TotalVuelos}")
    cursor.close()

def query9(conexion):
    """
    Top 5 de edades divido por género que más viajan
    """
    cursor = conexion.cursor()
    query = """
    WITH EdadGeneroVuelos AS (
        SELECT 
            p.Sexo AS Genero,
            p.Edad AS Edad,
            COUNT(v.Id_vuelo) AS TotalVuelos
        FROM 
            Pasajero p
        JOIN 
            Vuelo v ON p.Id_pasajero = v.Id_pasajero
        GROUP BY 
            p.Sexo, 
            p.Edad
    )
    SELECT TOP 5
        Genero,
        Edad,
        TotalVuelos
    FROM 
        EdadGeneroVuelos
    ORDER BY 
        TotalVuelos DESC;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(f"Género: {row.Genero}, Edad: {row.Edad}, Total Vuelos: {row.TotalVuelos}")
    cursor.close()
    
def query10(conexion):
    """
    Count de vuelos por MM-YYYY
    """
    cursor = conexion.cursor()
    query="""
    SELECT 
        FORMAT(Fecha, 'MM-yyyy') AS Month_Year,
        COUNT(*) AS TotalVuelos
    FROM 
        Vuelo
    GROUP BY 
        FORMAT(Fecha, 'MM-yyyy')
    ORDER BY 
        Month_Year;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(f"MM-YYYY: {row.Month_Year}, Total Vuelos: {row.TotalVuelos}")
    cursor.close()