import sys
import time
import random as rand

BLANCO='-'
TOT=0
J1={
    'pieces':'xX',
    'adversary':'oO',
    'crown':7,
    'direction':{
        'x':[(1,1),(1,-1)],
        'X':[(1,1),(1,-1),(-1,1),(-1,-1)]
    }
}

J2={
    'pieces':'oO',
    'adversary':'xX',
    'crown':0,
    'direction':{
        'o':[(-1,1),(-1,-1)],
        'O':[(1,1),(1,-1),(-1,1),(-1,-1)]
    }
}

EEE=[]

def crearTablero(tam):
    tab = [ [ BLANCO for j in range(tam) ] for i in range(tam)]
    P=['x','x','x',BLANCO,BLANCO,'o','o','o']
    for i in range(tam*tam):
        v=P[ int(i/tam) ]
        if i % 2 == int(i/tam)%2 :
            tab[int(i / tam)][i%tam] = v
    return tab

def imprimirTablero(tab):
    print('  |0|1|2|3|4|5|6|7|')
    for i in range(8):
        linea = ""
        for j in range(8):
            linea += "|" +tab[i][j]
        linea += "|"
        print( i,linea )
    print(" ")

def recmov(tablero,J,i,j):
    R=[]
    T=[]
    for dir in J['direction'][tablero[i][j]]:
        i_=i+2*dir[0]
        j_=j+2*dir[1]
        if i_ in range(8) and j_ in range(8) and tablero[i+dir[0]][j+dir[1]] in J['adversary'] and tablero[i_][j_]==BLANCO:
            T=recmov(makeMove(tablero,[(i,j),(i_,j_)],J),J,i_,j_)
            for k in range(len(T)):
                T[k]=[(i,j)]+T[k]
            R=R+T
    if len(R)==0:
        return [[(i,j)]]
    return R

def makeMove(tablero,m,J):#estado , movimiento
    E=[[tablero[i][j] for j in range(8)]for i in range(8)]
    if not (m is None):
        for i in range(1,len(m)):
            E[m[i][0]][m[i][1]]=E[m[i-1][0]][m[i-1][1]]
            E[m[i-1][0]][m[i-1][1]]=BLANCO
            if abs(m[i-1][0]-m[i][0])>1:
                x=int((m[i-1][0]+m[i][0])/2)
                y=int((m[i-1][1]+m[i][1])/2)
                E[x][y]=BLANCO
            if m[i][0]==J['crown']:
                E[m[i][0]][m[i][1]]=J['pieces'][1]
    
    return E

def moves(tablero,J):
    M=[]
    take=False
    for i in range(8):
        for j in range(8):
            if tablero[i][j] in J['pieces']:
                T=recmov(tablero,J,i,j)
                if len(T[0])>1:
                    take=True
                    M=M+T
    if not take:
        for i in range(8):
            for j in range(8):
                if tablero[i][j] in J['pieces']:
                    for dir in J['direction'][tablero[i][j]]:
                        if i+dir[0] in range(8) and j+dir[1] in range(8) and tablero[i+dir[0]][j+dir[1]]==BLANCO:
                            M=M+[[(i,j),(i+dir[0],j+dir[1])]]
    return M


def ciclos(T,Tv):
    coincidencias = 0 
    i = 0
    for tab in Tv :
        #imprimirTablero(tab)
        if tab == T:
           coincidencias += 1
    
    return coincidencias
    #if coincidencias >= 5:
    #    return True, coincidencias
    #else:
    #    return False, coincidencias

"""
def ciclos(E,J):#estado del tablero, jugador que acaba de jugar
    global REPETICIONES
    if len(EEE)<8:
        return False,None
    if E==EEE[len(EEE)-5]:
        REPETICIONES+=1
    else:
        REPETICIONES=0
    if REPETICIONES>9:
        n=0
        for e in E:
            for p in e:
                if p in J["pices"]:
                    n+=1
                if p in J["adversary"]:
                    n-=1
        if n==0:
            return True,None
        elif n>0:
            return True,J1['pices'][1]
        else:
            return True,J1['adversary'][1]
    return False,None
    #"""
