from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import requests

from database import conectar, criar_tabelas

app = Flask(__name__)


app.config["SECRET_KEY"] = "troque-esta-chave-em-producao"


app.config["DEBUG"] = True



def usuario_logado():
    """Retorna o id do usuário logado (via session) ou None."""
    return session.get("usuario_id")


def login_obrigatorio(func):
    """
    Decorator: qualquer rota que usar @login_obrigatorio só executa
    se existir um usuario_id na sessão. Isso é o que o enunciado chama
    de 'proteger as rotas internas com sessão'.
    """
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not usuario_logado():
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    return wrapper



@app.route("/")
def index():
    return redirect(url_for("dashboard") if usuario_logado() else url_for("login"))


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        
        senha_hash = generate_password_hash(senha)

        conn = conectar()
        try:
            conn.execute(
                "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
                (nome, email, senha_hash),
            )
            conn.commit()
        except Exception:
            conn.close()
            return render_template("registro.html", erro="E-mail já cadastrado.")
        conn.close()

        return redirect(url_for("login"))

    return render_template("registro.html", erro=None)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        conn = conectar()
        usuario = conn.execute(
            "SELECT * FROM usuarios WHERE email = ?", (email,)
        ).fetchone()
        conn.close()

        if usuario and check_password_hash(usuario["senha"], senha):
            session["usuario_id"] = usuario["id"]
            session["usuario_nome"] = usuario["nome"]
            return redirect(url_for("dashboard"))

        return render_template("login.html", erro="E-mail ou senha inválidos.")

    return render_template("login.html", erro=None)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))



@app.route("/dashboard")
@login_obrigatorio
def dashboard():
    conn = conectar()
    tarefas = conn.execute(
        "SELECT * FROM tarefas WHERE usuario_id = ?", (usuario_logado(),)
    ).fetchall()
    conn.close()

    try:
        resposta = requests.get("https://api.adviceslip.com/advice", timeout=3)
        frase = resposta.json()["slip"]["advice"]
    except Exception:
        frase = "Não foi possível carregar a frase motivacional hoje."

    return render_template("dashboard.html", tarefas=tarefas, frase=frase)


@app.route("/api/tarefas")
@login_obrigatorio
def api_tarefas():
    """
    Rota que retorna as tarefas em JSON, filtradas por status.
    É consumida via fetch() no JavaScript do dashboard, para filtrar
    sem recarregar a página (item 8 do enunciado).
    """
    status = request.args.get("status", "todas")

    conn = conectar()
    if status == "todas":
        tarefas = conn.execute(
            "SELECT * FROM tarefas WHERE usuario_id = ?", (usuario_logado(),)
        ).fetchall()
    else:
        tarefas = conn.execute(
            "SELECT * FROM tarefas WHERE usuario_id = ? AND status = ?",
            (usuario_logado(), status),
        ).fetchall()
    conn.close()

    return jsonify([dict(t) for t in tarefas])


@app.route("/nova_tarefa", methods=["GET", "POST"])
@login_obrigatorio
def nova_tarefa():
    if request.method == "POST":
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        status = request.form["status"]

        conn = conectar()
        conn.execute(
            "INSERT INTO tarefas (titulo, descricao, status, usuario_id) VALUES (?, ?, ?, ?)",
            (titulo, descricao, status, usuario_logado()),
        )
        conn.commit()
        conn.close()

        return redirect(url_for("dashboard"))

    return render_template("nova_tarefa.html")


@app.route("/editar/<int:id>", methods=["GET", "POST"])
@login_obrigatorio
def editar(id):
    conn = conectar()

   
    tarefa = conn.execute(
        "SELECT * FROM tarefas WHERE id = ? AND usuario_id = ?",
        (id, usuario_logado()),
    ).fetchone()

    if tarefa is None:
        conn.close()
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        status = request.form["status"]

        conn.execute(
            "UPDATE tarefas SET titulo = ?, descricao = ?, status = ? WHERE id = ?",
            (titulo, descricao, status, id),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("dashboard"))

    conn.close()
    return render_template("editar_tarefa.html", tarefa=tarefa)


@app.route("/excluir/<int:id>")
@login_obrigatorio
def excluir(id):
    conn = conectar()
    conn.execute(
        "DELETE FROM tarefas WHERE id = ? AND usuario_id = ?",
        (id, usuario_logado()),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("dashboard"))



@app.route("/progresso")
@login_obrigatorio
def progresso():
    return render_template("progresso.html")


@app.route("/api/progresso")
@login_obrigatorio
def api_progresso():
    """Retorna a contagem de tarefas por status, pro Chart.js desenhar o gráfico."""
    conn = conectar()
    linhas = conn.execute(
        "SELECT status, COUNT(*) as total FROM tarefas WHERE usuario_id = ? GROUP BY status",
        (usuario_logado(),),
    ).fetchall()
    conn.close()

    dados = {"pendente": 0, "em_andamento": 0, "concluida": 0}
    for linha in linhas:
        dados[linha["status"]] = linha["total"]

    return jsonify(dados)


if __name__ == "__main__":
    criar_tabelas()
    app.run(debug=True)
