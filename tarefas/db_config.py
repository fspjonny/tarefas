import os
import sqlite3
from sqlite3 import Error
import time


# Caso o diretório do banco não existir, será criado.
db_dir = os.path.join(os.path.dirname(__file__), 'db')
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

# Caminho usado para armazenar e ler o banco de dados. Pasta 'db' e dentro o arquivo 'dados.db'
caminho = os.path.join(os.path.dirname(__file__), 'db', 'dados.db')

def create_db():
    try:
        '''
        Se não existir 'dados.db', dentro de 'db', ele será criado nesse momento.
        Se já existir, será aberto e lido.
        '''
        connection = sqlite3.connect(caminho)
        return {"connected": connection}
    
    except Error as err:
        '''
        Qualquer problema para criar ou se conectar ao banco, levanta uma exceção.
        O erro pode ser impresso ou retornado como uma mensagem de alerta.
        '''
        return {"error message": f"Erro ao criar ou se conectar ao banco de dados: {err}"}


# Executor que query's
def execute_query(query: str, params=None, fetch=False):
    connect = create_db()
    
    # Verifica se houve erro na conexão
    if "error message" in connect:
        return connect  # Se houve erro, retorna a mensagem
    
    connection = connect["connected"]  # Corrigido: agora obtemos a conexão correta
    try:
        with connection:
            cursor = connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Se fetch for True, retorna os resultados (para consultas SELECT)
            if fetch:
                result = cursor.fetchall()
                return result  # Retorna os resultados da query
            
            connection.commit()
        return {"message": "Query executada com sucesso"}

    except Error as e:
        return {"message": f"Erro ao executar a query: {e}"}
    finally:
        connection.close()


# Criando tabela
create_table_query = f'''
CREATE TABLE IF NOT EXISTS tarefas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    date TEXT,
    status INTEGER DEFAULT 0
);
'''
execute_query(create_table_query)


# Métodos C.R.U.D.

def create(title: str):
    query = "INSERT INTO tarefas (title, date, status) VALUES (?, ?, ?)"
    execute_query(query, (title, time.strftime('%d/%m/%Y'), 0))


def read():
    query = "SELECT * FROM tarefas"
    resultado = execute_query(query, fetch=True)
    return resultado


def update(id: int, title: str = None):
    current_data = execute_query("SELECT title FROM tarefas WHERE id = ?", (id,), fetch=True)
    
    if not current_data:
        return {"message": "Registro não encontrado"}
    
    # Extrair os valores atuais
    current_title = current_data[0]

    # Substituir valores não fornecidos pelos valores atuais
    title = title if title is not None else current_title

    # Atualizar a tabela com os novos valores (ou os valores antigos, se não forem alterados)
    query = "UPDATE tarefas SET title = ? WHERE id = ?"
    execute_query(query, (title, id))
    return {"message": "Registro atualizado com sucesso"}


def delete(id: int):
    query = "DELETE FROM tarefas WHERE id = ?"
    execute_query(query, (id,))
    return {"message": "Registro excluído com sucesso"}


def status(id: int, value: int):
    query = "UPDATE tarefas SET status = ? WHERE id = ?"
    execute_query(query, (value, id))
    return {"message": "Status atualizado com sucesso"}


def read_active():
    query = "SELECT COUNT(*) FROM tarefas WHERE status == 0"
    resultado = execute_query(query, fetch=True)
    return resultado[0][0]

def read_deactive():
    query = "SELECT COUNT(*) FROM tarefas WHERE status == 1"
    resultado = execute_query(query, fetch=True)
    return resultado[0][0]
