from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
crsf = CSRFProtect(app)
bcrypt = Bcrypt(app)

from views_servisos import *
from views_clientes import *

if __name__ == '__main__':
    app.run(debug=True)
