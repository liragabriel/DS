import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

class Error:

    operacao = pd.read_csv(r'/home/desktop/dev/jupyter/error/websvc_error1.csv')

    #Lista todos os elementos da coluna operacao
    lista_com_todos = []
    for x in range(operacao.index.max()):
        lista_com_todos.append(operacao.operacao.loc[(operacao.operacao.index==x)].str.split())

    #Lista todos os elementos que tem algum fsan
    lista_com_fsan = []
    for x in range(operacao.index.max()):
        if 'fsan' in lista_com_todos[x][x]:
            lista_com_fsan.append(lista_com_todos[x][x])

    #Lista apenas o valor do fsan
    lista_fsan = []
    for c in range(len(lista_com_fsan)):
        for x in range(len(lista_com_fsan[c])):
            if 'fsan' in lista_com_fsan[c][x] and 'dslam_fsan_status:' not in lista_com_fsan[c][x]:
                lista_fsan.append(lista_com_fsan[c][x+1])

    #Remove valores repetidos ou sujos
    fsan = []
    for item in lista_fsan:
        if item.endswith(':'):
            item = item[:-1]
        if item not in fsan:
            fsan.append(item)

    #Cria uma sequência de todas as operaçãoes com determinado fsan
    sequencia = []
    for c in fsan:
        lista = []
        for x in operacao.operacao:
            if c in x or c+':' in x:
                lista.append(x)
        sequencia.append(lista)

    #Cria um dataframe para cada sequência de acontecimentos
    lista_data = []
    for x in sequencia:
        lista_data.append(pd.DataFrame(x))

    #Nomeia a coluna de cada dataframe com o valor do fsan
    for x in range(len(lista_data)):
        lista_data[x].columns = [fsan[x]]

    #Lista a ultima mensagem para cada operação
    ultima_msg = []
    for x in range(len(lista_data)):
        ultima_msg.append(lista_data[x].loc[lista_data[x].index.max(), fsan[x]])


    operacoes = len(lista_com_fsan) #Retorna quantidade de operações

    fsans = len(fsan) #Retorna numero de fsans

    media = len(lista_com_fsan) / len(fsan) #Retorna media de operações por fsan

    maior = [] 
    for item in lista_data:
        maior.append(item.index.max()) #Retorna a fsan com maior número de operações
    res_maior = max(maior)

    data_stats_sucess = {
        'Parâmetro': ['Quantidade de operações', 'Quantidade de fsans', 'Média de operações por fsan', 'Maior número de operações em uma fsan' ],
        'Quantidade': [int(operacoes), int(fsans), int(media), int(res_maior)]
    }

    data_stats_sucess = pd.DataFrame(data_stats_sucess)



    #Percentual de CREATEs
    contador_creates = 0
    for item in ultima_msg:
        if 'OK' in item or 'onu_business_create' in item or 'voip_create:' in item or 'onu_delete: fsan' in item:
            contador_creates += 1

    cruzo_creates = contador_creates*100
    resultado_sucesso = cruzo_creates/len(ultima_msg)

    #Percentual de ERROR
    contador_error = 0
    for item in ultima_msg:
        if '"error"' in item:
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
    fig, ax = plt.subplots(figsize=(8,8))
    ax.pie(sizes, colors=colors, shadow=True, startangle=90, autopct='%1.1f%%')
    ax.legend(labels, loc="best")
    ax.axis('equal')

 

    sucessos = []
    for x in range(len(ultima_msg)):
        if '"error"' not in ultima_msg[x]:
            corte_sucessos = ultima_msg[x].split()
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
    fig, ax = plt.subplots(figsize=(8,8))
    ax.pie(sizes, colors=colors, shadow=True, startangle=90, labels=labels, rotatelabels=True)
    ax.legend(labels, loc="best")
    ax.axis('equal')



    erros = []
    for x in range(len(ultima_msg)):
        if '"error"' in ultima_msg[x]:
            corte_erros = ultima_msg[x].split()
            erros.append(corte_erros[0])

    lista_erros = []
    for item in erros:
        if item not in lista_erros:
            lista_erros.append(item)
                
    DELETE = 0
    onu_bridge_path_list = 0
    onu_resync_update = 0
    omci_onu_status = 0
    CREATE = 0
    wifi_update = 0
    onu_status = 0
    onu_set2default_update = 0
    onu_checa_status = 0
    dslam_fsan_status = 0
    onu_check_conf_status = 0

    for item in erros:
        if 'DELETE' in item:
            DELETE += 1

        elif 'onu_bridge_path_list:' in item:
            onu_bridge_path_list += 1

        elif 'onu_resync_update:' in item:
            onu_resync_update += 1  

        elif 'onu_resync_update:' in item:
            onu_resync_update += 1

        elif 'omci_onu_status:' in item:
            omci_onu_status += 1

        elif 'CREATE' in item:
            CREATE += 1

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
            'omci_onu_status', 'CREATE', 'onu_resync_update', 'onu_set2default_update', 'dslam_fsan_status', 'wifi_update', 'onu_status'
        ],
        'Quantidade': [
            DELETE, onu_bridge_path_list, onu_check_conf_status, onu_checa_status,
            omci_onu_status, CREATE, onu_resync_update, onu_set2default_update, dslam_fsan_status, wifi_update, onu_status
        ]
    }

    quantidade_erros = pd.DataFrame(quantidade_erros)

    labels = quantidade_erros['Função']
    sizes = quantidade_erros['Quantidade']
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral','crimson','darkblue','fuchsia','sienna','tan','orangered','dimgray']
    fig, ax = plt.subplots(figsize=(9,15))
    ax.pie(sizes, colors=colors, shadow=True, startangle=90, labels=labels, labeldistance=0.7, rotatelabels=True, textprops = dict(rotation_mode = 'anchor', va='center', ha='center'))
    ax.legend(labels, loc="best")
    ax.axis('equal')

