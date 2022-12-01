import os
SECRET_KEY = 'rodrigo'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD='mysql+mysqlconnector',
        usuario='root',
        senha='admin',
        servidor='localhost',
        database='Carhub'
    )

UPLOADS_PAHT = os.path.dirname(os.path.abspath(__file__)) +'/uploads'
