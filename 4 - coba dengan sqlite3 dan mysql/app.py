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
        ipk = int(request.form['ipk'])
        mahasiswaBaru = Mahasiswa(nim=nim, nama=nama, jurusan=jurusan, ipk=ipk)
        mahasiswaBaru.save()
        
        return ['alhamdulillah masuk bro']
        


apiku.add_resource(IniResource, '/apiku', methods=['GET', 'POST'])

if __name__ == '__main__':
    aplikasiku.run(debug=True)