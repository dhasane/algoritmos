#from checkers import *

def player(E,M,J):
    if len(M)==0:
        return None
    for i in range(len(M)):
        print( i,':',M[i] )
    return M[int(input('move:'))]



'''

'''
