from flask import Flask
from datetime import date

app = Flask(__name__)

@app.route('/iniapiku')
def api():
    apipertama = {
        'sambutan' : 'Hello World!',
        'nama': 'ini api pertamaku, mana api mu',
        'tanggal': f'tanggal hari ini adalah tanggal {date.today()}' 
        }
    return apipertama, 


if __name__ == '__main__':
    app.run(debug=True)