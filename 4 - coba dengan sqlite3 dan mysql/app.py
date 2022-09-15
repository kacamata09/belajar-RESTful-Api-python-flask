from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_cors import CORS

aplikasiku = Flask(__name__)
apiku = Api(aplikasiku)
CORS(aplikasiku)

# database
# aplikasiku.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/cobarestful'
aplikasiku.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbcobarestful.db'
dbku = SQLAlchemy(aplikasiku)

class Mahasiswa(dbku.Model):
    nim = dbku.Column(dbku.String(12), primary_key=True)
    nama = dbku.Column(dbku.String(100), nullable=False)
    jurusan = dbku.Column(dbku.String(50))
    ipk = dbku.Column(dbku.Integer)
    
    def __repr__(self) -> str:
        return f'<{self.nama}>'
    
    def save(self):
        try:
            dbku.session.add(self)
            dbku.session.commit()
            return True
        except:
            return False


class IniResource(Resource):
    def get(self):
        dataMahasiswa = Mahasiswa.query.all()
        tampilkan = [{
          'nim': data.nim,
          'nama': data.nama,
          'jurusan': data.jurusan,
          'ipk': data.ipk 
        } for data in dataMahasiswa
                     ]
        return tampilkan
    
    def post(self):
        nim = request.form['nim']
        nama = request.form['nama']
        jurusan = request.form['jurusan']
        ipk = float(request.form['ipk'])
        mahasiswaBaru = Mahasiswa(nim=nim, nama=nama, jurusan=jurusan, ipk=ipk)
        mahasiswaBaru.save()
        
        return ['alhamdulillah masuk bro']
    
    # hapus semua
    def delete(self):
        # 'untuk menghapus semua data'
        # mahasiswa = Mahasiswa.query.all()
        # for data in mahasiswa:
        #     # hapusmahasiswa = Mahasiswa.query.get(data.nim)
        #     dbku.session.delete(data)
        #     dbku.session.commit()

        'hapus berdasarkan nim'    
        nim = request.form['nim']
        try:
            hapusData = Mahasiswa.query.get_or_404(nim)
            dbku.session.delete(hapusData)
            dbku.session.commit()
            return {'msg': f'data dengan nim{nim} berhasil dihapus'}
        except:
            return {'msg error':f'kemungkinan nim yang anda masukkan tidak ada'}
        # dbku.session.flush()
        # return {'msg':'berhasil dihapus semua mungkin bro'}
        
    def put(self):
        'ubah data'
        nim = request.form['nim']
        try:
            editData = Mahasiswa.query.get_or_404(nim)
            # nama = request.form['nama']
            # jurusan = request.form['jurusan']
            # ipk = request.form['ipk']
            editData.nama = request.form['nama']
            editData.jurusan = request.form['jurusan']
            editData.ipk = float(request.form['ipk'])
            dbku.session.commit()
            return {'msg':f' data dengan nim {nim} berhasil di edit'}
        except:
            return {'msg error':'ada yang salah bro pada database, mungkin {nim} yang anda masukkan tidak ada'}


apiku.add_resource(IniResource, '/apiku', methods=['GET', 'POST', 'DELETE', 'PUT'])

if __name__ == '__main__':
    aplikasiku.run(debug=True)