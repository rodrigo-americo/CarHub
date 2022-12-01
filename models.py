from jogoteca import db


class Servisos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    valor = db.Column(db.Integer, nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    descricao = db.Column(db.String(250))

    def __repr__(self):
        return '<Name %r>' % self.name


class Clientes(db.Model):
    cpf = db.Column(db.String(11), nullable=True)
    nome = db.Column(db.String(50), nullable=True)
    data = db.Column(db.String(50), primary_key=True)
    telefone = db.Column(db.String(11), nullable=True)
    email = db.Column(db.String(100), primary_key=True,  nullable=True)
    endereco = db.Column(db.String(250), nullable=True)
    senha = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return '<Name %r>' % self.name


class PrestadorServico(db.Model):
    cnpj = db.Column(db.String(14), nullable=True)
    nome = db.Column(db.String(50), nullable=True)
    telefone = db.Column(db.String(11), nullable=True)
    email = db.Column(db.String(100), primary_key=True,  nullable=True)
    localidade = db.Column(db.String(250), nullable=True)
    senha = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return '<Name %r>' % self.name