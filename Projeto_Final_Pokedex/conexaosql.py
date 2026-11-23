import mysql.connector
from mysql.connector import Error

def criar_conexao():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="",
            database="pokedex_bd"
        )
        return conexao
    except Error as e:
        print(f"Falha na conexão: {e}")
        return None