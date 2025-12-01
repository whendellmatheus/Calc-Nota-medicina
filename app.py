from flask import Flask, render_template, request, redirect, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "troque_esta_chave_para_uma_mais_secreta"

# abre conexão com banco
def get_db():
    return sqlite3.connect("database.db")


# LOGIN
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
            flash("Login inválido!")
            return redirect("/")

    return render_template("login.html")


# CADASTRO
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        senha = request.form["senha"]

        try:
            con = get_db()
            cur = con.cursor()
            cur.execute("INSERT INTO usuarios (username, senha) VALUES (?, ?)",
                        (username, senha))
            con.commit()
            con.close()

            flash("Conta criada com sucesso!")
            return redirect("/")

        except sqlite3.IntegrityError:
            flash("Usuário já existe!")
            return redirect("/register")

    return render_template("register.html")


# CALCULADORA
@app.route("/calculadora", methods=["GET", "POST"])
def calculadora():
    if "username" not in session:
        return redirect("/")

    periodo = request.args.get("periodo", 1)
    periodo = int(periodo)

    media_final = None
    notas_salvas = {}

    # ciclo básico
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

    # ciclo clínico
    else:
        componentes = {
            "nota_projeto": 0.50,
            "nota_pratica": 0.50
        }
        ciclo = "Ciclo Clínico"

    # cálculo
    if request.method == "POST":
        try:
            media = 0

            for nome_nota, peso in componentes.items():
                valor = request.form.get(nome_nota, "").strip()
                if valor == "":
                    raise KeyError("Campo vazio")

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


# LOGOUT
@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
