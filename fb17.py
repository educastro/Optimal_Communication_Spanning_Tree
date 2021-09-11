import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import itertools
from datetime import datetime

def expandir(G, nos_explorados, arestas_exploradas):
    nos_fronteira = list()
    vetices_fronteira = list()
    for v in nos_explorados:
        for u in nx.neighbors(G,v):
            if not (u in nos_explorados):
                nos_fronteira.append(u)
                vetices_fronteira.append([(u,v,G[u][v]['weight']), (v,u,G[v][u]['weight'])])
    return zip([nos_explorados | frozenset([v]) for v in nos_fronteira], [arestas_exploradas | frozenset(e) for e in vetices_fronteira])

def gerar_arvores_geradoras(G, root=0):
    nos_explorados = frozenset([root])
    arestas_exploradas = frozenset([])
    solucoes = [(nos_explorados, arestas_exploradas)]
    for ii in range(G.number_of_nodes()-1):
        solucoes = [expandir(G, nos, arestas) for (nos, arestas) in solucoes]
        solucoes = set([item for sublist in solucoes for item in sublist])
    lg = []
    for nos, arestas in solucoes:
        g1= nx.Graph()
        g1.add_weighted_edges_from(arestas,weight='weight')
        lg.append(g1) 
    return lg     

def apresentar_arvore(arvore, indice, grafo_req, combinacoes):
    print('Arestas: ', arvore.edges)
    custo_arvore = 0 
    for x in combinacoes:
        print('Vértices: ',x[0],x[1])
        print('Caminho: ',nx.shortest_path(arvore, source=x[0], target=x[1], weight='weight', method='dijkstra'))
        distancia= nx.shortest_path_length(arvore, source=x[0], target=x[1], weight='weight', method='dijkstra')
        print('Tamanho do Caminho: ',distancia)
        try:
            custo_com = grafo_req[x[0]][x[1]] * distancia
        except:
            custo_com=0
        print('Custo do Caminho: ',custo_com)
        custo_arvore+=custo_com
    
    
def obter_arvore_menor_custo_comunicacao(grafo,grafo_req):
    G = nx.Graph()
    for x in grafo:
        for y in grafo[x]:
            G.add_edge(x,y,weight=grafo[x][y])
    combinacoes = list(itertools.combinations(G.nodes(), r=2))#
    ST = gerar_arvores_geradoras(G)
    print(len(ST))
    indice=0
    ind_menor_arvore=0
    custo_com=0
    custo_total=0
    custo_menor_arvore=1000000000
    for g in ST:
        indice= ST.index(g)
        custo_arvore = 0 
        for x in combinacoes:
            distancia= nx.shortest_path_length(g, source=x[0], target=x[1], weight='weight', method='dijkstra')
            try:
                custo_com = grafo_req[x[0]][x[1]] * distancia
            except:
                custo_com=0
            custo_arvore+=custo_com
        if custo_menor_arvore > custo_arvore:
            custo_menor_arvore = custo_arvore
            ind_menor_arvore= indice

    ##### Arvore de Custo Mínimo #########
#    print('A árvore de indice: ', ind_menor_arvore, ' tem custo: ',custo_menor_arvore)         
#    apresentar_arvore(ST[ind_menor_arvore],ind_menor_arvore,grafo_req, combinacoes)
    


