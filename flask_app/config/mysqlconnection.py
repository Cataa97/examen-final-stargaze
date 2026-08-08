import os
import pymysql.cursors
from dotenv import load_dotenv

load_dotenv()

class MySQLConnection:
    def __init__(self, db):
        host = os.environ.get('MYSQLHOST') or os.environ.get('DB_HOST') or 'localhost'
        port = int(os.environ.get('MYSQLPORT') or os.environ.get('DB_PORT') or 3306)
        user = os.environ.get('MYSQLUSER') or os.environ.get('DB_USER') or 'root'
        password = os.environ.get('MYSQLPASSWORD') or os.environ.get('DB_PASSWORD') or ''

        print(f"Intentando conexion a MySQL en Host: {host}, Port: {port}, User: {user}")

        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            db=db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        self.connection = connection

    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("query", query)
                cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    result = cursor.fetchall()
                    return result
                else:
                    self.connection.commit()
            except Exception as e:
                print("error:", e)
                return False
            finally:
                self.connection.close()

def connectToMySQL(db):
    return MySQLConnection(db)