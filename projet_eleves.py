import numpy as np
import time
from fonctionsperso import *

"""
fonction prenant en paramètre un nom de fichier 'file_name' et retournant la représentation
d'un ensemble de pages web codée dans le fichier :
- 'key_words' représente le tableau des mots-clés contenus dans les pages
- 'm_adj' représente la matrice d'adjacence du graphe formé par les liens entre les pages
"""
def get_matrix_from_file(file_name) :
    file = open(file_name,'r')
    lines = file.readlines()
    n = int(lines[0])
    key_words=[]
    m_adj=np.zeros((n,n))
    for i in range(1,n+1) :
        kws = lines[i].split()
        key_words.append(kws)
    for i in range(n+1,2*n+1) :
        l = lines[i].split()
        for j in range(1,len(l)) :
            m_adj[int(l[0]),int(l[j])] = 1
    return key_words,m_adj

"""
fonction prenant en paramètre un graphe représenté par la liste des mots clés contenus dans les pages 'k_words'
et la matrice d'adjacence 'm_adj'
"""
def affiche_graphe(k_words,m_adj) :
    for i in range(len(k_words)) :
        print("mots-clés de la page",i," :",k_words[i])
    print("matrice d'adjacence :")
    print(m_adj)

"""
fonction prenant en paramètre un tableau de liste de mots clés contenus dans les pages web 'key_words'
et une liste de mots clés recherchés 'key_words_searched'
et retournant la liste des indices des pages contenant au moins un des mots cherchés.
"""
def select_pages(key_words,key_words_searched):
    res=[]
    for i in range(0,len(key_words)):
        for j in range(0,len(key_words[i])):
            for k in range(0,len(key_words_searched)):
                if key_words[i][j] == key_words_searched[k] and i not in res:
                    res.append(i)
                    break
    return res


"""
fonction prenant en paramètre une matrice d'adjacence 'm_adj' et une liste d'indices de pages sélectionnées 'pages'
et retournant la sous-matrice d'adjacence correspondant aux liens entre les pages sélectionnées.
----------------------- VERSION TEST -------------------------------"""
"""def select_matrix(m_adj,pages) :
    """ """ligne,colonne = m_adj.shape""" """
    for i in range(0,len(pages)+1):
        if i not in pages:
            np.delete(m_adj,i,0)
            np.delete(m_adj,i,1)
        else:
            continue
    return m_adj"""

def select_matrix(m_adj,pages):
    res = m_adj
    res = res[:,pages]
    res = res[pages,:]
    return res

"""
fonction prenant en paramètre une matrice d'adjacence 'm_adj'
et retournant la matrice de transition correspondante
"""
def get_transition_matrix(m_adj) :
    m = m_adj.shape[0]
    n = m_adj.shape[1]
    temp = np.zeros((m,n))
    for i in range(0,m):
        for j in range(0,n):
            if sum(m_adj[i]!=0):
                temp[i][j] = 0.8*(m_adj[i][j]/sum(m_adj[i]))+0.2*(1/m)
            else:
                temp[i] = 1/m
    return temp

"""
fonction prenant en paramètre une matrice de transition 'm_transi' et calculant un vecteur de score r vérifiant r*mat=r
selon la méthode du premier algorithme.
"""
def page_rank1(m_transi) :
    Nm = m_transi.transpose()
    Nm = Nm - np.identity(len(m_transi))
    cct = np.ones((1,len(Nm)))
    Nm = np.concatenate((Nm,cct),axis=0)
    ym = np.zeros((len(Nm),1))
    ym[len(Nm)-1][0] = 1
    Nm,ym = Gauss(Nm,ym)
    rscore = []
    rscore = solveTriSup(Nm,ym)

    return rscore

"""
fonction prenant en paramètre une matrice de transition 'm_transi' ainsi qu'un seuil 'eps' et calculant un vecteur de score
r vérifiant r*mat=r selon la méthode du second algorithme.
------------------------------- VERSION TEST ---------------------------"""  
"""def page_rank2(m_transi,eps) :
   n = len(m_transi)
   R0 = np.array([1/n] * n)
   R1 = np.array()
   R1 = np.copy(R0)
   R1 = np.dot(R0,m_transi)
   while max(abs(R1-R0.all())) > eps:
       R0 = R1
       R1 = R0 * m_transi
   return R1"""

def page_rank2(m_transi,eps):
    R0 = []
    n = len(m_transi)
    for i in range(0,n):
        R0.append(1/n)
    R1 = R0 @ m_transi
    while((np.abs(R1-R0)).max() > eps):
        R0 = R1
        R1 = R0 @ m_transi
    return R1

"""
fonction prenant en paramètre une liste 'pages' d'indices de pages sélectionnées et un vecteur 'rank' contenant leur score
correspondant et retournant la liste des indices des pages triées dans par ordre décroissant de score.
"""
def sort_pages(pages,rank) :
    if len(pages) == len(rank) !=0 :
        ind = rank.argsort()
        res = []
        for i in ind[::-1] :
            if pages[i] not in res:
                res.append(pages[i])
        return res
    else :
        return pages

key_w,m_adj = get_matrix_from_file("example-graph4.txt")
# key_w,m_adj = get_matrix_from_file("example-graph2.txt")
# key_w,m_adj = get_matrix_from_file("example-graph3.txt")
# key_w,m_adj = get_matrix_from_file("example-graph4.txt")
affiche_graphe(key_w,m_adj)

print("\n\nRecherche de 'a' ou 'b' :\n----------------------")
pages = select_pages(key_w,['a','b'])
print("  pages sélectionnées : ",pages)
s_m_adj = select_matrix(m_adj,pages)
print("  matrice sélectionnée : \n",s_m_adj)
m_transi = get_transition_matrix(s_m_adj)
print("  matrice de transition : \n",m_transi)

print("\n>>>>>>>>>> Méthode 1 <<<<<<<<<<<")
start_time = time.time()
r = page_rank1(m_transi)
print("  rank1 trouvé : ",r)
pages_triees_1 = sort_pages(pages,r)
print("  pages indexées 1: ",pages_triees_1)
print("  --- en %s seconds ---" % (time.time() - start_time))

print("\n>>>>>>>>>> Méthode 2 <<<<<<<<<<<")

start_time = time.time()

r2 = page_rank2(m_transi,10**(-5))
print("  rank2 trouvé : ",r2)
pages_triees_2 = sort_pages(pages,r2)
print("  pages indexées 2: ",pages_triees_2)
print("  --- en %s seconds ---" % (time.time() - start_time))

print("pages indexées identiques par les méthodes ? : ",pages_triees_1==pages_triees_2)
