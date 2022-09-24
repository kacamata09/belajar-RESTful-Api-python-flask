from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
# from datetime import datetime, timedelta
import jwt
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ini adalah secret key yang terkuat'
apiku = Api(app)

# buat decorator untuk kunci akses
def pakai_token(func):
    def kunci(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'pesan':'belum ada tokennya bro'})
        try:
            dekodetoken = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256']) 
        except:
            return jsonify({'pesan':'kemungkinan tokennya salah bro and sis'})
        return func(*args, **kwargs)
    return kunci

class BuatToken(Resource):
    def post(self):
        username = request.form.get('username')
        if username:
            # token tanpa kadaluarsa
            token = jwt.encode({'username':username}, app.config['SECRET_KEY'], algorithm='HS256')
            return jsonify({'token':token,
                            'pesan':f'silahkan copy tokennya ya {username}'})
        else:
            return jsonify({'pesan':'username belum ada bro'})

class Dashboard(Resource):
    @pakai_token
    def get(self):
        return jsonify({'pesan':'berhasil masuk berkat token'})
    
class About(Resource):
    def get(self):
        return jsonify({'pesan':'area bebas akses'})


apiku.add_resource(BuatToken, '/api/login/', methods=['POST'])
apiku.add_resource(Dashboard, '/api/dashboard/', methods=['GET'])
apiku.add_resource(About, '/bebas/', methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)
    