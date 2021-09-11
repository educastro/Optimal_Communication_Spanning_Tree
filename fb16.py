'''
Código desenvolvido enquanto implementação do artigo "O problema da árvore de abrangência de comunicação ideal (Optimum Communication Spanning Tree) e suas diferentes soluções" submetido no WPOS 2021.
Todos os autores possuem vínculo com o Programa de Pós-Graduação em Computação Aplicada da Universidade de Brasília, sendo os seguintes:
- Eduardo Castro
- Flávio Martins
- Leonardo Oliveira
- Ilo César
- Edison Ishikawa
O código a seguir tem como objetivo principal a geração de grafos e árvores de abrangência mínima para que seja calculada a árvore de abrangência de comunicação ótima conforme estabelecido por Hu (1974).
'''

# Importação das bibliotecas utilizadas pelo projeto
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import itertools
from datetime import datetime

# Função utilizada de forma recursiva com o objetivo de expandir todos os nós de um dado Grafo.
# Para tanto, é informado o Grafo, uma lista contendo todos os nós que já foram explorados e uma outra lista contendo as arestas que já foram exploradas.
# Desta forma, percorre-se todos nós sejam visitados.
def expandir(G, nos_explorados, arestas_exploradas):
    # Lista para que sejam armazenados os nós que ainda não foram visitados
    nos_fronteira = list()
    # Lista para que sejam armazenados os vértices que ainda não foram visitados
    vetices_fronteira = list()
    # aqui percorremos todos os nós que já foram explorados para que todos os seus vizinhos sejam verificados.
    for v in nos_explorados:
        # Função da biblioteca networkx que faz com que a tarefa de explorar grafos seja simplicada, em suma esta função percorre todos os vizinhos de um dado nó.
        for u in nx.neighbors(G,v):
            # Se o nó percorrido não fizer parte da lista que indica os nós que já foram visitados, os adicionamos na lista fronteira para qe sejam tratados e visitados posteriormente.
            if not (u in nos_explorados):
                nos_fronteira.append(u)
                vetices_fronteira.append([(u,v,G[u][v]['weight']), (v,u,G[v][u]['weight'])])
    # Retorna um objeto do tipo zip que consiste em um iterador de tuplas
    # Frozenset é apenas uma versão imutável do objeto set, trabalhar com este tipo de dado permite que seus objetos sejam utilizados enquanto chaves em dicionários ou em outros objetos do tipo set.
    return zip([nos_explorados | frozenset([v]) for v in nos_fronteira], [arestas_exploradas | frozenset(e) for e in vetices_fronteira])

# Função utilizada para gerar as diversas árvores possíveis
def gerar_arvores_geradoras(G, root=0):
    # Frozenset é apenas uma versão imutável do objeto set, trabalhar com este tipo de dado permite que seus objetos sejam utilizados enquanto chaves em dicionários ou em outros objetos do tipo set.
    nos_explorados = frozenset([root])
    arestas_exploradas = frozenset([])
    # Variável para armazenar os nós e arestas explorados
    solucoes = [(nos_explorados, arestas_exploradas)]
    # Aqui começamos a percorrer o grafo
    for ii in range(G.number_of_nodes()-1):
        # A função expandir é chamada para cada elemento de solucoes
        solucoes = [expandir(G, nos, arestas) for (nos, arestas) in solucoes]
        solucoes = set([item for sublist in solucoes for item in sublist])
    lg = []
    # Aqui se adiciona os pesos (distância) das árvores
    for nos, arestas in solucoes:
        g1= nx.Graph()
        g1.add_weighted_edges_from(arestas,weight='weight')
        lg.append(g1)
    # Retorna-se o grafo completo
    return lg

# Função feita exclusivamente para apresentar a árvore gerada e o resultado obtido
def apresentar_arvore(arvore, indice, grafo_req, combinacoes):
    print('Arestas: ', arvore.edges)
    custo_arvore = 0
    # Segue a rotina para cada uma das n combinações
    for x in combinacoes:
        # Imprime quantidade de versos
        print('Vértices: ',x[0],x[1])
        # Imprime os menores caminhos possíveis
        print('Caminho: ',nx.shortest_path(arvore, source=x[0], target=x[1], weight='weight', method='dijkstra'))
        distancia= nx.shortest_path_length(arvore, source=x[0], target=x[1], weight='weight', method='dijkstra')
        # Imprime a distância do caminho
        print('Tamanho do Caminho: ',distancia)
        # Aqui calcula-se o custo multiplicando o requisito pela distância
        try:
            custo_com = grafo_req[x[0]][x[1]] * distancia
        except:
            custo_com=0
        # Imprime o custo
        print('Custo do Caminho: ',custo_com)

        custo_arvore+=custo_com

