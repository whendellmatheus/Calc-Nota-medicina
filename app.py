from flask import Flask, render_template, request, redirect, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "medpondera_secret_key"  # chave usada para a sessão

# função para conectar no banco de dados
def get_db():
    return sqlite3.connect("database.db")

# cria a tabela de usuários caso ainda não exista
def init_db():
    con = get_db()
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    con.commit()
    con.close()

# inicia o banco quando o programa roda
init_db()

# rota de login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        senha = request.form["senha"]
        
        con = get_db()
        cur = con.cursor()
        # aqui verifica se o usuário e a senha existem
        cur.execute("SELECT username FROM usuarios WHERE username=? AND senha=?", (username, senha))
        result = cur.fetchone()
        con.close()
        
        if result:
            session["username"] = username  # salva o login
            return redirect("/calculadora")
        else:
            flash("Login ou senha incorretos!")
            return redirect("/")
            
    return render_template("login.html")

# rota para criar conta
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        senha = request.form["senha"]
        try:
            con = get_db()
            cur = con.cursor()
            # salva o novo usuário
            cur.execute("INSERT INTO usuarios (username, senha) VALUES (?, ?)", (username, senha))
            con.commit()
            con.close()
            flash("Conta criada! Agora faça login.")
            return redirect("/")
        except sqlite3.IntegrityError:
            flash("Esse nome de usuário já existe!")
            return redirect("/register")
            
    return render_template("register.html")

# rota para sair da conta
@app.route("/logout", methods=["POST"])
def logout():
    session.clear()  # limpa a sessão
    return redirect("/")

# rota da calculadora
@app.route("/calculadora", methods=["GET", "POST"])
def calculadora():
    if "username" not in session:  # verifica se o usuário está logado
        return redirect("/")

    # pega o período, padrão é 1
    try:
        periodo = int(request.args.get("periodo", 1))
    except ValueError:
        periodo = 1
    
    # limite máximo é 9
    if periodo > 9:
        periodo = 9

    disciplina = request.args.get("disciplina", "mulher")
    etapa = request.args.get("etapa", "av1") 

    media_final = None
    notas_salvas = {}
    componentes = []
    ciclo = ""
    formula_explicacao = "" 
    erro_msg = None 

    # define os componentes dependendo do período
    if periodo <= 4:
        ciclo = "Ciclo Básico"
        formula_explicacao = "soma normal com pesos"
        componentes = [
            {"key": "tbl_f",   "label": "TBL - Formativa",     "peso": 0.08},
            {"key": "tbl_s",   "label": "TBL - Somativa",      "peso": 0.32},
            {"key": "lmf_f",   "label": "LMF - Formativa",     "peso": 0.09},
            {"key": "lmf_s",   "label": "LMF - Somativa",      "peso": 0.21},
            {"key": "tutor_f", "label": "Tutoria - Formativa", "peso": 0.15},
            {"key": "tutor_s", "label": "Tutoria - Somativa",  "peso": 0.15},
        ]

    # componentes do ciclo clínico
    elif 5 <= periodo <= 9:
        ciclo = "Ciclo Clínico"
        
        if disciplina in ["mulher", "crianca"]:
            titulo = "Saúde da Mulher" if disciplina == "mulher" else "Saúde da Criança"
            formula_explicacao = f"{titulo}: 60% cognitivo + 40% prático"
            componentes = [
                {"key": "tbl_f", "label": "TBL Formativa (Cognitivo)", "peso": "20% (do Cog)"},
                {"key": "tbl_s", "label": "TBL Somativa (Cognitivo)",  "peso": "80% (do Cog)"},
                {"key": "sim_f", "label": "Simulação Formativa",       "peso": "40% (da Prat)"},
                {"key": "sim_s", "label": "Simulação Somativa",        "peso": "60% (da Prat)"},
            ]
        
        elif disciplina == "amb":
            if etapa == "av1":
                formula_explicacao = "AV1: 30% formativa + 70% somativa"
                componentes = [
                    {"key": "amb_f", "label": "AMB - Formativa", "peso": 0.3},
                    {"key": "amb_s", "label": "AMB - Somativa",  "peso": 0.7},
                ]
            else:
                formula_explicacao = "AV2: 30% form + 30% som + 40% osce"
                componentes = [
                    {"key": "amb_f",    "label": "AMB - Formativa",     "peso": 0.3},
                    {"key": "amb_s",    "label": "AMB - Somativa",      "peso": 0.3},
                    {"key": "amb_osce", "label": "AMB - Projeto/OSCE",  "peso": 0.4},
                ]

        elif disciplina == "iasc":
            formula_explicacao = "IASC: 25% form + 50% som + 25% projeto"
            componentes = [
                {"key": "iasc_f", "label": "IASC - Formativa",      "peso": 0.25},
                {"key": "iasc_s", "label": "IASC - Somativa",       "peso": 0.50},
                {"key": "iasc_p", "label": "IASC - Projeto/OSCE",   "peso": 0.25},
            ]

    # cálculo das notas
    if request.method == "POST":
        try:
            # função para pegar cada nota
            def get_nota(key):
                val_str = request.form.get(key, "").strip().replace(",", ".")
                notas_salvas[key] = val_str  # salva o valor digitado
                
                if not val_str: 
                    raise KeyError  # campo vazio
                
                val = float(val_str)
                
                # valida a nota entre 0 e 10
                if val < 0.0 or val > 10.0:
                    raise ValueError("Nota fora do limite")
                
                return val

            media = 0.0

            # cálculo do ciclo básico
            if periodo <= 4:
                for item in componentes:
                    media += get_nota(item["key"]) * float(item["peso"])

            # cálculo do ciclo clínico
            elif 5 <= periodo <= 9:

                if disciplina in ["mulher", "crianca"]:
                    tbl_f, tbl_s = get_nota("tbl_f"), get_nota("tbl_s")
                    sim_f, sim_s = get_nota("sim_f"), get_nota("sim_s")
                    
                    cognitivo = (tbl_f * 0.2) + (tbl_s * 0.8)
                    pratico   = (sim_f * 0.4) + (sim_s * 0.6)
                    media = (0.6 * cognitivo) + (0.4 * pratico)

                elif disciplina == "amb":
                    f, s = get_nota("amb_f"), get_nota("amb_s")
                    if etapa == "av1":
                        media = (0.3 * f) + (0.7 * s)
                    else:
                        osce = get_nota("amb_osce")
                        media = (0.3 * f) + (0.3 * s) + (0.4 * osce)

                elif disciplina == "iasc":
                    f, s, p = get_nota("iasc_f"), get_nota("iasc_s"), get_nota("iasc_p")
                    media = (0.25 * f) + (0.5 * s) + (0.25 * p)

            media_final = round(media, 2)

        except ValueError as e:
            if str(e) == "Nota fora do limite":
                erro_msg = "As notas devem ser entre 0.0 e 10.0"
            else:
                erro_msg = "Erro: digite somente números."
            media_final = None
            
        except KeyError:
            erro_msg = "Preencha todos os campos."
            media_final = None

    # retorna tudo para o html
    return render_template(
        "calculadora.html",
        periodo=periodo,
        ciclo=ciclo,
        disciplina=disciplina,
        etapa=etapa,
        formula_explicacao=formula_explicacao,
        componentes=componentes,
        media=media_final,
        erro_msg=erro_msg,
        notas_salvas=notas_salvas,
        username=session.get("username")
    )

if __name__ == "__main__":
    app.run(debug=True)
