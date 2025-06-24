import pymysql

# Datos de base de datos remota
db_host = "bfg8xigctazr1joepgzb-mysql.services.clever-cloud.com"
db_user = "uirpd1wa5zkjpk90"
db_password = "ZLaLbvvqoYAeiSErCTeM"
db_name = "bfg8xigctazr1joepgzb"

# Conexión
connection = pymysql.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print("Versión de MySQL:", version)
finally:
    connection.close()