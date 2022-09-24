from flask import Flask, request, jsonify, make_response
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sangat rahasia'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///belajarrest.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/belajarrest'
apiku = Api(app)
dbku = SQLAlchemy(app)

class Pengguna(dbku.Model):
    __tablename__ = 'flask-pengguna'
    username = dbku.Column(dbku.String(50), primary_key=True)
    password_hash = dbku.Column(dbku.String(255))
    
    @property
    def password(self):
        raise AttributeError('Maaf bro gak boleh liat passwordnya')
    
    @password.setter
    def set_password(self, password_hash):
        self.password_hash = generate_password_hash(password_hash, 'sha256')
    
    def cek_password(self, password_hash):
        return check_password_hash(self.password_hash, password_hash)
    
    

class Register(Resource):
    def post(self):
        username = request.form.get('username').lower()
        password = request.form.get('password')
        password_hashing = generate_password_hash(password, 'sha256')
        if not username or not password:
            return jsonify({'pesan':'belum ada bro username atau passwordnya'})
        penggunaBaru = Pengguna(username = username, password_hash = password_hashing)
        getPengguna = Pengguna.query.filter_by(username=username).first()
        if getPengguna == None:
            try:
                dbku.session.add(penggunaBaru)
                dbku.session.commit()
            except:
                return jsonify({'pesan':'kemungkinan ada yang salah pada database'})
        elif getPengguna != None:
            return jsonify({'pesan':'sudah ada username yang sama disini, silahkan cari username baru'})
        return jsonify({'pesan':f'selamat anda telah berhasil register, saudara/saudari {username}. silahkan login untuk mendapatkan token'})
    
class Login(Resource):
        def post(self):
            username = request.form.get('username').lower()
            # print(username)
            password = request.form.get('password')
            try:
                getPengguna = Pengguna.query.get_or_404(username)
            except:
                # getPengguna = Pengguna.query.get_or_404(username)
                return jsonify({'pesan':'username yang anda masukkan nggk ada bro'})
            # if getPengguna.cek_password(password):
            if getPengguna.password_hash == password:
                return jsonify({'pesan':'anda berhasil login'})
            return jsonify({'pesan':'coba lagi'})

apiku.add_resource(Register, '/api/register/', methods=['POST'])
# apiku.add_resource(Login, '/api/login/', methods=['POST'])
apiku.add_resource(Login, '/api/login/', methods=['POST'])


if __name__ == '__main__':
    app.run(debug=True)
    # dbku.create_all()