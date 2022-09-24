from flask import Flask, request, render_template
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
dbku = SQLAlchemy(app)

apiku = Api(app)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///barang.db'
app.config['SECRET_KEY'] = 'akuanakindonesiasehatdankuat,karenamamamemberiapa?'

barang = []

class Barang(Resource):
    def post(self):
        id = request.form['idbarang']
        nama = request.form['namabarang']
        harga = request.form['harga']
        barang.append({
            'id':id,
            'nama':nama,
            'harga':harga
        })
        return {'pesan':'sudah masuk'}
        
        

apiku.add_resource(Barang,  '/api', methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(debug=True)
        