# Função para que possamos obter a árvore com o menor custo de comunicação dado o grafo gerado com os pesos das distâncias e o novo input de dados que engloba os requisitos.
def obter_arvore_menor_custo_comunicacao(grafo,grafo_req):
    # É gerado o grafo que irá receber os dados
    G = nx.Graph()
    # Para cada elemento do grafo passado como parâmetro
    for x in grafo:
        # Para cada peso do grafo passado como parâmetro
        for y in grafo[x]:
            # Cria se um vértice equivalente
            G.add_edge(x,y,weight=grafo[x][y])
    # Gera-se uma lista com todas as combinações possíveis
    combinacoes = list(itertools.combinations(G.nodes(), r=2))#
    # Gera-se todas as árvores mínimas possíveis
    ST = gerar_arvores_geradoras(G)
    print(len(ST))
    indice=0
    ind_menor_arvore=0
    custo_com=0
    custo_total=0
    custo_menor_arvore=1000000000
    # Para cada árvores
    for g in ST:
        indice= ST.index(g)
        custo_arvore = 0
        # Para cada combinação
        for x in combinacoes:
            distancia= nx.shortest_path_length(g, source=x[0], target=x[1], weight='weight', method='dijkstra')
            try:
                custo_com = grafo_req[x[0]][x[1]] * distancia
            except:
                custo_com=0
            custo_arvore+=custo_com
        # Teste para obter a árvore com menor custo
        if custo_menor_arvore > custo_arvore:
            custo_menor_arvore = custo_arvore
            ind_menor_arvore= indice

    ##### Arvore de Custo Mínimo #########
#    print('A árvore de indice: ', ind_menor_arvore, ' tem custo: ',custo_menor_arvore)
#    apresentar_arvore(ST[ind_menor_arvore],ind_menor_arvore,grafo_req, combinacoes)



'''
Entradas:

grafo = {0: {1: 5, 2: 6, 3: 1}, 1: {0: 5, 2: 4, 3: 7},
        2: {0: 6, 1: 4, 3: 4}, 3: {0: 1, 1: 7, 2: 4}}

grafo_req = {0: {1: 1}, 1: {0: 1, 2: 1},
        2: {1: 1, 3: 1}, 3: {2: 1}}
'''

