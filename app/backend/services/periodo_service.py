from config import with_db_connection

@with_db_connection
def get_all_periodos(cursor):
    cursor.execute('SELECT id_periodo, nombre_periodo, fecha_inicio, fecha_fin, activo FROM periodos_escolares ORDER BY fecha_inicio DESC')
    rows = cursor.fetchall()
    # Las fechas se devuelven como objetos date, el frontend las puede manejar.
    return [dict(row) for row in rows]

@with_db_connection
def get_periodo_by_id(cursor, id):
    cursor.execute('SELECT id_periodo, nombre_periodo, fecha_inicio, fecha_fin, activo FROM periodos_escolares WHERE id_periodo = %s', (id,))
    row = cursor.fetchone()
    return dict(row) if row else None

@with_db_connection
def create_periodo(cursor, data):
    sql = """
    INSERT INTO periodos_escolares (nombre_periodo, fecha_inicio, fecha_fin, activo)
    VALUES (%s, %s, %s, %s)
    RETURNING id_periodo;
    """
    cursor.execute(sql, (data['nombre_periodo'], data['fecha_inicio'], data['fecha_fin'], data.get('activo', False)))
    periodo_id = cursor.fetchone()['id_periodo']
    return {'id_periodo': periodo_id, **data}

@with_db_connection
def update_periodo(cursor, id, data):
    sql = """
    UPDATE periodos_escolares
    SET nombre_periodo = %s, fecha_inicio = %s, fecha_fin = %s, activo = %s
    WHERE id_periodo = %s
    """
    cursor.execute(sql, (data['nombre_periodo'], data['fecha_inicio'], data['fecha_fin'], data.get('activo', False), id))
    return cursor.rowcount > 0

@with_db_connection
def delete_periodo(cursor, id):
    cursor.execute('DELETE FROM periodos_escolares WHERE id_periodo = %s', (id,))
    return cursor.rowcount > 0
