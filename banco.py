import sqlite3

con = sqlite3.connect("database.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE usuarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    senha TEXT,
)
""")
# EXEMPLOS DE USUÁRIOS
cur.execute("INSERT INTO usuarios (username, senha, periodo) VALUES ('joao', '123', 3)")
cur.execute("INSERT INTO usuarios (username, senha, periodo) VALUES ('maria', 'abc', 7)")

con.commit()
con.close()

print("Banco criado com sucesso.")