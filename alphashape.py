import numpy as np
from scipy.spatial import Delaunay
from area_of_polygon import area_of_polygon_crd
import networkx as nx
#pip3 install networkx

def sqrt_sum(a, b):
#Parametros:
#       a   -> ponto incial
#       b   -> ponto final 
#Retorno:
#       ret -> distancia entre o ponto incial e o ponto final
    x = (a[0]-b[0])
    y = (a[1]-b[1])
    ret = np.sqrt(x*x+y*y)
    return ret

def shapeToSomePolygons(shape):
#Parametros:
#       shape -> vetor de segmentos 
#Retorno:
#       ret   -> poligono definido com uma vetor de segmentos
    G = nx.Graph()
    allnodes = set()
    for line in shape:
        G.add_nodes_from(line)
        G.add_edge(line[0], line[1])
        allnodes.add(line[0])
        allnodes.add(line[1])

    result = []

    while allnodes:
        node = allnodes.pop()
        new_node = next(iter(G[node]), None)
        if not new_node: continue

        G.remove_edge(node, new_node)
        temp = nx.shortest_path(G, node, new_node)
        for j,t in enumerate(temp):
            if t in allnodes:
                allnodes.remove(t)

        result.append(temp)
        #print(result)
    return result

def getAlfaShapes(pts,alfas=1): 
#Parametros:
#       pts   -> vetor de coordenadas de pontos em uma imagem
#       alfas -> constante ou  vetor de constantes que representa o raio de uma circunferencia para selação de retas candidatas a forma Alpha 
#Retorno:
#       rez   -> vetor de segmentos da forma Alpha

    tri_ind = [(0,1),(1,2),(2,0)] #triangulo incial
    tri = Delaunay(pts) #triangulação dos pontos de borda pelo metodo Delaunay
    lenghts={}
    for s in tri.simplices:
        for ind in tri_ind:
            a = pts[s[ind[0]]]
            b = pts[s[ind[1]]]
            line = (a, b) #Define seguimento de reta do ponto A para o B
            lenghts[line] = sqrt_sum(a, b) #Usa a medida de distancia euclidiana para saber o comprimento das retas

    ls = sorted(lenghts.values()) #Oredena os valores de comprimentos de reta

    mean_length = np.mean(ls) #Obtem o valor medio das retas ordenadas
    mean_length_index = ls.index(next(filter(lambda x: x>=mean_length, ls))) #indexação de todos os as retas definidas
    magic_numbers = [ls[i] for i in range(mean_length_index, len(ls))]  #Define uma listas com os valores medio pro fim da lista de tamanhos de retas indexados
    magic_numbers[0] = 0  #O o primeiro valor da lista é atribuido ZERO
    sum_magic = np.sum(magic_numbers) #Somatorio de numerios magicos
    for i in range(2, len(magic_numbers)):
        magic_numbers[i] += magic_numbers[i-1]
    magic_numbers = [m /sum_magic for m in magic_numbers]

    rez = []
    for alfa in alfas:
        i = magic_numbers.index(next(filter(lambda z: z > alfa, magic_numbers), magic_numbers[-1]))
        av_length = ls[mean_length_index+i]

        lines = {}

        for s in tri.simplices:
            used = True
            for ind in tri_ind:
                if lenghts[(pts[s[ind[0]]], pts[s[ind[1]]])] > av_length:
                    used = False
                    break
            if used == False: continue

            for ind in tri_ind:
                i,j= s[ind[0]],s[ind[1]]
                line = (pts[min(i,j)], pts[max(i,j)])
                lines[line] = line in lines

        good_lines = []
        for v in lines:
            if not lines[v]:
                good_lines.append(v)

        result = shapeToSomePolygons(good_lines) # Define o poligono com os melhores seguimentos triangulados
        result.sort(key=area_of_polygon_crd, reverse=True)  #Ordena vetor de seguimentos

        new_list = []
        for i in range(len(result)):  
            new_list += result[i]
            #result[i] = str(result[i][0]) + ',' + str(result[i][1])

        rez_list = []
        for i in range(len(new_list)):
            rez_list.append(new_list[i][0])
            rez_list.append(new_list[i][1])

        #print(rez_list)
        rez.append(result)
        #print(result)

    return rez_list  