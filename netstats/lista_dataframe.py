import pandas as pd
from netstats.fsan import Fsan


class ListaDataframe:

    def __init__(self, operacao):
        self.operacao = operacao


    def dataframe(self):

        """
            Retorna uma lista de dataframes por FSAN, cada dataframe contém as operações realizadas

            com a FSAN.

            Returns
            -------
                list
        """

        fsan = Fsan(self.operacao).lista_de_fsans()

        sequencia = []
        for i in fsan:
            lista = []
            for j in self.operacao.operacao:
                if i in j or i+':' in j:
                    lista.append(j)
            sequencia.append(lista)

        lista_data = []
        for i in sequencia:
            lista_data.append(pd.DataFrame(i))
            pd.set_option('display.max_colwidth', -1)

        for i in range(len(lista_data)):
            lista_data[i].columns = [fsan[i]]

        return lista_data
