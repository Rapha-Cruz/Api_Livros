from flask import Flask, request, jsonify, Blueprint
from conexao import criar_conexao, fechar_conexao
from utils.auth import token_required  # Importar o middleware

livros_bp = Blueprint('livros', __name__)

#lista todos os livros do banco
@livros_bp.route('/listar', methods=['GET'])
def listar_livros():
    #conectar com o banco de dados
    conn = criar_conexao()    
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM LIVROS")
    livros = cursor.fetchall()

    #fechar conexão com banco de dados
    cursor.close()
    fechar_conexao(conn)

    return jsonify(livros)

#criar um livro novo
@livros_bp.route('/novolivro', methods=['POST'])
def criar_livro():
    data = request.json
    TITULO = data['TITULO']
    AUTOR = data['AUTOR']
    GENERO = data['GENERO']
    ANO_PUBLICACAO = data['ANO_PUBLICACAO']
    ID_EDITORA = data['ID_EDITORA']

    #conectar com o banco
    conn = criar_conexao()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO LIVROS (titulo, autor, genero, ano_publicacao, id_editora)"
                   "VALUES (%s, %s, %s, %s, %s)",
                   (TITULO, AUTOR, GENERO, ANO_PUBLICACAO, ID_EDITORA))
    conn.commit()

    #fechar a conexao com o banco de dados
    cursor.close()
    fechar_conexao(conn)

    return jsonify({"mensagem": "Livro criado com sucesso"})

#atualizar um livro pelo ID
@livros_bp.route('/<int:id>', methods=['PUT'])
def atualizar_livro(id):
    dados = request.get_json()
    titulo = dados['titulo']
    autor = dados['autor']
    genero = dados['genero']
    ano_publicacao = dados['ano_publicacao']
    id_editora = dados['id_editora']

    conn = criar_conexao()
    cursor = conn.cursor(dictionary=True)

    sql = "UPDATE livros SET titulo = %s, autor = %s, genero = %s, ano_publicacao = %s, id_editora = %s WHERE id_livro = %s"
    valores = (titulo, autor, genero, ano_publicacao, id_editora, id)

    cursor.execute(sql, valores)
    conn.commit()

    cursor.close()
    fechar_conexao(conn)

    return jsonify({"mensagem": "Livro atualizado com sucesso"}), 200

#deletar livros
@livros_bp.route('/<int:id_livro>', methods=['DELETE'])
def deletar_livro(id_livro):
    conn = criar_conexao()
    cursor = conn.cursor()

    sql = "DELETE FROM livros WHERE id_livro = %s"
    valores = (id_livro, )

    try :
        cursor.execute(sql, valores)
        conn.commit()
        return jsonify({"mensagem":"Livro deletado"}), 200
    
    except Exception as err:
        conn.rollback()
        return jsonify({"erro": f"Erro ao deletar o livro: {err}"}), 500

    finally: 
        cursor.close()
        fechar_conexao(conn)
