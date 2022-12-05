from flask import render_template, request, redirect, url_for
from jogoteca import app, db
from models import PrestadorServico
from helpers import FormularioPrestadorServico
from flask_bcrypt import generate_password_hash


@app.route('/novo_prestador')
def novoPrestador():
    form = FormularioPrestadorServico()
    return render_template('novoPrestador.html', titulo='Novo Prestador', form=form)


@app.route('/criar_prestador', methods=['POST', 'GET'])
def criarPrestador():
    form = FormularioPrestadorServico(request.form)

    cnpj = form.cnpj.data
    nome = form.nome.data
    telefone = form.telefone.data
    email = form.email.data
    localidade = form.localidade.data
    senha = generate_password_hash(form.senha.data).decode('utf-8')

    prestador = PrestadorServico(cnpj=cnpj, nome=nome,
                                 telefone=telefone, email=email, localidade=localidade, senha=senha)

    db.session.add(prestador)
    db.session.commit()
    return redirect(url_for('listarServisos'))


@app.route('/editar-prestador/<string:email>')
def editarPrestador(email):
    prestador = PrestadorServico.query.filter_by(email=email).first()
    form = FormularioPrestadorServico()

    form.cnpj.data = prestador.cnpj
    form.nome.data = prestador.nome
    form.data.data = prestador.data
    form.telefone.data = prestador.telefone
    form.email.data = prestador.email
    form.localidade.data = prestador.localicade

    return render_template('editarPrestador.html', titulo='Editar Infos',
                           email=email, form=form)


@app.route('/atualizar-prestador', methods=['POST'])
def atualizarPrestador():
    form = FormularioPrestadorServico(request.form)
    if form.validate_on_submit():
        prestador = PrestadorServico.query.filter_by(email=request.form['email']).first()
        prestador.cpf = form.cnpj.data
        prestador.nome = form.nome.data
        prestador.data = form.data.data
        prestador.telefone = form.telefone.data
        prestador.email = form.email.data
        prestador.localicade = form.localidade.data
        prestador.senha = generate_password_hash(form.senha.data).decode('utf-8')

        db.session.add(prestador)
        db.session.commit()

    return redirect(url_for('listarServisos'))
