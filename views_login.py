from flask import render_template, request, redirect, session, flash, url_for
from flask_bcrypt import check_password_hash
from Carhub import app
from models import Clientes, Prestador
from helpers import FormularioLogin


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    if proxima is None:
        proxima = url_for('listarServisos')
    form = FormularioLogin()
    return render_template('login.html', proxima=proxima, form=form)


@app.route('/autenticar', methods=['POST'])
def autenticar():
    form = FormularioLogin(request.form)
    email = form.email.data
    cliente = Clientes.query.filter_by(email=email).first()
    senha = check_password_hash(cliente.senha, form.senha.data)
    if cliente is None:
        prestador = Prestador.query.filter_by(email=email).first()
        senhap = check_password_hash(prestador.senha, form.senha.data)
    if cliente and senha:
        session['usuario_logado'] = cliente.email
        session['prestador'] = False
        flash(f'{session["usuario_logado"]} Esta logado')
        proxima_pagina = request.form['proxima']
        if request.form['proxima'] is None:
            proxima_pagina = url_for('criar')
        return redirect(proxima_pagina)
    elif prestador and senhap:
        session['usuario_logado'] = cliente.email
        session['prestador'] = True
        flash(f'{session["usuario_logado"]} Esta logado')
        proxima_pagina = request.form['proxima']
        if request.form['proxima'] is None:
           proxima_pagina = url_for('criar')
        return redirect(proxima_pagina)
    else:
        flash('Não foi possivel logar senha ou usuario incorreto')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Volte sempre')
    return redirect(url_for('index'))
