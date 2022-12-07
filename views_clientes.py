from flask import render_template, request, redirect, session, flash, url_for
from Carhub import app, db
from models import Clientes, Prestador
from helpers import FormularioClientes,FormularioLogin
from flask_bcrypt import generate_password_hash


@app.route('/novo_cliente')
def novoCliente():
    form = FormularioClientes()
    return render_template('novoCliente.html', titulo='Novo Cliente', form=form)


@app.route('/criar_usuario', methods=['POST', 'GET'])
def criarUsuario():
    form = FormularioClientes(request.form)
    email = form.email.data
    cliente_email = Clientes.query.filter_by(email=email).first()
    prestador_email = Prestador.query.filter_by(email=email).first()
    if cliente_email or prestador_email:
        flash('Email já cadastrado')
        return redirect(url_for('novoCliente'))
    cpf = form.cpf.data
    nome = form.nome.data
    data = form.data.data
    telefone = form.telefone.data
    endereco = form.endereco.data
    senha = generate_password_hash(form.senha.data).decode('utf-8')

    cliente = Clientes(cpf=cpf, nome=nome, data=data,
                       telefone=telefone, email=email, endereco=endereco, senha=senha)

    db.session.add(cliente)
    db.session.commit()
    return redirect(url_for('listarServisos'))


@app.route('/editar-cliente')
def editarCliente():
    email = session['usuario_logado']
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

    return redirect(url_for('listarServisos'))

