from netstats.fsan import Fsan
from netstats.lista_dataframe import ListaDataframe


class ListaMensagens:

    def __init__(self, operacao):
        self.operacao = operacao


    def mensagem(self):

        """
            Retorna lista com a última mensagem de cada dataframe de FSANs.

            Returns
            -------
                list
        """

        fsan = Fsan(self.operacao).lista_de_fsans()
        dataframe = ListaDataframe(self.operacao).dataframe()

        ultima_msg = []
        for i in range(len(dataframe)):
            ultima_msg.append(dataframe[i].loc[dataframe[i].index.max(), fsan[i]])

        return ultima_msg
