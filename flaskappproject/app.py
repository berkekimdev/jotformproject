from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text  # text fonksiyonunu içe aktar

app = Flask(__name__)

# MySQL bağlantı ayarları
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://berkroot:xxxxxxxxxxxx@34.29.191.126/pythonflask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def index():
    try:
        # Ham SQL sorgusu kullanarak verileri çekme
        result = db.session.execute(text("SELECT * FROM people"))  # text fonksiyonu ile sorguyu sarma test aaaaaaaaa1aa262 test test2 test 3 4 6  10
        people = result.fetchall()
        print(people)  # Terminalde bu veriyi kontrol edin
        return render_template('people.html', people=people)
    except Exception as e:
        return f"Hata: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
