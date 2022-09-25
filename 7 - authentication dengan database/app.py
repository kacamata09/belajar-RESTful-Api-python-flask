from enum import unique
from flask import Flask, request, jsonify, make_response
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from flask_migrate import Migrate
from flask_login import UserMixin, current_user, login_required, \
    login_user, logout_user, LoginManager


from functools import wraps


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sangat rahasia'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///belajarrest.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/belajarrest'
apiku = Api(app)
dbku = SQLAlchemy(app)
migrasidb = Migrate(app, dbku)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'loginuser'

@login_manager.user_loader
def load_user(id):
    try:
        return Pengguna.query.get_or_404(int(id))
    except:
        return jsonify({'pesan':'anda gagal login'})

def token_required(fungsi):
    @wraps(fungsi)
    def kunci_halaman(*args, **kwargs):
        token = request.args.get('token')
        # token = request.args.get('token') # bisa juga menggunakan form
        if not token:
            return jsonify({'pesan':'maaf token belum anda masukkan, silahkan masukkan token untuk akses ini'})
        try:
            bukaToken = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return jsonify({'pesan':'maaf token anda tidak valid atau token anda udah habis masa berlakunya'})
        return fungsi(*args, **kwargs)
    return kunci_halaman

# buat kunci akses untuk halaman yang tidak didapat akses user biasa
def akses_admin(fungsi):
    @wraps(fungsi)
    def kunci_halaman(*args, **kwargs):
        username = request.form.get('username')
        try:
            getUser = Pengguna.query.get_or_404(username)
        except:
            return make_response(jsonify({'pesan':'anda belum memasukkan username atau anda belum mendaftar'}))
        if (getUser.hak_akses).lower() == 'admin':
            return fungsi(*args, **kwargs)
        elif str(getUser.hak_akses).lower() == 'user':
            return jsonify({'pesan':'maaf user tidak boleh masuk, coba hacker jika ingin masuk'})
        else:
            return jsonify({'pesan':'ada kesalahan'})
    return kunci_halaman


class Pengguna(dbku.Model, UserMixin):
    __tablename__ = 'flask-pengguna'
    id = dbku.Column(dbku.Integer, primary_key=True, nullable=False)
    username = dbku.Column(dbku.String(50), unique=True)
    password_hash = dbku.Column(dbku.String(255))
    hak_akses = dbku.Column(dbku.String(50), default='user')
    
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
        hak_akses = request.form.get('hak_akses').lower()
        password_hashing = generate_password_hash(password, 'sha256')
        if not username or not password:
            return jsonify({'pesan':'belum ada bro username atau passwordnya'})
        penggunaBaru = Pengguna(username = username, password_hash = password_hashing, hak_akses=hak_akses)
        getPengguna = Pengguna.query.filter_by(username=username).first()
        if getPengguna == None:
            try:
                dbku.session.add(penggunaBaru)
                dbku.session.commit()
            except:
                # dbku.session.add(penggunaBaru)
                # dbku.session.commit()
                return jsonify({'pesan':'kemungkinan ada yang salah pada database'})
        elif getPengguna != None:
            return jsonify({'pesan':'sudah ada username yang sama disini, silahkan cari username baru'})
        return jsonify({'pesan':f'selamat anda telah berhasil register, saudara / saudari {username}. silahkan login untuk mendapatkan token'})
    
class LoginUser(Resource):
        def post(self):
            # id = request.form.get('id')
            # print(username)
            username = request.form.get('username')
            password = request.form.get('password')
            try:
                # getPengguna = Pengguna.query.get_or_404(id)
                getPengguna = Pengguna.query.filter_by(username=username).first()
            except:
                return jsonify({'pesan':'username yang anda masukkan nggk ada bro'})
            if getPengguna.cek_password(password):
                login_user(getPengguna)
            # if getPengguna.password_hash == password:
                token = jwt.encode(
                    {'username': username, 'exp':datetime.utcnow() + timedelta(days=1)}, 
                    app.config['SECRET_KEY'],
                    algorithm='HS256')
                return jsonify({'pesan':'anda berhasil login, silahkan copy tokennya untuk authentikasi', 'token':token})
            return jsonify({'pesan':'coba lagi mungkin password anda salah'})
        
        def get(self):
            return make_response(jsonify({'pesan':'login dulu bro'}))
        
        def delete(self):
            semua_user = Pengguna.query.all()
            for user in semua_user:
                dbku.session.delete(user)
                dbku.session.commit()
            return jsonify({'pesan':'semua sudah terhapus'})

class Dashboard(Resource):
    @token_required
    # @login_required
    def get(self):
        return jsonify({'pesan':'anda berhasil masuk menggunakan token'})

class BebasArea(Resource):
    def get(self):
        return jsonify({'pesan':'ini adalah halaman bebas akses. Hacker juga boleh masuk'})
    
class HalamanAdmin(Resource):
    @login_required
    # @token_required
    # @akses_admin
    def get(self):
        return jsonify({'pesan':'selamat anda berhasil login berarti anda admin'})



apiku.add_resource(Register, '/api/register/', methods=['POST'])
apiku.add_resource(LoginUser, '/api/login/', methods=['POST', 'GET', 'DELETE'])
apiku.add_resource(Dashboard, '/api/dashboard/', methods=['GET', 'POST'])
apiku.add_resource(BebasArea, '/bebas/', methods=['GET'])
apiku.add_resource(HalamanAdmin, '/admin/', methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)
    # dbku.create_all()
    