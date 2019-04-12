
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

def player(E,M,J):
    if J=='X':
        return getUtilMove(E,J1,J2,M,5)
    else:
        return getUtilMove(E,J2,J1,M,5)

def getUtilMove(E,J1,J2,M,d):
    move=None
    util=-float('Inf')
    for m in M:
        u=utilFunc(makeMove(E,m,J1),J1,J2,d,-1)
        if u>util:
            util=u
            move=m
    return move


def utilFunc(E,J1,J2,d,t):
    R=0
    M=None
    if d==0:
        R=utilFuncAux(E,J1)
        return R
    elif t>0:
        M=moves(E,J1)
        for m in M:
            R+=utilFunc(makeMove(E,m,J1),J1,J2,d-1,-t)
    else:
        M=moves(E,J2)
        for m in M:
            R+=utilFunc(makeMove(E,m,J2),J1,J2,d-1,-t)
    if len(M)==0:
        if t>0:
            return -24.
        else:
            return 24.
    return R/len(M)


def utilFuncAux(E,J):
    R=0.
    for E_ in E:
        for e in E_:
            if e==J['pices'][0]:
                R+=1.
            elif e==J['pices'][1]:
                R+=2.
            elif e==J['adversary'][0]:
                R-=1.
            elif e==J['adversary'][1]:
                R-=2.
    return R


def recmov(E,J,i,j):
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

def makeMove(E0,m,J):#estado , movimiento
    E=[[E0[i][j] for j in range(8)]for i in range(8)]
    for i in range(1,len(m)):
        E[m[i][0]][m[i][1]]=E[m[i-1][0]][m[i-1][1]]
        E[m[i-1][0]][m[i-1][1]]=BLANCO
        if abs(m[i-1][0]-m[i][0])>1:
            x=int((m[i-1][0]+m[i][0])/2)
            y=int((m[i-1][1]+m[i][1])/2)
            E[x][y]=BLANCO
        if m[i][0]==J['crown']:
            E[m[i][0]][m[i][1]]=J['pices'][1]
    return E


def moves(E,J):
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
