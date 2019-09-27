class Fsan:

    def __init__(self, operacao):
        self.operacao = operacao


    def lista_de_fsans(self):

        """
            Retorna uma lista com todos FSANs na base de dados.

            Returns
            -------
                list
        """

        lista_com_todos = []
        for i in range(self.operacao.index.max()):
            lista_com_todos.append(self.operacao.operacao.loc[(self.operacao.operacao.index ==
                                                               i)].str.split())

        lista_com_fsan = []
        for i in range(self.operacao.index.max()):
            if 'fsan' in lista_com_todos[i][i]:
                lista_com_fsan.append(lista_com_todos[i][i])

        lista_fsan = []
        for i in range(len(lista_com_fsan)):
            for j in range(len(lista_com_fsan[i])):
                if 'fsan' in lista_com_fsan[i][j] and 'dslam_fsan_status:' not in lista_com_fsan[i][j]:
                    lista_fsan.append(lista_com_fsan[i][j+1])

        fsan = []
        for item in lista_fsan:
            if item.endswith(':'):
                item = item[:-1]
            if item not in fsan:
                fsan.append(item)

        return fsan
