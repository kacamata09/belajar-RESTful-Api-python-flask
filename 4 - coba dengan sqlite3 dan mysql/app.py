from urllib import request
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_cors import CORS

aplikasiku = Flask(__name__)
apiku = Api(aplikasiku)
CORS(aplikasiku)

mahasiswa = {}

class IniResource(Resource):
    def get(self):
        return mahasiswa
    
    def post(self):
        nama = request.form['nama']
        ipk = int(request.form['ipk'])
        nim = request.form['nim']
        mahasiswa['nama'] = nama
        mahasiswa['ipk'] = ipk
        mahasiswa['nim'] = nim
        return ['alhamdulillah msuk bro']
        


apiku.add_resource(IniResource, '/apiku', methods=['GET', 'POST'])

aplikasiku.run(debug=True)