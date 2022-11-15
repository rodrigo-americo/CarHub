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


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Até um aprocima')
    return redirect(url_for('index'))
