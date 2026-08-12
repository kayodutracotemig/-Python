import sqlite3

DB_NAME = "banco.db"


def conectar():
    """
    Abre uma conexão com o banco SQLite.
    row_factory = sqlite3.Row faz com que cada linha retornada
    se comporte como um dicionário (dá pra fazer linha["nome"]
    em vez de precisar lembrar a posição de cada coluna).
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def criar_tabelas():
    """
    Cria as tabelas 'usuarios' e 'tarefas' caso ainda não existam.
    IF NOT EXISTS evita erro se você rodar o app várias vezes.
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            status TEXT NOT NULL DEFAULT 'pendente',
            usuario_id INTEGER NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    """)

    conn.commit()
    conn.close()
