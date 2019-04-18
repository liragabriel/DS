import pandas as pd
import numpy as np

operacao = pd.read_csv('websvc_error1.csv')

def filtar_fsan():

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

    #Remove valores repetidos ou com
    fsan = []
    for x in range(len(lista_fsan)):
        if lista_fsan[x] not in fsan and lista_fsan[x]+':' not in fsan:
            fsan.append(lista_fsan[x])
    for x in range(len(fsan)):
        if ':' in fsan[x]:
            del(fsan[x])
