from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
apiku = Api(app)

app.config['SECRET_KEY'] = 'hacker kalau bisa jangan menyerang'

# buat decorator wajib_token

def wajib_token(f):
    @wraps(f)
    def kunci(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'pesan':'belum ada bro tokennya'})
        try:
            hasil = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return make_response(jsonify({'pesan':'salah bro tokennya atau udah kadaluarsa'}), 401)
        return f(*args, **kwargs)
    return kunci

class AmbilToken(Resource):
    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'root' and password == 'superpassword':
            tokenku = jwt.encode({
                'username':username,
                'password':password,
                'exp': datetime.utcnow() + timedelta(minutes=20)
            }, app.config['SECRET_KEY'], algorithm='HS256')
            return jsonify({'pesan':'selamat anda berhasil login, silahkan copy tokennya',
                            'token': tokenku})
        else:
            return jsonify({'pesan':'kemungkinan user atau passwordnya salah bro'})        

class Dashboard(Resource):
    @wajib_token
    def get(self):
        return jsonify({'pesan':'selamat bro tlah berhasil akses halaman ini menggunakan toker'})
    
class Bebas(Resource):
    def get(self):
        return {'pesan':'halaman ini dapat diakses siapapun'}

apiku.add_resource(AmbilToken, '/api/login/', methods=['POST'])
apiku.add_resource(Dashboard, '/api/dashboard/', methods=['GET'])
apiku.add_resource(Bebas, '/bebas/', methods=['GET'])
        
if __name__ == '__main__':
    app.run(debug=True)