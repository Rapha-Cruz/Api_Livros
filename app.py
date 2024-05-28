from flask import Flask
from flask_cors import CORS
from rotas.rotas_livros import livros_bp
from rotas.rotas_usuarios import usuarios_bp
from rotas.rotas_auth import auth_bp  # Novo import para autenticação

app = Flask(__name__)
CORS(app)

app.register_blueprint(livros_bp, url_prefix='/livros')
app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
app.register_blueprint(auth_bp, url_prefix='/auth')  # Registrando o Blueprint de autenticação


#executar a API
if __name__  == "__main__":
     #app.run(port=8000, host='0.0.0.0')
     app.run()
     