# esta funcion sirve para definir si el jugador J ha perdido
def lose( tablero, tam, J):
    
    if tam == 0 :
        return True
    for e in tablero:
        if J['pieces'][0] in e or J['pieces'][1] in e:
            return False 
    
    return True

def contarJugadores(tablero):
    x = 0
    y = 0
    ganador = 0
    for y in range( len(tablero) ):
        for x in range( len ( tablero[y]) ):
            if   'x' == tablero[y][x] or 'X' == tablero[y][x]:
                x+=1
            elif 'o' == tablero[y][x] or 'O' == tablero[y][x]:
                y+=1
    
    if x > y:
        ganador = 1
    elif y > x:
        ganador = -1

    return ganador


def jugada(f,tablero,M,J,nombre,Tv,memoria):
    fin = False
    t1 = time.time() * 1000
    m=f(tablero,M,'X')
    tablero=makeMove(tablero,m,J)
    t2 = time.time() * 1000

    print("-----------")
    print("turno : ",J["pieces"],"(",nombre,")")
    imprimirTablero(tablero)

    #"""
    coincidencias = ciclos(tablero, Tv)
    print("coincidencias : ",coincidencias,"\ttiempo jugada : ",t2-t1)

    if coincidencias >= 5:
        ganador =  contarJugadores(tablero)
        fin = True

    Tv += [tablero]
    if len(Tv) > memoria:
        Tv.pop(0)
    ##"""
    return tablero , fin 
'''
T=[
['x','-','-','-','-','-','-','-'],
['-','x','-','-','-','-','-','x'],
['-','-','x','-','x','-','x','-'],
['-','-','-','-','-','x','-','x'],
['o','-','-','-','o','-','o','-'],
['-','-','-','o','-','-','-','o'],
['o','-','-','-','-','-','-','-'],
['-','o','-','o','-','-','-','-']
]'''

try:
    L=[sys.argv[1][:len(sys.argv[1])-3],sys.argv[2][:len(sys.argv[2])-3]]
    rand.shuffle(L)
    print( L[0],"juega como X" )
    print( L[1],"juega como O" )
    exec("import "+L[0]+" as LP1")
    exec("import "+L[1]+" as LP2")
    P1=LP1.player
    P2=LP2.player
    if len(sys.argv)>3:
        MaxTime=float(sys.argv[3])
    else:
        MaxTime=float("inf")
except:
    print( "uso:python checkers.py <lib1.py> <lib2.py> [maxtime(segundos)]" )
    exit()

memoria = 20 # cantidad de tableros guardados 
Tv = [] # tableros viejos

ganador = 0 # -1 : jugador 2 | 0 : empate | 1 : jugador 1

tablero=crearTablero(8)
imprimirTablero(tablero)
fin=False
k=0
M  = []

tiempo = 0

while not fin:

    # turno jugador 1
    
    M=moves(tablero,J1)
    fin=lose(tablero,len(M),J1)

    if not fin:
        
        tablero, fin = jugada(P1,tablero,M,J1,L[0],Tv,memoria)

        """
        coincidencias = ciclos(tablero, Tv)
        print("coincidencias : ",coincidencias,"\ttiempo jugada : ",tiempo)

        if coincidencias >= 5:
            ganador =  contarJugadores(tablero)
            fin = True

        Tv += [tablero]
        if len(Tv) > memoria:
            Tv.pop(0)
        """
        print(len(Tv))
        # turno jugador 2 
        
        M=moves(tablero,J2)
        fin=lose(tablero,len(M),J2)
        
        if not fin:

            tablero, fin = jugada(P2,tablero,M,J2,L[1],Tv,memoria)
            print(len(Tv))
            """
            coincidencias = ciclos(tablero, Tv)
            print("coincidencias : ",coincidencias,"\ttiempo jugada : ",tiempo)

            if coincidencias >= 5:
                ganador =  contarJugadores(tablero)
                fin = True
            Tv += [tablero]
            if len(Tv) > memoria:
                Tv.pop(0)
            """
        else:
            ganador = 1
    else:
        ganador = -1
  
    k+=1



if ganador == 1:
    print( "gana jugador : ", J1['pieces'],"(",L[0],")")
elif ganador == -1:
    print( "gana jugador : ", J2['pieces'],"(",L[1],")")
else:
    print("empate")


print( "\npartida terminada en ", k, " turnos" )
