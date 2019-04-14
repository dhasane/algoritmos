import sys
import time
import random as rand

REPETICIONES=0
BLANCO='-'
TOT=0
J1={
    'pices':'xX',
    'adversary':'oO',
    'crown':7,
    'direction':{
        'x':[(1,1),(1,-1)],
        'X':[(1,1),(1,-1),(-1,1),(-1,-1)]
    }
}

J2={
    'pices':'oO',
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
        v=P[i/tam]
        if i % 2 == int(i/tam)%2 :
            tab[int(i / tam)][i%tam] = v
    return tab
    #imprimirTablero(tab)

def imprimirTablero(tab):
    print '  |0|1|2|3|4|5|6|7|'
    for i in range(8):
        linea = ""
        for j in range(8):
            linea += "|" +tab[i][j]
            #print(''.join(i))
        linea += "|"
        print i,linea
    print " "


def recmov(E,J,i,j):#estado, jugador, posicion pieza
    R=[]
    T=[]
    for dir in J['direction'][E[i][j]]:
        i_=i+2*dir[0]
        j_=j+2*dir[1]
        if i_ in range(8) and j_ in range(8) and E[i+dir[0]][j+dir[1]] in J['adversary'] and E[i_][j_]==BLANCO:
            T=recmov(makeMove(E,[(i,j),(i_,j_)],J),J,i_,j_)
            for k in range(len(T)):
                T[k]=[(i,j)]+T[k]
            R=R+T
    if len(R)==0:
        return [[(i,j)]]
    return R

def makeMove(E0,m,J):#estado , movimiento, jugador
    if m is None:
        return E0
    E=[[E0[i][j] for j in range(8)]for i in range(8)]
    for i in range(1,len(m)):
        E[m[i][0]][m[i][1]]=E[m[i-1][0]][m[i-1][1]]
        E[m[i-1][0]][m[i-1][1]]=BLANCO
        if abs(m[i-1][0]-m[i][0])>1:
            x=(m[i-1][0]+m[i][0])/2
            y=(m[i-1][1]+m[i][1])/2
            E[x][y]=BLANCO
        if m[i][0]==J['crown']:
            E[m[i][0]][m[i][1]]=J['pices'][1]
    return E


def moves(E,J):#estado, jugador
    M=[]
    take=False
    for i in range(8):
        for j in range(8):
            if E[i][j] in J['pices']:
                T=recmov(E,J,i,j)
                if len(T[0])>1:
                    take=True
                    M=M+T
    if not take:
        for i in range(8):
            for j in range(8):
                if E[i][j] in J['pices']:
                    for dir in J['direction'][E[i][j]]:
                        if i+dir[0] in range(8) and j+dir[1] in range(8) and E[i+dir[0]][j+dir[1]]==BLANCO:
                            M=M+[[(i,j),(i+dir[0],j+dir[1])]]
    return M


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

def win(E,J1,M,m):#estadodel tablero ,jugador que acaba de jugar, oponente
    if not(m in M):
        return True,J1['adversary'][1]
    if len(moves(E,J2))==0:
        return True,J1['pices'][1]
    w,W=ciclos(E,J1)
    if w:
        return w,W
    for e in E:
        if J1['adversary'][0] in e or J1['adversary'][1] in e:
            return False,None
    return True,J1['pices'][1]


def race(f,MaxTime,*args):
    try:
        t1=time.time()
        R=f(*args)
        t2=time.time()
        if t2-t1<=MaxTime:
            return R
        return None
    except:
        print "error en la ejecucion del jugador"
        return None


try:
    L=[sys.argv[1][:len(sys.argv[1])-3],sys.argv[2][:len(sys.argv[2])-3]]
    rand.shuffle(L)
    print L[0],"juega como X"
    print L[1],"juega como O"
    exec("import "+L[0]+" as LP1")
    exec("import "+L[1]+" as LP2")
    P1=LP1.player
    P2=LP2.player
    if len(sys.argv)>3:
        MaxTime=float(sys.argv[3])
    else:
        MaxTime=float("inf")
except:
    print "uso:python checkers.py <lib1.py> <lib2.py> [maxtime(segundos)]"
    exit()
E=crearTablero(8)
imprimirTablero(E)
w=False#win condition
W=None#winer
k=0
while not w:
    M=moves(E,J1)
    m=race(P1,MaxTime,E,M,'X')
    E=makeMove(E,m,J1)
    EEE+=[E]
    if len(EEE)>10:
        EEE=EEE[1:]
    w,W=win(E,J1,M,m)
    imprimirTablero(E)
    if not w:
        M=moves(E,J2)
        m=race(P2,MaxTime,E,M,'O')
        E=makeMove(E,m,J2)
        EEE+=[E]
        if len(EEE)>10:
            EEE=EEE[1:]
        w,W=win(E,J2,M,m)
        imprimirTablero(E)
    k+=1


print "gana",W
print k
