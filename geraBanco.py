import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash
from pprint import pprint
print("Conectando...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='admin'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `Carhub`;")

cursor.execute("CREATE DATABASE `Carhub`;")

cursor.execute("USE `Carhub`;")

# criando tabelas
TABLES = {}
TABLES['Servisos'] = ('''
      CREATE TABLE `Servisos` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) NOT NULL,
      `valor` int NOT NULL,
      `email` varchar(100) NOT NULL,
      `categoria` varchar(40) NOT NULL,
      `descricao` varchar(250),
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Clientes'] = ('''
      CREATE TABLE `Clientes` (
      `cpf` varchar(11) NOT NULL,
      `nome` varchar(50) NOT NULL,
      `data` varchar(50) NOT NULL,
      `telefone` varchar(11) NOT NULL,
      `email` varchar(100) NOT NULL,
      `endereco` varchar(250) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`email`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Prestador'] = ('''
      CREATE TABLE `Prestador` (
      `cnpj` varchar(14) NOT NULL,
      `nome` varchar(50) NOT NULL,
      `telefone` varchar(11) NOT NULL,
      `email` varchar(100) NOT NULL,
      `localidade` varchar(250) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`email`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')



for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')

# inserindo Clientes
cliente_sql = 'INSERT INTO clientes (cpf, nome, data, telefone, email, endereco, senha)' \
              ' VALUES (%s, %s, %s,%s,%s,%s,%s)'
cliente = [
      ("99999999956", "Rodrigo", "11/05/1998 ", "11964802626",
       "rodrigo_7_4_7@hotmail.com", "Rua do retiro 2251", generate_password_hash("123").decode("utf-8")),
      ("99999889956", "Diego", "11/05/1998 ", "11970867253",
       "oliver.diegoramos@hotmail.com", "pass ", generate_password_hash("123").decode("utf-8"))
]

cursor.executemany(cliente_sql, cliente)

cursor.execute('select * from Carhub.clientes')
print(' -------------  cliente:  -------------')
for cliente in cursor.fetchall():
    pprint(cliente)


# inserindo Prestadores de serviço
prestadores_sql = 'INSERT INTO Prestador (cnpj, nome, telefone, email, localidade, senha)' \
                  ' VALUES (%s, %s, %s,%s,%s,%s)'
prestadores = [
      ("99999999999999", "Cleber", "11970867253",
       "cleber@hotmail.com", " Henrique Felipe da Costa, 682 - Vila Guilherme",
       generate_password_hash("1234").decode("utf-8")),
      ("99999999999946", "Hubens", "11970867253",
       "hubens@hotmail.com", " Henrique Felipe da Costa, 682 - Vila Guilherme", generate_password_hash("1234").decode("utf-8"))
]
cursor.executemany(prestadores_sql, prestadores)

cursor.execute('select * from Carhub.Prestador')
print(' -------------  Prestador:  -------------')
for user in cursor.fetchall():
    pprint(user)



# inserindo Serviços
Servisos_sql = 'INSERT INTO Servisos (nome, valor,email, categoria,descricao) VALUES (%s, %s ,%s, %s,%s)'
Servisos = [
      ('Jogo de peneu', '50', 'hubens@hotmail.com', 'Troca', 'Troca os quatros peneus do caro'),
      ('Troca de Ólio', '15', 'cleber@hotmail.com', 'Troca', 'Troca de Ólio'),
      ('Alinhamento do peneu', '24', 'hubens@hotmail.com', 'Revisao', 'Alinha os penus da frente e de tras para não tenha desvio quando virar'),
      ('Limpeza do interior', '123', 'cleber@hotmail.comm', 'Qualidade', 'Passa aspirador por todo o carro e coloca sache de pinho'),
      ('Troca de pastilha de freio', '645', 'hubens@hotmail.com', 'Troca', 'Troca a pastilha de freio'),
      ('Instalar insufilme', '879', 'hubens@hotmail.com', 'Instalacao', 'Instala insulvilme com o numero que o cliente pedir'),
]
cursor.executemany(Servisos_sql, Servisos)

cursor.execute('select * from Carhub.Servisos')
print(' -------------  Produtos:  -------------')
for servisos in cursor.fetchall():
   pprint(servisos)

# commitando se não nada tem efeito
conn.commit()
cursor.close()
conn.close()
