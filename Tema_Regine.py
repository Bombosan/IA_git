from copy import deepcopy
from ctypes import sizeof
from pydoc import doc
from random import random
import random
import numpy as np
#for debug
import time

def generateMatrix(n):
    return pozitionareRND(np.zeros((n,n)),n)
def pozitionareRND(tabla,n):
        #linieGen = random.sample(range(0,n),n)
        #colGen = random.sample(range(0,n),n)

        for i in range(0,n):            
            generat = False
            while(not generat):
                linieGen = random.randint(0,n-1)
                colGen = random.randint(0,n-1)
                if(tabla[linieGen][colGen] == 0):
                    generat = True
                    tabla[linieGen][colGen] = 1
                

        return tabla
def LineCountQueen(tablaSah,i,n):
    nr = 0
    for j in range(n):
        if(tablaSah[i][j] == 1):
            nr=nr+1
    return nr
def ColumnCountQueen(tablaSah,j,n):
    nr = 0
    for i in range(n):
        if(tablaSah[i][j] == 1):
            nr=nr+1
    return nr

def Diag1CountQueen(tablaSah,i,j):
    #print("diagonala: " + str(np.trace(tablaSah,j+i)))
    #print(tablaSah)
    #print(np.diag(tablaSah,j))
    return np.trace(tablaSah,j)

def Diag2CountQueen(tablaSah,i,j):
    #print(tablaSah[::-1])
    #print(np.diag(tablaSah[::-1],j))
    return np.trace(tablaSah[::-1],j)

def VerifQueen(i,j):
    if(LineCountQueen(i,j) or ColumnCountQueen(i,j) or Diag1CountQueen(i,j) or Diag2CountQueen(i,j)):
        return 1
    return 0 

#to calculate the heuristic cost; in this case it is the total number of attacks
def heuristic_cost(tablaSah):
    h = 0
    #calculam pentru toate liniile
    for i in range(len(tablaSah)):
        local_cost = LineCountQueen(tablaSah,i,len(tablaSah))
        if(local_cost>0):
            h = h + local_cost-1
    #debug 
    #print('cost linie: ' + str(h))

    #calculul costului pentru coloane
    for j in range(len(tablaSah)):
        local_cost = ColumnCountQueen(tablaSah,j,len(tablaSah))
        if(local_cost>0):
            h = h + local_cost-1
    #debug 
    #print('cost coloane: ' + str(h))

    #calcul cost diagonala principala si secundara
    for i in range(len(tablaSah)//2+1):
        local_cost_sup = Diag1CountQueen(tablaSah,0,i)
        if(local_cost_sup>0):
            h = h + local_cost_sup - 1
        if(i>0):
            local_cost_inf = Diag1CountQueen(tablaSah,0,-i)
            if(local_cost_inf>0):
                h = h + local_cost_inf - 1

    #debug 
    #print('cost diagonala principala: ' + str(h))

    for i in range(len(tablaSah)//2+1):
        local_cost_sup = Diag2CountQueen(tablaSah,0,i)
        if(local_cost_sup>0):
            h = h + local_cost_sup - 1
        if(i>0):
            local_cost_inf = Diag2CountQueen(tablaSah,0,-i)
            if(local_cost_inf>0):
                h = h + local_cost_inf - 1
    #debug 
    #print('cost diagonala secundara: ' + str(h))

    return h




def hill_climbing(tablaSah):
    #calculam un cost initial
    current_h = heuristic_cost(tablaSah)

    #salvam intr-o lista pozitia fiecarei regine de pe tabla; In felul acesta ne asiguram cu un numar fix de n stari ce nu se va repeta
    list_regine = []
    for i in range(0, len(tablaSah)):
        for j in range(0, len(tablaSah)):
            if(tablaSah[i][j] == 1):
                list_regine.append( (i,j) )
    for a,b in list_regine:
        print(a,b)

    #succesiv vom determina optimul local pentru fiecare stare(regina) pana cand ajungem la 0 atacuri, momentan in care toate reginele sunt puse la locul lor!
    #while(1):
        #BRUTE FORCE
        #determinam heuristica costului maxim; in cazul de fata, numarul minim de atacuri fata de starea curenta a tablei!    
        for i_q, j_q in list_regine:
                #vom incerca toate mutarile posibile ??? pentru starea curenta (regina curent gasita) si intoarcem la final
                    #tabela cu solutia finala a problemei pentru starea curenta
                    tablaBest = tablaSah
                    for i in range(0, len(tablaSah)):
                        for j in range(0, len(tablaSah)):
                            if(tablaSah[i][j] != 1):
                                tablaTemp = deepcopy(tablaSah)
                                tablaTemp[i_q][j_q] = 0
                                tablaTemp[i][j] = 1
                                min_h = heuristic_cost(tablaTemp)

                                #debug
                                afisareTabla(tablaTemp)
                                print(min_h)
                                #print(min_h)
                                #time.sleep(10)
                            if(min_h < current_h):
                                tablaBest = tablaTemp
                                current_h = min_h
                #///
                    tablaSah = tablaBest
                    
                    
                    if(current_h == 0):
                        #tablaSah = tablaBest
                        return tablaSah
                
                            
def afisareTabla(tablaSah):
    for i in range(len(tablaSah)):
        for j in range(len(tablaSah)):
            if(tablaSah[i][j] == 1):
                print('Q', end=" ")
            else:
                print('_', end=" ")
        print()


def __main__():
    #tablaSah = generateMatrix(8)
    #for debugging
    tablaSah = []
    for i in range(4):
        row = input("line=")
        row = [int(x) for x in row.split(" ")]
        tablaSah.append(row)
        
    n = len(tablaSah)
    #tablaSah = pozitionareRND(tablaTemp,8)
    print(heuristic_cost(tablaSah))    
    afisareTabla(hill_climbing(tablaSah))
if __name__ == "__main__":
    __main__()