import csv
import os
from flask import Flask, render_template, url_for, request, redirect, flash

from google import genai

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'super secret key')

GENAI_API_KEY = os.getenv("GENAI_API_KEY", "AIzaSyAOjWk97-zMQ0xVJ0KMmVmEaUzUyN-2a7Y")
client = genai.Client(api_key=GENAI_API_KEY)


def call_gemini_api(question):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=question
        )
        return response.text
    except Exception as e:
        return f"Erro ao chamar a API: {e}"


@app.route('/')
def ola():
    return render_template('index.html')


@app.route('/sobre-equipe')
def sobre_equipe():
    return render_template('sobre_equipe.html')


@app.route('/estruturas-selecao')
def estruturas_selecao():
    return render_template('selecao.html')


@app.route('/estruturas-repeticao')
def estruturas_repeticao():
    return render_template('repeticao.html')


@app.route('/vetores-matrizes')
def vetores_matrizes():
    return render_template('vetores_matrizes.html')


@app.route('/funcoes-procedimentos')
def funcoes_procedimentos():
    return render_template('funcoes.html')


@app.route('/tratamento-excecoes')
def tratamento_excecoes():
    return render_template('excecoes.html')


@app.route('/glossario')
def glossario():
    glossario_de_termos = []
    with open('bd_glossario.csv', 'r', newline='', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo, delimiter=';')
        for linha in reader:
            glossario_de_termos.append(linha)
    return render_template('glossario.html', glossario=glossario_de_termos)


@app.route('/novo-termo')
def novo_termo():
    return render_template('novo_termo.html')


@app.route('/criar_termo', methods=['POST'])
def criar_termo():
    termo = request.form['termo'].strip()
    definicao = request.form['definicao'].strip()

    if not termo or not definicao:
        flash('Termo e definição não podem estar vazios.', 'error')
        return redirect(url_for('novo_termo'))

    with open('bd_glossario.csv', 'a', newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo, delimiter=';')
        writer.writerow([termo, definicao])

    flash(f'O termo "{termo}" foi adicionado ao glossário!', 'success')
    return redirect(url_for('glossario'))


@app.route('/duvidas', methods=['GET', 'POST'])
def duvidas():
    resposta_gemini = None
    pergunta = None
    error = None
    if request.method == 'POST':
        pergunta = request.form['pergunta']
        if pergunta:
            resposta_gemini = call_gemini_api(pergunta)
        else:
            error = "A pergunta não pode estar vazia."
    return render_template('duvidas.html', resposta=resposta_gemini, pergunta=pergunta, error=error)


if __name__ == '__main__':
    app.run(debug=True)
