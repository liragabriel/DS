import seaborn as sns
from matplotlib import pyplot as plt
plt.style.use('ggplot')


class Access:

    def __init__(self, logs):
        self.logs = logs


    def graph_acesso_por_usuario(self):

        """
            Cria um arquivo png com o gráfico representando a quantidade de acessos por API.

            Returns
            -------
                None
        """

        acessos_por_usuario = self.logs.usuario.value_counts().to_frame().reset_index()
        acessos_por_usuario.columns = ['Usuário', 'Acessos']

        plt.figure()
        plt.tight_layout()
        graf_cod = sns.barplot(x=acessos_por_usuario['Usuário'], y=acessos_por_usuario['Acessos'])
        graph = graf_cod.get_figure()
        graph.savefig('static/acessos_por_usuario.png')


    def data_acesso_por_usuario(self):

        """
            Cria um dataframe com a quantidade de acessos por API.

            Returns
            -------
                dataframe
        """

        acessos_por_usuario = self.logs.usuario.value_counts().to_frame().reset_index()
        acessos_por_usuario.columns = ['Usuário', 'Acessos']
        data = acessos_por_usuario.head().to_html()

        return data


    def graph_acesso_por_url(self):

        """
            Cria um arquivo png com o gráfico representando a quantidade de acessos por URL.

            Returns
            -------
                None
        """

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

        """
            Cria um dataframe com a quantidade de acessos por URL.

            Returns
            -------
                dataframe
        """

        urls = self.logs.url.value_counts().to_frame().reset_index()
        urls.columns = ['URL', 'Acessos']
        data = urls.head().to_html()

        return data



    def graph_status_code(self):

        """
            Cria um arquivo png com o gráfico representando a frequência de cada status code.

            Returns
            -------
                None
        """

        status = self.logs.status_code.value_counts().to_frame().reset_index()
        status.columns = ['Code', 'Frequência']

        status.Code = [int(i) for i in status.Code]

        plt.figure()
        plt.tight_layout()
        graf_cod = sns.barplot(x=status['Code'].astype(int), y=status['Frequência'])
        fig = graf_cod.get_figure()
        fig.savefig('static/status_code.png')


    def data_status_code(self):

        """
            Cria um dataframe com a frequência de cada status code.

            Returns
            -------
                dataframe
        """

        status = self.logs.status_code.value_counts().to_frame().reset_index()
        status.columns = ['Code', 'Frequência']

        status.Code = [int(i) for i in status.Code]
        data = status.head().to_html()

        return data
