from flask import render_template, request, redirect, session, flash, url_for
from flask_bcrypt import check_password_hash
from jogoteca import app, db
from models import Clientes
from helpers import FormularioClientes
from flask_bcrypt import generate_password_hash


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    if proxima is None:
        proxima = url_for('index')
    form = FormularioClientes()
    return render_template('login.html', proxima=proxima, form=form)


@app.route('/autenticar', methods=['POST'])
def autenticar():
    form = FormularioClientes(request.form)
    cliente = Clientes.query.filter_by(email=form.email.data).first()
    senha = check_password_hash(cliente.senha, form.senha.data)
    if cliente and senha:
        session['usuario_logado'] = cliente.email
        flash(f'{session["usuario_logado"]} Esta logado')
        proxima_pagina = request.form['proxima']
        if request.form['proxima'] is None:
            proxima_pagina = url_for('criar')
        return redirect(proxima_pagina)
    else:
        flash('Não foi possivel logar senha ou usuario incorreto')
        return redirect(url_for('login'))


@app.route('/novo_cliente')
def novoCliente():
    form = FormularioClientes()
    return render_template('novoCliente.html', titulo='Novo Cliente', form=form)


@app.route('/criar_usuario', methods=['POST', 'GET'])
def criarUsuario():
    form = FormularioClientes(request.form)

    cpf = form.cpf.data
    nome = form.nome.data
    data = form.data.data
    telefone = form.telefone.data
    email = form.email.data
    endereco = form.endereco.data
    senha = generate_password_hash(form.senha.data).decode('utf-8')

    cliente = Clientes(cpf=cpf, nome=nome, data=data,
                       telefone=telefone, email=email, endereco=endereco, senha=senha)

    db.session.add(cliente)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/editar-cliente/<string:email>')
def editarCliente(email):
    cliente = Clientes.query.filter_by(email=email).first()
    form = FormularioClientes()

    form.cpf.data = cliente.cpf
    form.nome.data = cliente.nome
    form.data.data = cliente.data
    form.telefone.data = cliente.telefone
    form.email.data = cliente.email
    form.endereco.data = cliente.endereco

    return render_template('editarCliente.html', titulo='Editar Infos',
                           email=email, form=form)

@app.route('/atualizar-cliente',methods=['POST'])
def atualizarCliente():
    form = FormularioClientes(request.form)
    if form.validate_on_submit():
        cliente = Clientes.query.filter_by(email=request.form['email']).first()
        cliente.cpf = form.cpf.data
        cliente.nome = form.nome.data
        cliente.data = form.data.data
        cliente.telefone = form.telefone.data
        cliente.email = form.email.data
        cliente.endereco = form.endereco.data
        cliente.senha = generate_password_hash(form.senha.data).decode('utf-8')

        db.session.add(cliente)
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Até um aprocima')
    return redirect(url_for('index'))


