import os
import pymysql.cursors
from dotenv import load_dotenv

load_dotenv()
# --- DEBUG TEMPORAL ---
print("DEBUG DB_HOST =", repr(os.environ.get('DB_HOST')))
print("DEBUG DB_PORT =", repr(os.environ.get('DB_PORT')))
print("DEBUG DB_USER =", repr(os.environ.get('DB_USER')))
# -----------------------

class MySQLConnection:
    def __init__(self, db):
        connection = pymysql.connect(
            host=os.environ.get('DB_HOST'),
            port=int(os.environ.get('DB_PORT', 3306)),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
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
                print("Ejecutando Query:", query)
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
                print("error", e)
                return False
            finally:
                self.connection.close()

def connectToMySQL(db):
    return MySQLConnection(db)