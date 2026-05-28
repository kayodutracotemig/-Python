from flask import Flask, request, render_template_string

app = Flask(__name__)

usuarios_permitidos = {
    'kayo': '22402039', 
    'dolga': 'cotemig2026',
    'janaina': 'cotemig2026',
    'antonio': 'cotemig2026'
}

def show_the_login_form():
    return render_template_string("""
        <h2>Sistemas de Login - COTEMIG</h2>
        <form method="POST">
            <input type="text" name="usuario" placeholder="Usuário" required><br><br>
            <input type="password" name="senha" placeholder="Senha" required><br><br>
            <button type="submit">Entrar</button>
        </form>
    """)

def do_the_login():
    usuario_digitado = request.form.get('usuario')
    senha_digitada = request.form.get('senha')

    login_valido = False

    for usuario_salvo, senha_salva in usuarios_permitidos.items():
        if usuario_digitado == usuario_salvo and senha_digitada == senha_salva:
            login_valido = True
            break 

    if login_valido:
        return f"<h1>Bem-vindo, {usuario_digitado}! Acesso concedido.</h1>"
    else:
        return "<h1>Login ou senha inválidos.</h1>"

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()

if __name__ == "__main__":
    app.run(debug=True)