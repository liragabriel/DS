import pandas as pd
from matplotlib import pyplot as plt
from netstats.lista_mensagens import ListaMensagens


class Error:

    def __init__(self, operacao):
        self.operacao = operacao


    def percentual_sucesso(self):

        """
            Cria um arquivo png com o gráfico representando o percentual de sucessos por operação.

            Returns
            -------
                None
        """

        ultima_msg = ListaMensagens(self.operacao).mensagem()

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


    def sucesso_por_operacao(self):

        """
            Cria um arquivo png com o gráfico representando a quantidade de operações bem-sucedidas

            para cada operação.

            Returns
            -------
                None
        """

        ultima_msg = ListaMensagens(self.operacao).mensagem()

        sucessos = []
        for i in range(len(ultima_msg)):
            if 'error' not in ultima_msg[i]:
                corte_sucessos = ultima_msg[i].split()
                sucessos.append(corte_sucessos[0])

        lista_sucessos = []
        for item in sucessos:
            if item not in lista_sucessos:
                lista_sucessos.append(item)

        dic = {
            'smart': 0,
            'onu_delete:': 0,
            'onu_business_create:': 0,
            'voip_create:': 0
        }

        for item in sucessos:
            for operacao in dic:
                if item == operacao:
                    dic[operacao] += 1

        quantidade_sucessos = {
            'Função': [
                'onu_home_create', 'onu_delete', 'voip_create', 'onu_business_create'
                ],
            'Quantidade': [
                dic['smart'], dic['onu_delete:'], dic['voip_create:'], dic['onu_business_create:']
                ]
        }

        quantidade_sucessos = pd.DataFrame(quantidade_sucessos)

        labels = quantidade_sucessos['Função']
        sizes = quantidade_sucessos['Quantidade']
        colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(sizes, colors=colors, shadow=True)
        ax.legend(labels, loc="best")
        ax.axis('equal')
        plt.savefig('static/operacao_sucesso.png')


    def erros_por_operacao(self):

        """
            Cria um arquivo png com o gráfico representando a quantidade de operações malsucedidas

            para cada operação.

            Returns
            -------
                None
        """

        ultima_msg = ListaMensagens(self.operacao).mensagem()

        erros = []
        for i in range(len(ultima_msg)):
            if 'error' in ultima_msg[i]:
                corte_erros = ultima_msg[i].split()
                erros.append(corte_erros[0])

        lista_erros = []
        for item in erros:
            if item not in lista_erros:
                lista_erros.append(item)

        dic = {
            'DELETE': 0,
            'onu_bridge_path_list:': 0,
            'onu_resync_update:': 0,
            'omci_onu_status:': 0,
            'CREATE': 0,
            'wifi_update:': 0,
            'onu_status:': 0,
            'onu_set2default_update:': 0,
            'onu_checa_status:': 0,
            'dslam_fsan_status:': 0,
            'onu_check_conf_status:': 0,
        }

        for item in erros:
            for operacao in dic:
                if item == operacao:
                    dic[operacao] += 1

        quantidade_erros = {
            'Função': [
                'DELETE', 'onu_bridge_path_list', 'onu_check_conf_status', 'onu_checa_status',
                'omci_onu_status', 'CREATE', 'onu_resync_update', 'onu_set2default_update',
                'dslam_fsan_status', 'wifi_update', 'onu_status'
            ],
            'Quantidade': [
                dic['DELETE'], dic['onu_bridge_path_list:'], dic['onu_resync_update:'],
                dic['omci_onu_status:'], dic['CREATE'], dic['wifi_update:'],
                dic['onu_status:'], dic['onu_set2default_update:'],
                dic['onu_checa_status:'], dic['dslam_fsan_status:'],
                dic['onu_check_conf_status:']
                ]
        }

        quantidade_erros = pd.DataFrame(quantidade_erros)

        labels = quantidade_erros['Função']
        sizes = quantidade_erros['Quantidade']
        colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'crimson', 'darkblue',
                  'fuchsia', 'sienna', 'tan', 'orangered', 'dimgray']
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(sizes, colors=colors, shadow=True)
        ax.legend(labels, loc="best")
        ax.axis('equal')
        plt.savefig('static/operacao_error.png')
