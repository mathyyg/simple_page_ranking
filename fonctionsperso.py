import numpy as np

def permutation(A,y,i,k) :
    line_i = A[i].copy()
    y_i = y[i]
    A[i] = A[k]
    A[k] = line_i

    y[i] = y[k]
    y[k] = y_i
    return A,y

def elimination(A,y,i,j) :
    for k in range(i+1,len(A)) :
        y[k] = y[k]-A[k,j]*y[i]/A[i,j]
        A[k] = A[k]-A[k,j]*A[i]/A[i,j]
    return A,y

def next_pivot(A,i,j) :
    n,p = A.shape
    k = i
    l = j
    while l<p and np.isclose(A[k,l],0) :
        if k < n-1 :
            k+=1
        else :
            k=i
            l+=1
    return k,l

def Gauss(A,y) :
    n,p = A.shape
    i=0
    j=0
    while i < n and j < p :
        k,j = next_pivot(A,i,j)
        if j < p :
            if k != i :
                permutation(A,y,i,k)
            A,y = elimination(A,y,i,j)

            i = i+1
            j = j+1
    return A,y

def first_non_zero(L) :
    for i in range(len(L)) :
        if not np.isclose(L[i],0) :
            return i
    return -1

def solveTriSup(A,y) :
    (n,p) = A.shape
    nb_eq = n
    res = np.zeros(p)
    for i in range(n-1,-1,-1) :
        k = first_non_zero(A[i])
        if(k != -1) :
            t = y[i]
            for l in range(k+1,p) :
                t = t-A[i,l]*res[l]
            res[k] = t/A[i,k]
        else :
            if not np.isclose(y[i],0)  :
                print("Pas de solution")
            else :
                nb_eq = nb_eq-1
    if nb_eq < p :
        print("Infinité de solutions")
    else :
        print("Unique solution")
    return res