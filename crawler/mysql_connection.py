# 負責「Python 如何連進 MySQL」

import mysql.connector
# http://localhost:8080

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="1234",
        database="mydb"
    )