class Access:

    logs = pd.read_csv('websvc_access.csv')
    logs.drop('fora', inplace=True, axis=1)

    #Acesso por usuário
    acessos_por_usuario = logs.usuario.value_counts().to_frame().reset_index()
    acessos_por_usuario.columns = ['Usuario', 'Acessos']
    print(acessos_por_usuario)

    labels = acessos_por_usuario['Usuario']
    sizes = acessos_por_usuario['Acessos']
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral','crimson','darkblue','fuchsia','sienna']
    patches, texts = plt.pie(sizes, colors=colors, shadow=True, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.axis('equal')
    plt.tight_layout()

    #Acessos por url
    urls = logs.url.value_counts().to_frame().reset_index()
    urls.columns = ['url', 'acessos']

    #Gŕafico do acesso às URLs
    x = urls.loc[(urls['acessos']>=100)].url
    y = urls.acessos

    plt.figure(figsize=(40,7))
    plt.xticks(rotation=45)
    plt.title('URLs mais acessadas')
    sns.barplot(x=x, y=y, palette='GnBu_d')

    #Horário dos Acessos
    pico_de_acesso = logs.datas.value_counts().to_frame().reset_index()
    pico_de_acesso.columns = ['Hora', 'Acessos']

    #Gŕafico entre o período com mais acessos
    x = pico_de_acesso.loc[(pico_de_acesso['Acessos']>=10)].Hora
    y = pico_de_acesso.Acessos

    plt.figure(figsize=(40,7))
    plt.xticks(rotation=45)
    plt.title('Variação durante o horário com mais acessos')
    sns.lineplot(x=x, y=y)

    #Gráfico de acesso durante o dia
    #Gráfico de acessos entre 6:25 e 6:59
    grafico_seis = logs.datas.loc[(logs.datas.index<235)].value_counts().reset_index()
    grafico_seis.columns = ['hora', 'acessos']
    res_grafico_seis = grafico_seis.acessos.count()

    #Gráfico de acessos entre 7:00 e 7:59
    grafico_sete = logs.datas.loc[(logs.datas.index<2380)].value_counts().reset_index()
    grafico_sete.columns = ['hora', 'acessos']
    res_grafico_sete = grafico_sete.acessos.count() - res_grafico_seis

    #Gráfico de acessos entre 8:00 e 8:59
    grafico_oito = logs.datas.loc[(logs.datas.index<5906)].value_counts().reset_index()
    grafico_oito.columns = ['hora', 'acessos']
    res_grafico_oito = grafico_oito.acessos.count() - res_grafico_sete - res_grafico_seis

    #Gráfico de acessos entre 9:00 e 9:59
    grafico_nove = logs.datas.loc[(logs.datas.index<9821)].value_counts().reset_index()
    grafico_nove.columns = ['hora', 'acessos']
    res_grafico_nove = grafico_nove.acessos.count() - res_grafico_oito - res_grafico_sete - res_grafico_seis

    #Gráfico de acessos entre 10:00 e 10:59
    grafico_dez = logs.datas.loc[(logs.datas.index<16140)].value_counts().reset_index()
    grafico_dez.columns = ['hora', 'acessos']
    res_grafico_dez = grafico_dez.acessos.count() - res_grafico_nove - res_grafico_oito - res_grafico_sete - res_grafico_seis

    #Gráfico de acessos entre 11:00 e 11:59
    grafico_onze = logs.datas.loc[(logs.datas.index<21392)].value_counts().reset_index()
    grafico_onze.columns = ['hora', 'acessos']
    res_grafico_onze = grafico_onze.acessos.count() - res_grafico_dez - res_grafico_nove - res_grafico_oito - res_grafico_sete - res_grafico_seis

    #Gráfico de acessos entre 12:00 e 12:59
    grafico_doze = logs.datas.loc[(logs.datas.index<26538)].value_counts().reset_index()
    grafico_doze.columns = ['hora', 'acessos']
    res_grafico_doze = grafico_doze.acessos.count() - res_grafico_onze - res_grafico_dez - res_grafico_nove - res_grafico_oito - res_grafico_sete - res_grafico_seis

    #Gráfico de acessos entre 13:00 e 13:59
    grafico_treze = logs.datas.loc[(logs.datas.index<30836)].value_counts().reset_index()
    grafico_treze.columns = ['hora', 'acessos']
    res_grafico_treze = grafico_treze.acessos.count() - res_grafico_doze - res_grafico_onze - res_grafico_dez - res_grafico_nove - res_grafico_oito - res_grafico_sete - res_grafico_seis

    #Gráfico de acessos entre 14:00 e 14:59
    grafico_quatorze = logs.datas.loc[(logs.datas.index<35404)].value_counts().reset_index()
    grafico_quatorze.columns = ['hora', 'acessos']
    res_grafico_quatorze = grafico_quatorze.acessos.count()  - res_grafico_treze - res_grafico_doze - res_grafico_onze - res_grafico_dez - res_grafico_nove - res_grafico_oito - res_grafico_sete - res_grafico_seis

    #Gráfico de acessos entre 15:00 e 15:59
    grafico_quinze = logs.datas.loc[(logs.datas.index<39149)].value_counts().reset_index()
    grafico_quinze.columns = ['hora', 'acessos']
    res_grafico_quinze = grafico_quinze.acessos.count() - res_grafico_quatorze - res_grafico_treze - res_grafico_doze - res_grafico_onze - res_grafico_dez - res_grafico_nove - res_grafico_oito - res_grafico_sete - res_grafico_seis

    #Gráfico de acessos entre 16:00 e 16:59
    grafico_dezesseis = logs.datas.loc[(logs.datas.index<42887)].value_counts().reset_index()
    grafico_dezesseis.columns = ['hora', 'acessos']
    res_grafico_dezesseis = grafico_dezesseis.acessos.count() - res_grafico_quinze - res_grafico_quatorze - res_grafico_treze - res_grafico_doze - res_grafico_onze - res_grafico_dez - res_grafico_nove - res_grafico_oito - res_grafico_sete - res_grafico_seis

    #Gráfico de acessos entre 17:00 e 17:59
    grafico_dezessete = logs.datas.loc[(logs.datas.index<47021)].value_counts().reset_index()
    grafico_dezessete.columns = ['hora', 'acessos']
    res_grafico_dezessete = grafico_dezessete.acessos.count() - res_grafico_dezesseis - res_grafico_quinze - res_grafico_quatorze - res_grafico_treze - res_grafico_doze - res_grafico_onze - res_grafico_dez - res_grafico_nove - res_grafico_oito - res_grafico_sete - res_grafico_seis

    #Gráfico de acessos entre 18:00 e 18:59
    grafico_dezoito = logs.datas.loc[(logs.datas.index<50219)].value_counts().reset_index()
    grafico_dezoito.columns = ['hora', 'acessos']
    res_grafico_dezoito = grafico_dezoito.acessos.count()  - res_grafico_dezessete - res_grafico_dezesseis - res_grafico_quinze - res_grafico_quatorze - res_grafico_treze - res_grafico_doze - res_grafico_onze - res_grafico_dez - res_grafico_nove  - res_grafico_oito - res_grafico_sete - res_grafico_seis

    #Gráfico de acessos entre 19:00 e 19:59
    grafico_dezenove = logs.datas.loc[(logs.datas.index<54423)].value_counts().reset_index()
    grafico_dezenove.columns = ['hora', 'acessos']
    res_grafico_dezenove = grafico_dezenove.acessos.count() - res_grafico_dezoito - res_grafico_dezessete - res_grafico_dezesseis - res_grafico_quinze - res_grafico_quatorze - res_grafico_treze - res_grafico_doze - res_grafico_onze - res_grafico_dez - res_grafico_nove  - res_grafico_oito - res_grafico_sete - res_grafico_seis

    #Gráfico de acessos entre 20:00 e 20:59
    grafico_vinte = logs.datas.loc[(logs.datas.index<59770)].value_counts().reset_index()
    grafico_vinte.columns = ['hora', 'acessos']
    res_grafico_vinte = grafico_vinte.acessos.count() - res_grafico_dezenove - res_grafico_dezoito - res_grafico_dezessete - res_grafico_dezesseis - res_grafico_quinze - res_grafico_quatorze - res_grafico_treze - res_grafico_doze - res_grafico_onze - res_grafico_dez - res_grafico_nove  - res_grafico_oito - res_grafico_sete - res_grafico_seis

    #Gráfico de acessos entre 21:00 e 21:59
    grafico_vinte_um = logs.datas.loc[(logs.datas.index<62883)].value_counts().reset_index()
    grafico_vinte_um.columns = ['hora', 'acessos']
    res_grafico_vinte_um = grafico_vinte_um.acessos.count() - res_grafico_vinte - res_grafico_dezenove - res_grafico_dezoito - res_grafico_dezessete - res_grafico_dezesseis - res_grafico_quinze - res_grafico_quatorze - res_grafico_treze - res_grafico_doze - res_grafico_onze - res_grafico_dez - res_grafico_nove  - res_grafico_oito - res_grafico_sete - res_grafico_seis

    #Gráfico de acessos entre 22:00 e 22:59
    grafico_vinte_dois = logs.datas.loc[(logs.datas.index<64619)].value_counts().reset_index()
    grafico_vinte_dois.columns = ['hora', 'acessos']
    res_grafico_vinte_dois = grafico_vinte_dois.acessos.count() - res_grafico_vinte_um - res_grafico_vinte - res_grafico_dezenove - res_grafico_dezoito - res_grafico_dezessete - res_grafico_dezesseis - res_grafico_quinze - res_grafico_quatorze - res_grafico_treze - res_grafico_doze - res_grafico_onze - res_grafico_dez - res_grafico_nove  - res_grafico_oito - res_grafico_sete - res_grafico_seis

    #Gráfico de acessos entre 22:00 e 23:59
    grafico_vinte_tres = logs.datas.loc[(logs.datas.index<65404)].value_counts().reset_index()
    grafico_vinte_tres.columns = ['hora', 'acessos']
    res_grafico_vinte_tres = grafico_vinte_tres.acessos.count() - res_grafico_vinte_dois - res_grafico_vinte_um - res_grafico_vinte - res_grafico_dezenove - res_grafico_dezoito - res_grafico_dezessete - res_grafico_dezesseis - res_grafico_quinze - res_grafico_quatorze - res_grafico_treze - res_grafico_doze - res_grafico_onze - res_grafico_dez - res_grafico_nove  - res_grafico_oito - res_grafico_sete - res_grafico_seis

    x = np.array(['6:25 e 6:59','7:00 e 7:59','8:00 e 8:59','9:00 e 9:59','10:00 e 10:59','11:00 e 11:59','12:00 e 12:59','13:00 e 13:59','14:00 e 14:59','15:00 e 15:59','16:00 e 16:59','17:00 e 17:59',
    '18:00 e 18:59','19:00 e 19:59','20:00 e 20:59','21:00 e 21:59','22:00 e 22:59','23:00 e 23:59'])
    y = np.array([res_grafico_seis, res_grafico_sete, res_grafico_oito, res_grafico_nove, res_grafico_dez, res_grafico_onze, res_grafico_doze, res_grafico_treze, res_grafico_quatorze, res_grafico_quinze, 
    res_grafico_dezesseis, res_grafico_dezessete,res_grafico_dezoito, res_grafico_dezenove, res_grafico_vinte, res_grafico_vinte_um, res_grafico_vinte_dois, res_grafico_vinte_tres])

    plt.figure(figsize=(40,7))
    plt.xticks(rotation=45)
    plt.title('Acessos dia 18/3')
    plt.plot(x, y, '-o')

    #status code
    status = logs.status_code.value_counts().to_frame().reset_index()
    status.columns = ['Code', 'Frequencia']
    print(status.astype(int))
    plt.figure(figsize=(10,10))
    plt.title('Status Code')
    sns.barplot(x=status['Code'].astype(int), y=status['Frequencia'] , hue=status.Code.astype(int))