'''
grafo = {0: {1: 2, 5: 2}, 1: {0: 2, 2: 3, 4: 3, 5: 2},
             2: {1: 3, 3: 3, 4: 3, 5: 3},
             3: {2: 3, 4: 3},
             4: {1: 3, 2: 3, 3: 3, 5: 4},
             5: {0: 2, 1: 2, 2: 3, 4: 4 }}

grafo_req = {0: {1: 10, 5: 8},
                 1: {0: 10, 2: 4, 4: 2, 5: 3},
                 2: {1: 4, 3: 5, 4: 4, 5: 0},
                 3: {2: 5, 4: 7, 5: 2},
                 4: {1: 2, 2: 4, 3: 7, 5: 3},
                 5: {0: 8, 1: 3, 2: 0, 3: 2, 4: 3}}
'''
'''
grafo = {0: {1: 2, 5: 2}, 1: {0: 2, 2: 3, 4: 3, 5: 2},
             2: {1: 3, 3: 3, 4: 3, 5: 3},
             3: {2: 3, 4: 3},
             4: {1: 3, 2: 3, 3: 3, 5: 4},
             5: {0: 2, 1: 2, 2: 3, 4: 4 }}

grafo_req = {0: {1: 10, 5: 8},
                 1: {0: 10, 2: 4, 4: 2, 5: 3},
                 2: {1: 4, 3: 5, 4: 4, 5: 0},
                 3: {2: 5, 4: 7, 5: 2},
                 4: {1: 2, 2: 4, 3: 7, 5: 3},
                 5: {0: 8, 1: 3, 2: 0, 3: 2, 4: 3}}
'''
'''

grafo = {0: {1: 1, 2: 1, 3: 1, 4:1}, 1: {0: 1, 2: 1, 3: 1, 4: 1},
        2: {0: 1, 1: 1, 3: 1, 4: 1}, 3: {0: 1, 1: 1, 2: 1, 4: 1},
        4: {0: 1, 1: 1, 2: 1, 3: 1}}

grafo_req = {0: {1: 1, 2: 1, 3: 1, 4:1}, 1: {0: 1, 2: 1, 3: 1, 4: 1},
        2: {0: 1, 1: 1, 3: 1, 4: 1}, 3: {0: 1, 1: 1, 2: 1, 4: 1},
        4: {0: 1, 1: 1, 2: 1, 3: 1}}
'''
'''
grafo= {0: {1: 5}, 1: {2: 5}, 2: {3: 5}, 3: {4: 5}, 4: {5: 5}, 5: {6: 5}, 6: {7: 5}, 7: {8: 5}, 8: {9: 5}, 9: {0: 5}}
grafo_req= {0: {1: 5}, 1: {2: 5}, 2: {3: 5}, 3: {4: 5}, 4: {5: 5}, 5: {6: 5}, 6: {7: 5}, 7: {8: 5}, 8: {9: 5}, 9: {0: 5}}
'''
'''
grafo= {0: {1: 5}, 1: {2: 5}, 2: {3: 5}, 3: {4: 5}, 4: {5: 5}, 5: {6: 5}, 6: {7: 5}, 7: {8: 5}, 8: {9: 5}, 9: {10: 5}, 10: {11: 5}, 11: {12: 5}, 12: {13: 5}, 13: {14: 5}, 14: {15: 5}, 15: {16: 5}, 16: {17: 5}, 17: {18: 5}, 18: {19: 5}, 19: {0: 5}}
grafo_req = {0: {1: 5}, 1: {2: 5}, 2: {3: 5}, 3: {4: 5}, 4: {5: 5}, 5: {6: 5}, 6: {7: 5}, 7: {8: 5}, 8: {9: 5}, 9: {10: 5}, 10: {11: 5}, 11: {12: 5}, 12: {13: 5}, 13: {14: 5}, 14: {15: 5}, 15: {16: 5}, 16: {17: 5}, 17: {18: 5}, 18: {19: 5}, 19: {0: 5}}
'''
'''
grafo= {0: {1: 5}, 1: {2: 5}, 2: {3: 5}, 3: {4: 5}, 4: {5: 5}, 5: {6: 5}, 6: {7: 5}, 7: {8: 5}, 8: {9: 5}, 9: {10: 5}, 10: {11: 5}, 11: {12: 5}, 12: {13: 5}, 13: {14: 5}, 14: {15: 5}, 15: {16: 5}, 16: {17: 5}, 17: {18: 5}, 18: {19: 5}, 19: {20: 5}, 20: {21: 5}, 21: {22: 5}, 22: {23: 5}, 23: {24: 5}, 24: {25: 5}, 25: {26: 5}, 26: {27: 5}, 27: {28: 5}, 28: {29: 5}, 29: {0: 5}}
grafo_req = {0: {1: 5}, 1: {2: 5}, 2: {3: 5}, 3: {4: 5}, 4: {5: 5}, 5: {6: 5}, 6: {7: 5}, 7: {8: 5}, 8: {9: 5}, 9: {10: 5}, 10: {11: 5}, 11: {12: 5}, 12: {13: 5}, 13: {14: 5}, 14: {15: 5}, 15: {16: 5}, 16: {17: 5}, 17: {18: 5}, 18: {19: 5}, 19: {20: 5}, 20: {21: 5}, 21: {22: 5}, 22: {23: 5}, 23: {24: 5}, 24: {25: 5}, 25: {26: 5}, 26: {27: 5}, 27: {28: 5}, 28: {29: 5}, 29: {0: 5}}
'''
'''
grafo= {0: {1: 5}, 1: {2: 5}, 2: {3: 5}, 3: {4: 5}, 4: {5: 5}, 5: {6: 5}, 6: {7: 5}, 7: {8: 5}, 8: {9: 5}, 9: {10: 5}, 10: {11: 5}, 11: {12: 5}, 12: {13: 5}, 13: {14: 5}, 14: {15: 5}, 15: {16: 5}, 16: {17: 5}, 17: {18: 5}, 18: {19: 5}, 19: {20: 5}, 20: {21: 5}, 21: {22: 5}, 22: {23: 5}, 23: {24: 5}, 24: {25: 5}, 25: {26: 5}, 26: {27: 5}, 27: {28: 5}, 28: {29: 5}, 29: {30: 5}, 30: {31: 5}, 31: {32: 5}, 32: {33: 5}, 33: {34: 5}, 34: {35: 5}, 35: {36: 5}, 36: {37: 5}, 37: {38: 5}, 38: {39: 5}, 39: {0: 5}}
grafo_req = {0: {1: 5}, 1: {2: 5}, 2: {3: 5}, 3: {4: 5}, 4: {5: 5}, 5: {6: 5}, 6: {7: 5}, 7: {8: 5}, 8: {9: 5}, 9: {10: 5}, 10: {11: 5}, 11: {12: 5}, 12: {13: 5}, 13: {14: 5}, 14: {15: 5}, 15: {16: 5}, 16: {17: 5}, 17: {18: 5}, 18: {19: 5}, 19: {20: 5}, 20: {21: 5}, 21: {22: 5}, 22: {23: 5}, 23: {24: 5}, 24: {25: 5}, 25: {26: 5}, 26: {27: 5}, 27: {28: 5}, 28: {29: 5}, 29: {30: 5}, 30: {31: 5}, 31: {32: 5}, 32: {33: 5}, 33: {34: 5}, 34: {35: 5}, 35: {36: 5}, 36: {37: 5}, 37: {38: 5}, 38: {39: 5}, 39: {0: 5}}
'''
'''
grafo={0: {1: 5}, 1: {2: 5}, 2: {3: 5}, 3: {4: 5}, 4: {5: 5}, 5: {6: 5}, 6: {7: 5}, 7: {8: 5}, 8: {9: 5}, 9: {10: 5}, 10: {11: 5}, 11: {12: 5}, 12: {13: 5}, 13: {14: 5}, 14: {15: 5}, 15: {16: 5}, 16: {17: 5}, 17: {18: 5}, 18: {19: 5}, 19: {20: 5}, 20: {21: 5}, 21: {22: 5}, 22: {23: 5}, 23: {24: 5}, 24: {25: 5}, 25: {26: 5}, 26: {27: 5}, 27: {28: 5}, 28: {29: 5}, 29: {30: 5}, 30: {31: 5}, 31: {32: 5}, 32: {33: 5}, 33: {34: 5}, 34: {35: 5}, 35: {36: 5}, 36: {37: 5}, 37: {38: 5}, 38: {39: 5}, 39: {40: 5}, 40: {41: 5}, 41: {42: 5}, 42: {43: 5}, 43: {44: 5}, 44: {45: 5}, 45: {46: 5}, 46: {47: 5}, 47: {48: 5}, 48: {49: 5}, 49: {50: 5}, 50: {51: 5}, 51: {52: 5}, 52: {53: 5}, 53: {54: 5}, 54: {55: 5}, 55: {56: 5}, 56: {57: 5}, 57: {58: 5}, 58: {59: 5}, 59: {60: 5}, 60: {61: 5}, 61: {62: 5}, 62: {63: 5}, 63: {64: 5}, 64: {65: 5}, 65: {66: 5}, 66: {67: 5}, 67: {68: 5}, 68: {69: 5}, 69: {70: 5}, 70: {71: 5}, 71: {72: 5}, 72: {73: 5}, 73: {74: 5}, 74: {75: 5}, 75: {76: 5}, 76: {77: 5}, 77: {78: 5}, 78: {79: 5}, 79: {80: 5}, 80: {81: 5}, 81: {82: 5}, 82: {83: 5}, 83: {84: 5}, 84: {85: 5}, 85: {86: 5}, 86: {87: 5}, 87: {88: 5}, 88: {89: 5}, 89: {90: 5}, 90: {91: 5}, 91: {92: 5}, 92: {93: 5}, 93: {94: 5}, 94: {95: 5}, 95: {96: 5}, 96: {97: 5}, 97: {98: 5}, 98: {99: 5}, 99: {0: 5}}
grafo_req = {0: {1: 5}, 1: {2: 5}, 2: {3: 5}, 3: {4: 5}, 4: {5: 5}, 5: {6: 5}, 6: {7: 5}, 7: {8: 5}, 8: {9: 5}, 9: {10: 5}, 10: {11: 5}, 11: {12: 5}, 12: {13: 5}, 13: {14: 5}, 14: {15: 5}, 15: {16: 5}, 16: {17: 5}, 17: {18: 5}, 18: {19: 5}, 19: {20: 5}, 20: {21: 5}, 21: {22: 5}, 22: {23: 5}, 23: {24: 5}, 24: {25: 5}, 25: {26: 5}, 26: {27: 5}, 27: {28: 5}, 28: {29: 5}, 29: {30: 5}, 30: {31: 5}, 31: {32: 5}, 32: {33: 5}, 33: {34: 5}, 34: {35: 5}, 35: {36: 5}, 36: {37: 5}, 37: {38: 5}, 38: {39: 5}, 39: {40: 5}, 40: {41: 5}, 41: {42: 5}, 42: {43: 5}, 43: {44: 5}, 44: {45: 5}, 45: {46: 5}, 46: {47: 5}, 47: {48: 5}, 48: {49: 5}, 49: {50: 5}, 50: {51: 5}, 51: {52: 5}, 52: {53: 5}, 53: {54: 5}, 54: {55: 5}, 55: {56: 5}, 56: {57: 5}, 57: {58: 5}, 58: {59: 5}, 59: {60: 5}, 60: {61: 5}, 61: {62: 5}, 62: {63: 5}, 63: {64: 5}, 64: {65: 5}, 65: {66: 5}, 66: {67: 5}, 67: {68: 5}, 68: {69: 5}, 69: {70: 5}, 70: {71: 5}, 71: {72: 5}, 72: {73: 5}, 73: {74: 5}, 74: {75: 5}, 75: {76: 5}, 76: {77: 5}, 77: {78: 5}, 78: {79: 5}, 79: {80: 5}, 80: {81: 5}, 81: {82: 5}, 82: {83: 5}, 83: {84: 5}, 84: {85: 5}, 85: {86: 5}, 86: {87: 5}, 87: {88: 5}, 88: {89: 5}, 89: {90: 5}, 90: {91: 5}, 91: {92: 5}, 92: {93: 5}, 93: {94: 5}, 94: {95: 5}, 95: {96: 5}, 96: {97: 5}, 97: {98: 5}, 98: {99: 5}, 99: {0: 5}}

grafo= {0: {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}, 1: {0: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}, 2: {0: 5, 1: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}, 3: {0: 5, 1: 5, 2: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}, 4: {0: 5, 1: 5, 2: 5, 3: 5, 5: 5, 6: 5, 7: 5, 8: 5}, 5: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 6: 5, 7: 5, 8: 5}, 6: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 7: 5, 8: 5}, 7: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 8: 5}, 8: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5}, 9: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}}
grafo_req = {0: {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}, 1: {0: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}, 2: {0: 5, 1: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}, 3: {0: 5, 1: 5, 2: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}, 4: {0: 5, 1: 5, 2: 5, 3: 5, 5: 5, 6: 5, 7: 5, 8: 5}, 5: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 6: 5, 7: 5, 8: 5}, 6: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 7: 5, 8: 5}, 7: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 8: 5}, 8: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5}, 9: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}}
'''
grafo= {0: {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5}, 1: {0: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5}, 2: {0: 5, 1: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5}, 3: {0: 5, 1: 5, 2: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5}, 4: {0: 5, 1: 5, 2: 5, 3: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5}, 5: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 6: 5, 7: 5, 8: 5, 9: 5}, 6: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 7: 5, 8: 5, 9: 5}, 7: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 8: 5, 9: 5}, 8: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 9: 5}, 9: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}}
grafo_req = {0: {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5}, 1: {0: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5}, 2: {0: 5, 1: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5}, 3: {0: 5, 1: 5, 2: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5}, 4: {0: 5, 1: 5, 2: 5, 3: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5}, 5: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 6: 5, 7: 5, 8: 5, 9: 5}, 6: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 7: 5, 8: 5, 9: 5}, 7: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 8: 5, 9: 5}, 8: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 9: 5}, 9: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}}


'''
grafo = {}
grafo_req = {}
c={}
nd = input()
nd=int(nd)

for x in range(nd):
    c=input().split()
    if not c[0] in grafo:
        grafo[c[0]]={}
    grafo[c[0]][c[1]] = c[2]

    if not c[1] in grafo:
        grafo[c[1]]={}
    grafo[c[1]][c[0]] = c[2]

print(grafo)

for x in range(nd):
    c=input().split()
    if not c[0] in grafo_req:
        grafo_req[c[0]]={}
    grafo_req[c[0]][c[1]] = c[2]

    if not c[1] in grafo_req:
        grafo_req[c[1]]={}
    grafo_req[c[1]][c[0]] = c[2]
print(grafo_req)
'''

# Variável para que possamos medir o tempo de processamento do código
a =datetime.now()
# Função principal do código, aqui que se obtém a árvore de abrangência de comunicação mínima
obter_arvore_menor_custo_comunicacao(grafo,grafo_req)
# Reduz-se o valor do horário coletado agora com o coletado no início do código para saber quanto tempo o código levou para ser executado.
print(datetime.now()-a)
