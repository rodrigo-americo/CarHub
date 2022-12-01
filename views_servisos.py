import os

from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import db, app
from models import Servisos

from helpers import recupera_imagem, deleta_imagem, FormularioServico
import time


@app.route('/')
def index():
    lista_imagens = os.listdir(app.config['UPLOADS_PAHT'])
    form = FormularioServico()
    lista_de_servisos = Servisos.query.order_by(Servisos.id)
    return render_template('lista.html', titulo='Servisos', lista_de_servisos=lista_de_servisos
                           , form=form, lista_imagens=lista_imagens)


@app.route('/novo')
def novo():

    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormularioServico()
    return render_template('novo.html', titulo='Novo servisos', form=form)


@app.route('/criar', methods=['POST', 'GET'])
def criar():
    form = FormularioServico(request.form)
    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    nome = form.nome.data
    valor = form.valor.data
    categoria = form.categoria.data
    descricao = form.descricao.data

    serviso_nome = Servisos.query.filter_by(nome=nome).first()
    if serviso_nome:
        flash('Serviso já existente')
        return redirect(url_for('criar'))

    serviso = Servisos(nome=nome, valor=valor, categoria=categoria, descricao=descricao)

    timestamp = time.time()
    arquivo = request.files['arquivo']

    arquivo.save(f'{app.config["UPLOADS_PAHT"]}/logo{serviso.id}-{timestamp}.jpg')
    db.session.add(serviso)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/editar/<int:id>')
def editar(id):
    capa_jogo = recupera_imagem(id)
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for(f'editar/{id}')))
    serviso = Servisos.query.filter_by(id=id).first()
    form = FormularioServico()
    form.nome.data = serviso.nome
    form.valor.data = serviso.valor
    form.categoria.data = serviso.categoria
    form.descricao.data = serviso.descricao
    return render_template('editar.html', titulo='Editar servisos', id=id, capa_jogo=capa_jogo, form=form)


@app.route('/atualizar', methods=['POST'])
def atualizar():
    form = FormularioServico(request.form)
    if form.validate_on_submit():

        serviso = Servisos.query.filter_by(id=request.form['id']).first()

        serviso.nome = form.nome.data
        serviso.valor = form.valor.data
        serviso.categoria = form.categoria.data
        serviso.descricao = form.descricao.data

        db.session.add(serviso)
        db.session.commit()
        deleta_imagem(serviso.id)
        timestamp = time.time()
        arquivo = request.files['arquivo']
        arquivo.save(f'{app.config["UPLOADS_PAHT"]}/logo{serviso.id}-{timestamp}.jpg')
    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):

    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))
    Servisos.query.filter_by(id=id).delete()
    db.session.commit()
    flash(f'Item {id} foi deletado')
    return redirect(url_for('index'))


@app.route('/resultado', methods=['POST'])
def resultado():
    form = FormularioServico()
    lista_de_servisos = Servisos.query.filter_by(categoria=request.form['busca'])
    return render_template('lista.html', titulo='Servisos', lista_de_servisos=lista_de_servisos, form=form)


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

@app.route('/detalhe/<int:id>')
def detalhe(id):
    capa_jogo = recupera_imagem(id)
    serviso = Servisos.query.filter_by(id=id).first()
    form = FormularioServico()
    form.nome.data = serviso.nome
    form.valor.data = serviso.valor
    form.categoria.data = serviso.categoria
    form.descricao.data = serviso.descricao
    return render_template('detalhe.html', form=form, capa_jogo=capa_jogo)
