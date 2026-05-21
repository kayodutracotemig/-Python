from flask import Flask

app = Flask(__name__)

@app.route("/")
def paginaInicial():
    return("Olá")

@app.route("/pagina2")
def paginaSecundaria():
    return("Voce está na segunda pagina")

if __name__ == "__main__":
    app.run(debug=True)