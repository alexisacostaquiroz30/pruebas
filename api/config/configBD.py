import pyodbc

def get_connection():
    conn_str = (
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=ALEXIS;'  
        r'DATABASE=bdPruebaCelsia;'
        r'Trusted_Connection=yes;'
    )
    return pyodbc.connect(conn_str)
