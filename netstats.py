#------------------------------------------------
#
#        Trabalho de Conclusão de Curso
#
# Faculdade de Americana - Ciência da Computação
#
#            by Gabriel Lira © 2019
#
#------------------------------------------------

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
plt.style.use('ggplot')


class Access:

    def __init__(self, logs):
        self.logs = logs


    """
    @ Rota: acesso_por_usuario
    @ Descrição: retorna um gráfico e um dataframe com a quantidade de acessos por usuário
    """
    def graph_acesso_por_usuario(self):

        acessos_por_usuario = self.logs.usuario.value_counts().to_frame().reset_index()
        acessos_por_usuario.columns = ['Usuário', 'Acessos']

        plt.figure()
        plt.tight_layout()
        graf_cod = sns.barplot(x=acessos_por_usuario['Usuário'], y=acessos_por_usuario['Acessos'])
        graph = graf_cod.get_figure()
        graph.savefig('static/acessos_por_usuario.png')

    def data_acesso_por_usuario(self):

        acessos_por_usuario = self.logs.usuario.value_counts().to_frame().reset_index()
        acessos_por_usuario.columns = ['Usuário', 'Acessos']
        data = acessos_por_usuario.head().to_html()

        return data


    """
    @ Rota: acesso_por_url
    @ Descrição: retorna uma gráfico e um dataframe com a quantidade de acessos por url
    """
    def graph_acesso_por_url(self):

        urls = self.logs.url.value_counts().to_frame().reset_index()
        urls.columns = ['URL', 'Acessos']

        x = urls.loc[(urls['Acessos'] >= 4000)].URL
        y = urls.Acessos

        plt.figure()
        plt.xticks(rotation=45)
        graf_url = sns.barplot(x=x, y=y)
        plt.tight_layout()
        fig = graf_url.get_figure()
        fig.savefig('static/acessos_por_url.png', dpi=300, bbox_inches='tight')

    def data_acesso_por_url(self):

        urls = self.logs.url.value_counts().to_frame().reset_index()
        urls.columns = ['URL', 'Acessos']
        data = urls.head().to_html()

        return data


    """
    @ Rota: acesso_por_usuario
    @ Descrição: retorna um gráfico e um dataframe com a frequência de cada código HTTP
    """
    def graph_status_code(self):

        status = self.logs.status_code.value_counts().to_frame().reset_index()
        status.columns = ['Code', 'Frequência']

        status.Code = [int(i) for i in status.Code]

        plt.figure()
        plt.tight_layout()
        graf_cod = sns.barplot(x=status['Code'].astype(int), y=status['Frequência'])
        fig = graf_cod.get_figure()
        fig.savefig('static/status_code.png')

    def data_status_code(self):

        status = self.logs.status_code.value_counts().to_frame().reset_index()
        status.columns = ['Code', 'Frequência']

        status.Code = [int(i) for i in status.Code]
        data = status.head().to_html()

        return data


class Fsan:

    def __init__(self, operacao):
        self.operacao = operacao


    def lista_de_fsans(self):

        # Lista todos os elementos da coluna operacao
        lista_com_todos = []
        for i in range(self.operacao.index.max()):
            lista_com_todos.append(self.operacao.operacao.loc[(self.operacao.operacao.index == i)].str.split())

        # Lista todos os elementos que tem algum fsan
        lista_com_fsan = []
        for i in range(self.operacao.index.max()):
            if 'fsan' in lista_com_todos[i][i]:
                lista_com_fsan.append(lista_com_todos[i][i])

        # Lista apenas o valor do fsan
        lista_fsan = []
        for i in range(len(lista_com_fsan)):
            for j in range(len(lista_com_fsan[i])):
                if 'fsan' in lista_com_fsan[i][j] and 'dslam_fsan_status:' not in lista_com_fsan[i][j]:
                    lista_fsan.append(lista_com_fsan[i][j+1])

        # Remove valores repetidos ou sujos
        fsan = []
        for item in lista_fsan:
            if item.endswith(':'):
                item = item[:-1]
            if item not in fsan:
                fsan.append(item)

        # Cria uma sequência de todas as operações com determinado fsan
        sequencia = []
        for i in fsan:
            lista = []
            for j in self.operacao.operacao:
                if i in j or i+':' in j:
                    lista.append(j)
            sequencia.append(lista)

        # Cria um dataframe para cada sequência de acontecimentos
        lista_data = []
        for i in sequencia:
            lista_data.append(pd.DataFrame(i))
            pd.set_option('display.max_colwidth', -1)

        # Nomeia a coluna de cada dataframe com o valor do fsan
        for i in range(len(lista_data)):
            lista_data[i].columns = [fsan[i]]

        return lista_data


## Lista a ultima mensagem para cada operação
#ultima_msg = []
#for i in range(len(lista_data)):
#    ultima_msg.append(lista_data[i].loc[lista_data[i].index.max(), fsan[i]])
#

