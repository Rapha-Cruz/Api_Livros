from flask import Flask, request, jsonify, Blueprint
from conexao import criar_conexao, fechar_conexao
from hashlib import sha256
from utils.auth import generate_token, token_required

usuarios_bp = Blueprint('usuarios', __name__)

#criar um usuario novo
@usuarios_bp.route('/novousuario', methods=['POST'])
def criar_usuario():
    data = request.json
    NOME = data['NOME']
    EMAIL = data['EMAIL']
    SENHA = data['SENHA']

    #converte a senha em uma sequencia de bytes usando a codificação UTF-8
    #aplica o algoritmo de hash sha256 
    #aplica a conversao do hash para hexadecimal, para armazenar no banco de dados
    senhaCripto = sha256(SENHA.encode('utf-8')).hexdigest()

    #conectar com o banco
    conn = criar_conexao()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO USUARIOS (NOME, EMAIL, SENHA)"
                   "VALUES (%s, %s, %s)",
                   (NOME, EMAIL, senhaCripto))
    conn.commit()

    #fechar a conexao com o banco de dados
    cursor.close()
    fechar_conexao(conn)

    return jsonify({"mensagem": "Usuário criado com sucesso"}), 200


# logar
@usuarios_bp.route('/login', methods=['POST'])
def login_usuario():
    data = request.json
    EMAIL = data['EMAIL']
    SENHA = data['SENHA']

    #conectar com o banco
    conn = criar_conexao()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT SENHA, NOME FROM USUARIOS WHERE EMAIL=%s",
                   (EMAIL,))
    senhaBanco = cursor.fetchone()
   
    if checar_senha(senhaBanco['SENHA'], SENHA):
        #fechar a conexao com o banco de dados
        cursor.close()
        fechar_conexao(conn)

        token = generate_token(senhaBanco['NOME'])
        return jsonify({'token': token, 'Nome': senhaBanco['NOME'] })
    
        #return jsonify({"token": token}), 200
    else :
        #fechar a conexao com o banco de dados
        cursor.close()
        fechar_conexao(conn)
        return jsonify({"mensagem": "Login Incorreto"}), 200
    
# Função para verificar a senha
def checar_senha(senhaBanco, senha):
    senha_convertida = sha256(senha.encode('utf-8')).hexdigest()
    return senhaBanco == senha_convertida