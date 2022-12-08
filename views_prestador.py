from flask import render_template, request, redirect, url_for, flash, session
from Carhub import app, db
from models import Prestador, Clientes
from helpers import FormularioPrestador
from flask_bcrypt import generate_password_hash


@app.route('/novo_prestador')
def novoPrestador():
    form = FormularioPrestador()
    return render_template('novoPrestador.html', titulo='Novo Prestador', form=form)


@app.route('/criar_prestador', methods=['POST', 'GET'])
def criarPrestador():
    form = FormularioPrestador(request.form)
    prestador_email = Prestador.query.filter_by(email=form.email.data).first()
    cliente_email = Clientes.query.filter_by(email=form.email.data).first()
    if prestador_email or cliente_email:
        flash('Email já cadastrado')
        return redirect(url_for('novoPrestador'))
    cnpj = form.cnpj.data
    nome = form.nome.data
    telefone = form.telefone.data
    email = form.email.data
    localidade = form.localidade.data
    senha = generate_password_hash(form.senha.data).decode('utf-8')

    prestador = Prestador(cnpj=cnpj, nome=nome,
                                 telefone=telefone, email=email, localidade=localidade, senha=senha)

    db.session.add(prestador)
    db.session.commit()
    return redirect(url_for('listarServisos'))


@app.route('/editar-prestador')
def editarPrestador():
    email = session['usuario_logado']
    print(email)
    prestador = Prestador.query.filter_by(email=email).first()
    form = FormularioPrestador()

    form.cnpj.data = prestador.cnpj
    form.nome.data = prestador.nome
    form.telefone.data = prestador.telefone
    form.email.data = prestador.email
    form.localidade.data = prestador.localidade
    return render_template('editarPrestador.html', titulo='Editar Infos',
                           email=email, form=form)


@app.route('/atualizar-prestador', methods=['POST'])
def atualizarPrestador():
    form = FormularioPrestador(request.form)
    if form.validate_on_submit():
        prestador = Prestador.query.filter_by(email=request.form['email']).first()
        prestador.cnpj = form.cnpj.data
        prestador.nome = form.nome.data
        prestador.data = form.data.data
        prestador.telefone = form.telefone.data
        prestador.email = form.email.data
        prestador.localicade = form.localidade.data
        prestador.senha = generate_password_hash(form.senha.data).decode('utf-8')

        db.session.add(prestador)
        db.session.commit()

    return redirect(url_for('listarServisos'))