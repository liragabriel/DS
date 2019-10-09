from netstats.lista_dataframe import ListaDataframe


class EstatisticasGerais:

    def __init__(self, operacao):
        self.operacao = operacao


    def estatisticas(self):

        lista_data = ListaDataframe(self.operacao).dataframe()

        lista_com_todos = []
        for x in range(self.operacao.index.max()):
            lista_com_todos.append(self.operacao.operacao.loc[(self.operacao.operacao.index == x)].str.split())

        lista_com_fsan = []
        for x in range(self.operacao.index.max()):
            if 'fsan' in lista_com_todos[x][x]:
                lista_com_fsan.append(lista_com_todos[x][x])

        lista_fsan = []
        for c in range(len(lista_com_fsan)):
            for x in range(len(lista_com_fsan[c])):
                if 'fsan' in lista_com_fsan[c][x] and 'dslam_fsan_status:' not in lista_com_fsan[c][x]:
                    lista_fsan.append(lista_com_fsan[c][x+1])

        fsan = []
        for item in lista_fsan:
            if item.endswith(':'):
                item = item[:-1]
            if item not in fsan:
                fsan.append(item)

        operacoes = len(lista_com_fsan)
        fsans = len(fsan)
        media = len(lista_com_fsan) / len(fsan)

        maior = []
        for item in lista_data:
            maior.append(item.index.max())
        res_maior = max(maior)

        data_stats_success = {
            'Quantidade de operações': int(operacoes),
            'Quantidade de fsans': int(fsans),
            'Média de operações por fsan': int(media),
            'Maior número de operações em uma fsan': int(res_maior),
        }

        return data_stats_success
