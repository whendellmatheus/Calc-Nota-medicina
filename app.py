from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "troque_esta_chave_para_uma_mais_secreta"


# conexão com sqlite
def get_db():
    return sqlite3.connect("database.db")


# login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        senha = request.form["senha"]

        con = get_db()
        cur = con.cursor()
        cur.execute("SELECT username FROM usuarios WHERE username=? AND senha=?", (username, senha))
        result = cur.fetchone()
        con.close()

        if result:
            session["username"] = username
            return redirect("/calculadora")
        else:
            return "Login inválido!"

    return render_template("login.html")

# calculadora
@app.route("/calculadora", methods=["GET", "POST"])
def calculadora():
    # pega período do select ou padrão = 1
    periodo = request.args.get("periodo")
    if periodo is None:
        periodo = 1
    periodo = int(periodo)

    media_final = None
    notas_salvas = {}

    # pesos do ciclo básico
    if periodo <= 4:
        componentes = {
            "tbl_f": 0.08,
            "tbl_s": 0.32,
            "lmf_f": 0.09,
            "lmf_s": 0.21,
            "tutor_f": 0.15,
            "tutor_s": 0.15
        }
        ciclo = "Ciclo Básico"

    # pesos do ciclo clínico
    else:
        componentes = {
            "nota_projeto": 0.50,
            "nota_pratica": 0.50
        }
        ciclo = "Ciclo Clínico"

    # cálculo de média
    if request.method == "POST":
        try:
            media = 0
            for nome_nota, peso in componentes.items():
                valor = request.form.get(nome_nota, "").strip()
                if valor == "":
                    raise KeyError("vazio")
                nota = float(valor)
                notas_salvas[nome_nota] = valor
                media += nota * peso

            media_final = media

        except:
            media_final = "Erro: preencha todos os campos com números."

    return render_template(
        "calculadora.html",
        periodo=periodo,
        ciclo=ciclo,
        componentes=componentes,
        media=media_final,
        notas_salvas=notas_salvas,
        username=session.get("username")
    )


#Rota de Logout
@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/")




if __name__ == "__main__":
    app.run(debug=True)
