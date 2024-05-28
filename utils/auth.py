#pip install PyJWT

import jwt
import datetime
from flask import request, jsonify
from functools import wraps

SECRET_KEY = 'chave_secreta'

def generate_token(username):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        'iat': datetime.datetime.utcnow(),
        'sub': username
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Verifica se o token está presente no header da requisição
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization'].split()
                        
            if auth_header[0] == 'Bearer':
                token = auth_header[1]
            else:
                return jsonify({'message': 'Formato de Token inválido!'}), 401

        if not token:
            return jsonify({'message': 'Token foi perdido!'}), 401

        try:
            # Decodifica o token (você precisa definir sua chave secreta e algoritmo)
            data = jwt.decode(token, "chave_secreta", algorithms=["HS256"])
            # Adicione outras verificações de token aqui, se necessário
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido!'}), 401

        return f(*args, **kwargs)
    
    return decorated