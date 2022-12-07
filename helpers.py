import os
from flask_wtf import FlaskForm
from Carhub import app
from wtforms import StringField, IntegerField, validators, SubmitField, PasswordField



class FormularioLogin(FlaskForm):
    email = StringField('Email', [validators.data_required(), validators.length(min=1, max=100)])
    senha = PasswordField('Senha', [validators.data_required(), validators.length(min=1, max=100)])
    login = SubmitField('Login')
class FormularioServico(FlaskForm):
    nome = StringField('Nome do serviço', [validators.data_required(), validators.length(min=1, max=50)])
    valor = IntegerField('Valor do serviço', [validators.data_required()])
    categoria = StringField('Categoria do serviço', [validators.data_required(), validators.length(min=1, max=50)])
    descricao = StringField('Descrição', [validators.data_required(), validators.length(min=1, max=250)])
    salvar = SubmitField('Salvar')


class FormularioPrestador(FlaskForm):
    cnpj = StringField('CNPJ', [validators.data_required(), validators.length(min=1, max=14)])
    nome = StringField('Nome Prestador', [validators.data_required(), validators.length(min=1, max=50)])
    telefone = StringField('Telefone', [validators.data_required(), validators.length(min=1, max=11)])
    email = StringField('Email', [validators.data_required(), validators.length(min=1, max=100)])
    localidade = StringField('Endereço', [validators.data_required(), validators.length(min=1, max=250)])
    senha = PasswordField('Senha', [validators.data_required(), validators.length(min=1, max=100)])
    login = SubmitField('Login')


class FormularioClientes(FlaskForm):
    cpf = StringField('CPF', [validators.data_required(), validators.length(min=1, max=11)])
    nome = StringField('Nome do Cliente', [validators.data_required(), validators.length(min=1, max=50)])
    data = StringField('Data', [validators.data_required(), validators.length(min=1, max=50)])
    telefone = StringField('Telefone', [validators.data_required(), validators.length(min=1, max=11)])
    email = StringField('Email', [validators.data_required(), validators.length(min=1, max=100)])
    endereco = StringField('Endereço', [validators.data_required(), validators.length(min=1, max=250)])
    senha = PasswordField('Senha', [validators.data_required(), validators.length(min=1, max=100)])
    salvar = SubmitField('Salvar')


def recupera_imagem(id=0):
    for nome_arquivo in os.listdir(app.config['UPLOADS_PAHT']):
        if f'logo{id}' in nome_arquivo:
            return nome_arquivo
    return 'capa_padrao.jpg'


def deleta_imagem(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'capa_padrao.jpg':
        os.remove(os.path.join(app.config['UPLOADS_PAHT'], arquivo))


