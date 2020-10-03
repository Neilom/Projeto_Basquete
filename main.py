# -----> Importação das bibliotecas necessárias para desenvolver o aplicativo 
from PyQt5 import uic, QtWidgets
import sqlite3

# -----> Variável que fazem conexão com o banco de dados
connection = sqlite3.connect('temporada.db')

# -----> Cursor necessário para acessar o banco de dados
cursor = connection.cursor()
    
# -----> Função que permite adquirir a ultima linha do banco de dados e transfere ele para a variável "dados" em uma lista (array)
def consulta():
    dados = cursor.execute("SELECT * FROM dados")
    for row in cursor.fetchall():  # -> Função que interpreta em python um dado extraido de um banco de dados
        dados = row
    return dados

# -----> Função que faz a verificação lógica
def logica():
    dados = consulta() # -----> Uma lista com os últimos dados do banco de dados
    quebra_max = dados[5] 
    quebra_min = dados[4]
    jogo = dados[0]
    maximo_temporada = dados[3]
    minimo_temporada = dados[2]
    jogo += 1
    placar = int(interface.campo_placar.text())

    # -----> Verificar se o placar atual ultrapassou os valores de máximo ou mínimo da temporada e acrescenta 1 na respectiva ultrapassagem.
    if maximo_temporada < placar:
        quebra_max += 1
    elif minimo_temporada > placar:
       quebra_min += 1

    # -----> Verifica se o placar atual é o maior ou o menor da temporada e modifica-o conforme sua colocação
    if placar > maximo_temporada:
        maximo_temporada = placar  
    elif placar < minimo_temporada:
        minimo_temporada = placar  
    
    # -----> Chama o cursor do bancos de dados e executa a inserção dos dados no mesmo.
    cursor.execute("INSERT INTO dados (Jogo, placar, mintemp, maxtemp, quebramin, quebramax) VALUES(?,?,?,?,?,?)", (jogo, placar, minimo_temporada, maximo_temporada, quebra_min, quebra_max))
    connection.commit()
    
# -----> Função que seleciona todos os dados do banco de dado e imprimo os dados na janela do GUI (Interface Gráfica do Usuário / do inglês "Graphical User Interface")
def atualizarDados():
        query = "SELECT * FROM dados"
        result  = connection.execute(query)
        interface.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            interface.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                interface.table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

# -----> Definições da interface.
app = QtWidgets.QApplication([])
interface = uic.loadUi("main.ui")

# -----> Definição dos botões
interface.btn_placar.clicked.connect(logica)
interface.btn_placar.clicked.connect(atualizarDados)
interface.btn_atualizar.clicked.connect(atualizarDados)

# -----> Execução da interface 
interface.show()
app.exec()
