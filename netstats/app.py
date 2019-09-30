"""
            Trabalho de Conclusão de Curso
    Faculdade de Americana - Ciência da Computação
                Gabriel Lira © 2019
"""

import os
import pandas as pd
from flask import Flask, render_template, request
from netstats.access import Access
from netstats.fsan import Fsan
from netstats.lista_dataframe import ListaDataframe
from netstats.error import Error
from netstats.estatisticas_gerais import EstatisticasGerais


logs = pd.read_csv(r'/home/desktop/dev/netstats/websvc_access.csv')
logs.drop('fora', inplace=True, axis=1)
operacao = pd.read_csv(r'/home/desktop/dev/netstats/websvc_error1.csv')


class Netstats:

    def __init__(self):
        self.access = Access(logs)
        self.fsan = Fsan(operacao)
        self.lista_data = ListaDataframe(operacao)
        self.error = Error(operacao)
        self.estatisticas = EstatisticasGerais(operacao)


app = Flask(__name__)
netstats = Netstats()


@app.route('/')
@app.route('/home')
def home():
    for imagem in os.listdir('static'):
        if imagem in os.listdir('static'):
            if imagem != 'estilo.css' and imagem != 'fontAwesome':
                os.remove(f'static/{imagem}')

    resposta = netstats.estatisticas.estatisticas()

    return render_template('home.html', data=resposta)


@app.route('/pesquisar-fsan', methods=['POST', 'GET'])
def pesquisar_fsan():

    if request.method == 'POST':

        fsan_value = request.form['fsan']

        for tabela in netstats.lista_data.dataframe():
            if fsan_value == tabela.columns:
                resposta = tabela.to_json(orient='values')
                break
            else:
                resposta = 'FSAN não identificado'
        return render_template('pesquisar_fsan.html', resposta=resposta, fsan=fsan_value)

    else:
        return render_template('pesquisar_fsan.html')


@app.route('/analises')
def analises():

    while True:
        if not os.path.exists('static/acessos_por_usuario.png'):
            netstats.access.graph_acesso_por_usuario()

        if not os.path.exists('static/acessos_por_url.png'):
            netstats.access.graph_acesso_por_url()

        if not os.path.exists('static/status_code.png'):
            netstats.access.graph_status_code()

        if not os.path.exists('static/percentual_sucesso.png'):
            netstats.error.percentual_sucesso()

        if not os.path.exists('static/operacao_sucesso.png'):
            netstats.error.sucesso_por_operacao()

        if not os.path.exists('static/operacao_error.png'):
            netstats.error.erros_por_operacao()

        else:
            return render_template('analises.html')


@app.route('/acessos-por-usuario')
def acesso_por_usuario():
    return render_template('acessos_por_usuario.html',
                           data=netstats.access.data_acesso_por_usuario())


@app.route('/acessos-por-url')
def rota_acesso_por_url():
    return render_template('acessos_por_url.html',
                           data=netstats.access.data_acesso_por_url())


@app.route('/status-code')
def rota_status_code():
    return render_template('status_code.html', data=netstats.access.data_status_code())


@app.route('/percentual-sucesso')
def rota_percentual_sucesso():
    return render_template('percentual_sucesso.html')


@app.route('/sucesso-por-operacao')
def rota_sucesso_por_operacao():
    return render_template('sucesso_por_operacao.html')


@app.route('/erros-por-operacao')
def rota_erros_por_operacao():
    return render_template('operacao_error.html')


if __name__ == '__main__':
    app.run(debug=True)
