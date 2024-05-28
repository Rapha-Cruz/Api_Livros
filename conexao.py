#pip install mysql-connector-python
import mysql.connector

#configuração do banco de dados
def criar_conexao():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "admin",
        database = "biblioteca"
)
   
def fechar_conexao(conexao):
    if conexao:
        conexao.close()

