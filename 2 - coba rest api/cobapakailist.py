# test rest api

from flask import Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS

app = Flask(__name__)
apiku = Api(app)
# CORS(app)

# ini variabel kosong yang mau diisi
siswa = []

class ResourcePertama(Resource):
    def get(self):
        # response = {'pesan':'Hello World, ini restful pertamaku'}
        return siswa
    
    def post(self):
        nama_siswa = request.form["nama"]
        kelas_siswa = request.form["kelas"]
        siswa.append({
            "nama" : nama_siswa, 
            "kelas" : kelas_siswa
        })
        response_post = {'msg': f'Data {nama_siswa} dengan kelas {kelas_siswa} berhasil dimasukkan'}
        # response_post = siswa
        return response_post


# apiku.add_resource(ResourcePertama, '/apiku', methods=['GET', 'POST'])
apiku.add_resource(ResourcePertama, '/apiku', methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(debug=True)