from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS

app = Flask(__name__)
apiku = Api(app)
CORS(app)

    
barang = []

class AkuResource(Resource):
    def post(self):
        'fungsi post'
        kodeBrg = request.form['kodeBrg']
        nama = request.form['namaBrg']
        stok = request.form['stokBrg']
        barang.append({
            'kodeBarang': kodeBrg,
            'namabarang': nama,
            'stokBarang': int(stok)
        })
        return jsonify({'pesan':'sudah berhasil bro, code 200',
                'baramg': barang,
                'cek':'perubahannya',
                'a jsonify':'mengurutkan dari a'})
    
    def get(self):
        'fungsi get'
        return jsonify({
            'pesan': 'Ini adalah get method',
            'barang': barang
        })
        
apiku.add_resource(AkuResource, '/', methods=['GET', 'POST', 'PUT', 'DELETE'])
        
if __name__ == '__main__':
    app.run(debug=True)