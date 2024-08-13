# controllers/controlador.py
from config.configBD import get_connection
import json

def get_clientes():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Cambia la consulta a la tabla 'clientes'
    query = 'SELECT * FROM clientes'
    cursor.execute(query)

    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    
    results = [dict(zip(columns, row)) for row in rows]
    
    conn.close()
    return results

def get_cliente(identificacion):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Cambia la consulta a la tabla 'clientes'
    query = 'SELECT * FROM clientes WHERE identificacion ='+identificacion
    cursor.execute(query)

    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    
    results = [dict(zip(columns, row)) for row in rows]
    
    conn.close()
    return results


def insert_cliente(identificacion, nombres, apellidos, tipoIdentificacion, fechaNacimiento, numeroCelular, correoElectronico):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Verificar si la identificación ya existe
    check_query = 'SELECT COUNT(*) FROM clientes WHERE identificacion = ?'
    cursor.execute(check_query, (identificacion,))
    exists = cursor.fetchone()[0]
    
    if exists > 0:
        conn.close()
        return {'code': 500, 'msg': 'La identificación ya existe'}

    insert_query = '''
        INSERT INTO clientes (identificacion, nombres, apellidos, tipoIdentificacion, fechaNacimiento, numeroCelular, correoElectronico)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    '''
    values = (identificacion, nombres, apellidos, tipoIdentificacion, fechaNacimiento, numeroCelular, correoElectronico)
    
    cursor.execute(insert_query, values)
    conn.commit()
    
    conn.close()
    return {'code': 200, 'msg': 'Registro exitoso'}

def update_cliente(identificacion, nombres, apellidos, tipoIdentificacion, fechaNacimiento, numeroCelular, correoElectronico):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Verificar si la identificación existe
    check_query = 'SELECT COUNT(*) FROM clientes WHERE identificacion = ?'
    cursor.execute(check_query, (identificacion,))
    exists = cursor.fetchone()[0]
    
    if exists == 0:
        conn.close()
        return {'code': 500, 'msg': 'La identificación no existe'}

    update_query = '''
        UPDATE clientes
        SET nombres = ?, apellidos = ?, tipoIdentificacion = ?, fechaNacimiento = ?, numeroCelular = ?, correoElectronico = ?
        WHERE identificacion = ?
    '''
    values = (nombres, apellidos, tipoIdentificacion, fechaNacimiento, numeroCelular, correoElectronico, identificacion)
    
    cursor.execute(update_query, values)
    conn.commit()
    
    conn.close()
    return {'code': 200, 'msg': 'Actualización exitosa'}

def delete_cliente(identificacion):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Verificar si la identificación existe
    check_query = 'SELECT COUNT(*) FROM clientes WHERE identificacion = ?'
    cursor.execute(check_query, (identificacion,))
    exists = cursor.fetchone()[0]
    
    if exists == 0:
        conn.close()
        return {'code': 500, 'msg': 'La identificación no existe'}

    # Eliminar el cliente
    delete_query = 'DELETE FROM clientes WHERE identificacion = ?'
    cursor.execute(delete_query, (identificacion,))
    conn.commit()
    
    conn.close()
    return {'code': 200, 'msg': 'Eliminación exitosa'}