'''
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
'''
grafo= {0: {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5}, 1: {0: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5}, 2: {0: 5, 1: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5}, 3: {0: 5, 1: 5, 2: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5}, 4: {0: 5, 1: 5, 2: 5, 3: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5}, 5: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 6: 5, 7: 5, 8: 5, 9: 5}, 6: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 7: 5, 8: 5, 9: 5}, 7: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 8: 5, 9: 5}, 8: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 9: 5}, 9: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}}
grafo_req = {0: {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5}, 1: {0: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5}, 2: {0: 5, 1: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5}, 3: {0: 5, 1: 5, 2: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5}, 4: {0: 5, 1: 5, 2: 5, 3: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5}, 5: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 6: 5, 7: 5, 8: 5, 9: 5}, 6: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 7: 5, 8: 5, 9: 5}, 7: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 8: 5, 9: 5}, 8: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 9: 5}, 9: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}}
'''

#grafo= {0: {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5, 11: 5, 12: 5, 13: 5, 14: 5}, 1: {0: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5, 11: 5, 12: 5, 13: 5, 14: 5}, 2: {0: 5, 1: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5, 11: 5, 12: 5, 13: 5, 14: 5}, 3: {0: 5, 1: 5, 2: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5, 11: 5, 12: 5, 13: 5, 14: 5}, 4: {0: 5, 1: 5, 2: 5, 3: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5, 11: 5, 12: 5, 13: 5, 14: 5}, 5: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5, 11: 5, 12: 5, 13: 5, 14: 5}, 6: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 7: 5, 8: 5, 9: 5, 10: 5, 11: 5, 12: 5, 13: 5, 14: 5}, 7: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 8: 5, 9: 5, 10: 5, 11: 5, 12: 5, 13: 5, 14: 5}, 8: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 9: 5, 10: 5, 11: 5, 12: 5, 13: 5, 14: 5}, 9: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 10: 5, 11: 5, 12: 5, 13: 5, 14: 5}, 10: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 11: 5, 12: 5, 13: 5, 14: 5}, 11: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5, 12: 5, 13: 5, 14: 5}, 12: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5, 11: 5, 13: 5, 14: 5}, 13: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5, 11: 5, 12: 5, 14: 5}, 14: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5, 11: 5, 12: 5, 13: 5}}
#grafo_req = {0: {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5, 11: 5, 12: 5, 13: 5, 14: 5}, 1: {0: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5, 11: 5, 12: 5, 13: 5, 14: 5}, 2: {0: 5, 1: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5, 11: 5, 12: 5, 13: 5, 14: 5}, 3: {0: 5, 1: 5, 2: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5, 11: 5, 12: 5, 13: 5, 14: 5}, 4: {0: 5, 1: 5, 2: 5, 3: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5, 11: 5, 12: 5, 13: 5, 14: 5}, 5: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5, 11: 5, 12: 5, 13: 5, 14: 5}, 6: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 7: 5, 8: 5, 9: 5, 10: 5, 11: 5, 12: 5, 13: 5, 14: 5}, 7: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 8: 5, 9: 5, 10: 5, 11: 5, 12: 5, 13: 5, 14: 5}, 8: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 9: 5, 10: 5, 11: 5, 12: 5, 13: 5, 14: 5}, 9: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 10: 5, 11: 5, 12: 5, 13: 5, 14: 5}, 10: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 11: 5, 12: 5, 13: 5, 14: 5}, 11: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5, 12: 5, 13: 5, 14: 5}, 12: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5, 11: 5, 13: 5, 14: 5}, 13: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5, 11: 5, 12: 5, 14: 5}, 14: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5, 11: 5, 12: 5, 13: 5}}

grafo= {0: {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}, 1: {0: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}, 2: {0: 5, 1: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}, 3: {0: 5, 1: 5, 2: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}, 4: {0: 5, 1: 5, 2: 5, 3: 5, 5: 5, 6: 5, 7: 5, 8: 5}, 5: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 6: 5, 7: 5, 8: 5}, 6: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 7: 5, 8: 5}, 7: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 8: 5}, 8: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5}}
grafo_req = {0: {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}, 1: {0: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}, 2: {0: 5, 1: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}, 3: {0: 5, 1: 5, 2: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}, 4: {0: 5, 1: 5, 2: 5, 3: 5, 5: 5, 6: 5, 7: 5, 8: 5}, 5: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 6: 5, 7: 5, 8: 5}, 6: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 7: 5, 8: 5}, 7: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 8: 5}, 8: {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5}}

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

a =datetime.now()
obter_arvore_menor_custo_comunicacao(grafo,grafo_req)
print(datetime.now()-a)



