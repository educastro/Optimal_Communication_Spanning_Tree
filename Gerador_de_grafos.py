'''
Código desenvolvido enquanto implementação do artigo "O problema da árvore de abrangência de comunicação ideal (Optimum Communication Spanning Tree) e suas diferentes soluções" submetido no WPOS 2021.
Todos os autores possuem vínculo com o Programa de Pós-Graduação em Computação Aplicada da Universidade de Brasília, sendo os seguintes:
- Eduardo Castro
- Flávio Martins
- Leonardo Oliveira
- Ilo César
- Edison Ishikawa
O código a seguir tem como objetivo principal a geração de grafos.
'''
n=0
g={}
# Coleta de input contendo a quantidade de nós desejados
n=int(input())
# For para geração do grafo
for x in range(n):
    g[x]={}
    for y in range(n):
        if y!= x:
            # Definição do valor para cada conexão entre nós
            g[x][y] = 5
print('grafo=',g)
print('grafo_req =',g)


'''
n=0
g={}
n=int(input())
for x in range(n-1):
    g[x]={}
    g[x][x+1] = 5
g[x+1]={}
g[x+1][0] = 5
print('grafo=',g)
print('grafo_req =',g)
'''
