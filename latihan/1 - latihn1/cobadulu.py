# import library yang dibutuhkan
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

# inisiasi app ke menjadi object flask
app = Flask(__name__)

# config database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dblatihan.db'
dbku = SQLAlchemy(app)

     
# buat orm class model untuk database   
class Pegawai(dbku.Model):
    id = dbku.Column(dbku.Integer, primary_key=True)
    nama = dbku.Column(dbku.String(50), nullable=False)
    jabatan = dbku.Column(dbku.String(100))
    

@app.route('/restapi', methods=['POST', 'GET', 'PUT', 'DELETE'])
def apiku():    
    if request.method == 'POST':
        'ini adalah fungsi post'
        nama = request.form['nama']
        jabatan = request.form['jabatan']
        tambahPegawai = Pegawai(nama=nama, jabatan=jabatan)
        dbku.session.add(tambahPegawai)
        dbku.session.commit()
        return {'pesan': 'data anda berhasil disimpan'}
    
    if request.method =='PUT':
        'ini adalah fungsi put atau edit data pada rest api'
        id = request.form['id']
        try:
            pegawai = Pegawai.query.get_or_404(id)
            pegawai.nama = request.form.get('nama')
            pegawai.jabatan = request.form.get('jabatan')
            dbku.session.commit()
            return {'pesan':'berhasil edit bro'}
        except:
            return {'pesan': f'tampaknya ada kesalahan bro, kemungkinan sih id {id} gak ada'}

    if request.method == 'DELETE':
        'ini adalah fungsi hapus data'
        id = request.form['id']
        try:
            pegawai = Pegawai.query.get_or_404(id)
            dbku.session.delete(pegawai)
            dbku.session.commit()
            return {'pesan':f'data dengan id {id} dan nama {pegawai.nama} berhasil dihapus'}
        except:
            return {'pesan': f'ada yang salah bro, kemungkinan id {id} yang anda masukkan tidak ada'}
            
    'ini adalah fungsi get data'
    pegawai = Pegawai.query.all()
    datapegawai = [{
        'id': data.id,
        'nama': data.nama,
        'jabatan': data.jabatan
    } for data in pegawai
    ]
    return {'pesan':'ini datanya bro', 'Data Pegawai': datapegawai}

    


if __name__ == '__main__':
    app.run(debug=True)