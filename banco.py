import sqlite3
import os

db_name = "database.db"


if os.path.exists(db_name):
    os.remove(db_name)
    print(f"Arquivo antigo '{db_name}' deletado.")


con = sqlite3.connect(db_name)
cur = con.cursor()

cur.execute("""
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
)
""")

try:
    
    cur.execute("INSERT INTO usuarios (username, senha) VALUES (?, ?)", 
                ('whendell', '123456'))
    print("Usuário 'whendell' criado com sucesso.")
except sqlite3.IntegrityError:
    print("Erro: Usuário já existe.")

con.commit()
con.close()

print("Novo banco de dados criado.")