'''
#-----------------------------------------------------
# Retorna um gráfico com o percentual total de sucesso
#-----------------------------------------------------
def percentual_sucesso():
    contador_creates = 0
    for item in ultima_msg:
        if 'OK' in item or 'onu_business_create' in item or 'voip_create:' in item or 'onu_delete: fsan' in item:
            contador_creates += 1

    cruzo_creates = contador_creates*100
    resultado_sucesso = cruzo_creates/len(ultima_msg)

    #Percentual de ERROR
    contador_error = 0
    for item in ultima_msg:
        if 'error' in item:
            contador_error += 1

    cruzo_error = contador_error*100
    resultado_error = cruzo_error/len(ultima_msg)

    ocorrencia = {
        'tipo': ['Sucesso', 'Erro'],
        'quantidade': [resultado_sucesso, resultado_error]
    }

    data_ocorrencia = {
        'Resultado': ['Sucesso', 'Erro'],
        'FSANs': [contador_creates, contador_error]
    }

    data_ocorrencia = pd.DataFrame(data_ocorrencia)

    labels = ocorrencia['tipo']
    sizes = ocorrencia['quantidade']
    colors = ['yellowgreen', 'gold']
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(sizes, colors=colors, shadow=True,
           startangle=90, autopct='%1.1f%%')
    ax.legend(labels, loc="best")
    ax.axis('equal')
    plt.savefig('static/percentual_sucesso.png')


#----------------------------------------------------------------
# Retorna um gráfico com as operações que obtiveram mais sucessos
#----------------------------------------------------------------
def sucesso_por_operacao():
    sucessos = []
    for i in range(len(ultima_msg)):
        if 'error' not in ultima_msg[i]:
            corte_sucessos = ultima_msg[i].split()
            sucessos.append(corte_sucessos[0])

    lista_sucessos = []
    for item in sucessos:
        if item not in lista_sucessos:
            lista_sucessos.append(item)

    smart = 0
    onu_delete = 0
    onu_business_create = 0
    voip_create = 0

    for item in sucessos:
        if 'smart' in item:
            smart += 1

        elif 'onu_delete:' in item:
            onu_delete += 1

        elif 'onu_business_create:' in item:
            onu_business_create += 1

        elif 'voip_create:' in item:
            voip_create += 1

    quantidade_sucessos = {
        'Função': ['onu_home_create', 'onu_delete', 'voip_create', 'onu_business_create'],
        'Quantidade': [smart, onu_delete, voip_create, onu_business_create]
    }

    quantidade_sucessos = pd.DataFrame(quantidade_sucessos)

    labels = quantidade_sucessos['Função']
    sizes = quantidade_sucessos['Quantidade']
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(sizes, colors=colors, shadow=True,
           startangle=90, labels=labels, rotatelabels=True)
    ax.legend(labels, loc="best")
    ax.axis('equal')
    plt.savefig('static/operacao_sucesso.png')


#-------------------------------------------------------------
# Retorna um gráfico com as operações que obtiveram mais erros
#-------------------------------------------------------------
def erros_por_operacao():
    erros = []
    for i in range(len(ultima_msg)):
        if 'error' in ultima_msg[i]:
            corte_erros = ultima_msg[i].split()
            erros.append(corte_erros[0])

    lista_erros = []
    for item in erros:
        if item not in lista_erros:
            lista_erros.append(item)

    vDELETE = 0
    onu_bridge_path_list = 0
    onu_resync_update = 0
    omci_onu_status = 0
    vCREATE = 0
    wifi_update = 0
    onu_status = 0
    onu_set2default_update = 0
    onu_checa_status = 0
    dslam_fsan_status = 0
    onu_check_conf_status = 0

    for item in erros:
        if 'DELETE' in item:
            vDELETE += 1

        elif 'onu_bridge_path_list:' in item:
            onu_bridge_path_list += 1

        elif 'onu_resync_update:' in item:
            onu_resync_update += 1

        elif 'onu_resync_update:' in item:
            onu_resync_update += 1

        elif 'omci_onu_status:' in item:
            omci_onu_status += 1

        elif 'CREATE' in item:
            vCREATE += 1

        elif 'wifi_update:' in item:
            wifi_update += 1

        elif 'onu_status:' in item:
            onu_status += 1

        elif 'onu_set2default_update:' in item:
            onu_set2default_update += 1

        elif 'onu_checa_status:' in item:
            onu_checa_status += 1

        elif 'dslam_fsan_status:' in item:
            dslam_fsan_status += 1

        elif 'onu_check_conf_status:' in item:
            onu_check_conf_status += 1

    quantidade_erros = {
        'Função': [
            'DELETE', 'onu_bridge_path_list', 'onu_check_conf_status', 'onu_checa_status',
            'omci_onu_status', 'CREATE', 'onu_resync_update', 'onu_set2default_update',
            'dslam_fsan_status', 'wifi_update', 'onu_status'
        ],
        'Quantidade': [
            vDELETE, onu_bridge_path_list, onu_check_conf_status, onu_checa_status,
            omci_onu_status, vCREATE, onu_resync_update, onu_set2default_update,
            dslam_fsan_status, wifi_update, onu_status
        ]
    }

    quantidade_erros = pd.DataFrame(quantidade_erros)

    labels = quantidade_erros['Função']
    sizes = quantidade_erros['Quantidade']
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'crimson', 'darkblue',
              'fuchsia', 'sienna', 'tan', 'orangered', 'dimgray']
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(sizes, colors=colors, shadow=True, startangle=90, labels=labels, labeldistance=0.7,
           rotatelabels=True, textprops=dict(rotation_mode='anchor', va='center',
                                             ha='center'))
    ax.legend(labels, loc="best")
    ax.axis('equal')
    plt.savefig('static/operacao_error.png')
'''
