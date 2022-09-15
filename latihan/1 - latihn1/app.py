# import library yang dibutuhkan
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_cors import CORS

# inisiasi app ke menjadi object flask
app = Flask(__name__)

# config database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dblatihan.db'
dbku = SQLAlchemy(app)

# inisiasi variable api
apiku = Api(app)
CORS(app)

     
# buat orm class model untuk database   
class Pegawai(dbku.Model):
    id = dbku.Column(dbku.Integer, primary_key=True)
    nama = dbku.Column(dbku.String(50), nullable=False)
    jabatan = dbku.Column(dbku.String(100))
    
# buat class resource
class IniResource(Resource):
    def get(self):
        'ini adalah fungsi get data'
        pegawai = Pegawai.query.all()
        datapegawai = [{
            'id': data.id,
            'nama': data.nama,
            'jabatan': data.jabatan
        } for data in pegawai
        ]
        return {'pesan':'ini datanya bro', 'Data Pegawai': datapegawai}
        
        
    def post(self):
        'ini adalah fungsi post'
        nama = request.form['nama']
        jabatan = request.form['jabatan']
        tambahPegawai = Pegawai(nama=nama, jabatan=jabatan)
        dbku.session.add(tambahPegawai)
        dbku.session.commit()
        return {'pesan': 'data anda berhasil disimpan'}
    
    def put(self):
        'ini adalah fungsi put atau edit data pada rest api'
        id = request.form['id']
        try:
            pegawai = Pegawai.query.get_or_404(id)
            pegawai.nama = request.form['nama']
            pegawai.jabatan = request.form['jabatan']
            dbku.session.commit()
            return {'pesan':'berhasil edit bro'}
        except:
            return {'pesan': f'tampaknya ada kesalahan bro, kemungkinan sih id {id} gak ada'}
        
    def delete(self):
        'ini adalah fungsi hapus data'
        id = request.form['id']
        try:
            pegawai = Pegawai.query.get_or_404(id)
            dbku.session.delete(pegawai)
            dbku.session.commit()
            return {'pesan':f'data dengan id {id} dan nama {pegawai.nama} berhasil dihapus'}
        except:
            return {'pesan': f'ada yang salah bro, kemungkinan id {id} yang anda masukkan tidak ada'}
    
apiku.add_resource(IniResource, '/restapi', methods=['POST', 'GET', 'PUT', 'DELETE'])

if __name__ == '__main__':
    app.run(debug=True)