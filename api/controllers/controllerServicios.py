# controllers/servicios_controlador.py
from config.configBD import get_connection
import json

def get_servicios():
    conn = get_connection()
    cursor = conn.cursor()
    
    query = 'SELECT * FROM servicios'
    cursor.execute(query)
    
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    
    # Convertir las filas en diccionarios con nombres de columnas
    results = [dict(zip(columns, row)) for row in rows]
    
    conn.close()
    return results

def get_servicio(identificacion,servicio):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Cambia la consulta a la tabla 'clientes'
    query = 'SELECT * FROM servicios WHERE identificacion ='+identificacion +' AND servicio = ' + servicio
    cursor.execute(query)

    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    
    results = [dict(zip(columns, row)) for row in rows]
    
    conn.close()
    return results


def insert_servicio(identificacion, servicio, fechaInicio, ultimaFacturacion, ultimoPago):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Verificar si el cliente existe
    check_cliente_query = 'SELECT COUNT(*) FROM clientes WHERE identificacion = ?'
    cursor.execute(check_cliente_query, (identificacion,))
    cliente_exists = cursor.fetchone()[0]
    
    if cliente_exists == 0:
        conn.close()
        return {'code': 500, 'msg': 'La identificación del cliente no existe'}

    # Insertar el nuevo servicio
    insert_query = '''
        INSERT INTO servicios (identificacion, servicio, fechaInicio, ultimaFacturacion, ultimoPago)
        VALUES (?, ?, ?, ?, ?)
    '''
    values = (identificacion, servicio, fechaInicio, ultimaFacturacion, ultimoPago)
    
    cursor.execute(insert_query, values)
    conn.commit()
    
    conn.close()
    return {'code': 200, 'msg': 'Registro exitoso'}

def update_servicio(identificacion, servicio, fechaInicio, ultimaFacturacion, ultimoPago):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Verificar si el servicio existe
    check_query = 'SELECT COUNT(*) FROM servicios WHERE identificacion = ? AND servicio = ?'
    cursor.execute(check_query, (identificacion, servicio))
    exists = cursor.fetchone()[0]
    
    if exists == 0:
        conn.close()
        return {'code': 500, 'msg': 'El servicio no existe'}

    # Actualizar el servicio
    update_query = '''
        UPDATE servicios
        SET fechaInicio = ?, ultimaFacturacion = ?, ultimoPago = ?
        WHERE identificacion = ? AND servicio = ?
    '''
    values = (fechaInicio, ultimaFacturacion, ultimoPago, identificacion, servicio)
    
    cursor.execute(update_query, values)
    conn.commit()
    
    conn.close()
    return {'code': 200, 'msg': 'Actualización exitosa'}

def delete_servicio(identificacion, servicio):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Verificar si el servicio existe
    check_query = 'SELECT COUNT(*) FROM servicios WHERE identificacion = ? AND servicio = ?'
    cursor.execute(check_query, (identificacion, servicio))
    exists = cursor.fetchone()[0]
    
    if exists == 0:
        conn.close()
        return {'code': 500, 'msg': 'El servicio no existe'}

    # Eliminar el servicio
    delete_query = 'DELETE FROM servicios WHERE identificacion = ? AND servicio = ?'
    cursor.execute(delete_query, (identificacion, servicio))
    conn.commit()
    
    conn.close()
    return {'code': 200, 'msg': 'Eliminación exitosa'}
