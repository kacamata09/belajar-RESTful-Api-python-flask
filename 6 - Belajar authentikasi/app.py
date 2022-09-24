from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from datetime import datetime, timedelta
import jwt
from functools import wraps

app = Flask(__name__)
apiku = Api(app)

app.config['SECRET_KEY'] = 'hacker jangan menyerang'

# buat dekorator cek token untuk authentikasi
def cek_token(f):
    @wraps(f)
    def kunci(*args, **kwargs):
        'token akan diparsing melalui parameter di endpoint'
        token = request.args.get('token')
        # token = request.form.get('token')
        if not token:
            return make_response(jsonify({'pesan':'tokennya belum ada'}), 404)
        try:
            hasil = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return make_response(jsonify({'pesan':'tokennya salah'}), 404)
        return f(*args, **kwargs)
    return kunci

class Login(Resource):
    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'root' and password == 'superpassword':
            
            token = jwt.encode({
                'username': username,
                'password': password, 
                'exp':datetime.utcnow() + timedelta(minutes=5)
                }, app.config['SECRET_KEY'], algorithm='HS256'
                               )
        return jsonify({'token':token, 'pesan':'Berhasil login, silahkan ambil tokennya'})
    
class Dashboard(Resource):
    @cek_token
    def get(self):
        return jsonify({'pesan':'berhasil login dengan token'})
    
class BisaAkses(Resource):
    def get(self):
        return jsonify({'pesan':'siapapun bisa akses'})

apiku.add_resource(Login, '/api/login', methods=['POST'])
apiku.add_resource(Dashboard, '/api/dashboard', methods=['GET'])
apiku.add_resource(BisaAkses, '/api/bisa', methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)