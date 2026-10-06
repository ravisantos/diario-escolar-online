from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

@app.route('/')
def inicio():
    return 'Diário Escolar funcionando!'

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

