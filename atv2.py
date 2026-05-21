from flask import Flask

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def paginaInicial():
    return("""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Currículo - Seu Nome</title>
        <style>
            body { font-family: 'Arial', sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; background-color: #f4f4f4; }
            .cv-container { background: #fff; padding: 40px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; margin-bottom: 5px; }
            h2 { color: #3498db; border-bottom: 2px solid #3498db; padding-bottom: 10px; margin-top: 30px; }
            .header-info { text-align: center; margin-bottom: 30px; }
            .experience-item, .education-item { margin-bottom: 20px; }
            .job-title, .school-name { font-weight: bold; }
            .job-date, .school-date { color: #7f8c8d; font-style: italic; }
            ul { margin-top: 5px; }
        </style>
    </head>
    <body>
        <div class="cv-container">
            <header class="header-info">
                <h1>Seu Nome Completo</h1>
                <p>Desenvolvedor Front-end | HTML, CSS, JavaScript</p>
                <p>kayoodutra.s@gmail.com | (31) 997733737 | Cidade - MG</p>
                <p><a href="https://www.linkedin.com/in/kayo-dutra-dos-santos-3aa87434a/?skipRedirect=true" target="_blank">LinkedIn</a> | <a href="https://github.com/kayodutracotemig" target="_blank">GitHub</a></p>
            </header>

            <section id="sobre">
                <h2>Resumo Profissional</h2>
                <p>Profissional apaixonado por tecnologia com experiência em criar interfaces responsivas e funcionais utilizando HTML, CSS e JavaScript. Focado em UX e desempenho.</p>
            </section>

            <section id="experiencia">
                <h2>Experiência Profissional</h2>
                <div class="experience-item">
                    <p class="job-title">Desenvolvedor Web</p>
                    <ul>
                        <li>Desenvolvimento de layouts responsivos utilizando HTML5 e CSS3.</li>
                        <li>Otimização de performance de sites (SEO e velocidade).</li>
                    </ul>
                </div>
            </section>

            <section id="educacao">
                <h2>Educação</h2>
                <div class="education-item">
                    <p class="school-date">COTEMIG - 2024-2026</p>
                </div>
            </section>

            <section id="habilidades">
                <h2>Habilidades</h2>
                <p>HTML5, CSS3, JavaScript, React, Git,Responsividade.</p>
            </section>
        </div>
    </body>
    </html>
""")

@app.route("/pagina2")
def paginaSecundaria():
    return

if __name__ == "__main__":
    app.run(debug=True)