import os
import pandas as pd
from flask import Flask, render_template, request
from netstats import Access, Fsan, ListaData, Error


logs = pd.read_csv(r'/home/desktop/lng/teste_tcc/websvc_access.csv')
logs.drop('fora', inplace=True, axis=1)
operacao = pd.read_csv(r'/home/desktop/dev/jupyter/DS/websvc_error1.csv')


class Netstats:

    def __init__(self):
        self.access = Access(logs)
        self.fsan = Fsan(operacao)
        self.lista_data = ListaData(operacao)
        self.error = Error(operacao)


app = Flask(__name__)
netstats = Netstats()


# Retorna o template inicial e exclui todos os gráficos gerados
@app.route('/')
@app.route('/home')
def home():
    for imagem in os.listdir('static'):
        if imagem in os.listdir('static'):
            if imagem != 'estilo.css' and imagem != 'fontAwesome':
                os.remove(f'static/{imagem}')
    return render_template('home.html')


# Retorna todas operações com o fsan pesquisado
@app.route('/pesquisar-fsan', methods=['POST', 'GET'])
def pesquisar_fsan():
    if request.method == 'POST':
        fsan_value = request.form['fsan']
        for tabela in netstats.lista_data.dataframe():
            if fsan_value == tabela.columns:
                resposta = tabela.to_html(index=False)
                break
            else:
                resposta = 'FSAN não identificado'
        return render_template('pesquisar_fsan.html', resposta=resposta)
    else:
        return render_template('pesquisar_fsan.html')


@app.route('/analises')
def analises():
    return render_template('analises.html')


@app.route('/acessos-por-usuario')
def acesso_por_usuario():
    imagem = 'static/acessos_por_usuario.png'
    while True:
        if os.path.exists(imagem):
            return render_template('acessos_por_usuario.html',
                                   data=netstats.access.data_acesso_por_usuario())
        else:
            netstats.access.graph_acesso_por_usuario()


@app.route('/acessos-por-url')
def rota_acesso_por_url():
    imagem = 'static/acessos_por_url.png'
    while True:
        if os.path.exists(imagem):
            return render_template('acessos_por_url.html',
                                   data=netstats.access.data_acesso_por_url())
        else:
            netstats.access.graph_acesso_por_url()


@app.route('/status-code')
def rota_status_code():
    imagem = 'static/status_code.png'
    while True:
        if os.path.exists(imagem):
            return render_template('status_code.html', data=netstats.access.data_status_code())
        else:
            netstats.access.graph_status_code()


"""ERROR"""
@app.route('/percentual-sucesso')
def rota_percentual_sucesso():
    imagem = 'static/percentual_sucesso.png'
    while True:
        if os.path.exists(imagem):
            return render_template('percentual_sucesso.html')
        else:
            netstats.error.percentual_sucesso()


@app.route('/sucesso-por-operacao')
def rota_sucesso_por_operacao():
    imagem = 'static/operacao_sucesso.png'
    while True:
        if os.path.exists(imagem):
            return render_template('sucesso_por_operacao.html')
        else:
            netstats.error.sucesso_por_operacao()


@app.route('/erros-por-operacao')
def rota_erros_por_operacao():
    imagem = 'static/operacao_error.png'
    while True:
        if os.path.exists(imagem):
            return render_template('operacao_error.html')
        else:
            netstats.error.erros_por_operacao()


if __name__ == '__main__':
    app.run(debug=True)
