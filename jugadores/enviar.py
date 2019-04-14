


import os,sys

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

# crea un tablero de tamanio tam 
def crearTablero(tam):
    tab = [ [ BLANCO for j in range(tam) ] for i in range(tam)]
    P=['x','x','x',BLANCO,BLANCO,'o','o','o']
    for i in range(tam*tam):
        v=P[ int(i/tam) ]
        if i % 2 == int(i/tam)%2 :
            tab[int(i / tam)][i%tam] = v
    return tab

# imprime el tablero tab
def imprimirTablero(tab):
    imprimir(' |0|1|2|3|4|5|6|7|')
    for i in range(8):
        linea = ""
        for j in range(8):
            linea += "|" +tab[i][j]
        linea += "|"
        imprimir( i,linea )
    imprimir(" ") 

def send( nomPipe, texto ):
    pipeout = os.open(nomPipe, os.O_WRONLY)
    os.write(pipeout, texto)
 
def reciv( nomPipe ):
    pipein = open(nomPipe, 'r')
    line = pipein.readline()[:-1]
    return line
 

def enviarTablero(tablero,J,nomPipe):
    env = ''
    par = 0
    for fila in range(len(tablero)):

        par = fila % 2

        for i in tablero[fila]:
            if par % 2 == 0:
                env += i
            par +=1
    env += ':' + J
    print(env)
    
    send(nomPipe,env)

    pipeRec = nomPipe+"-x"

    imprimir("esperando por : ",pipeRec)
    ret = reciv(pipeRec)
    print ret

def imprimir(*args):
    imp = ''
    
    for i in args:
        imp +=str(i)
    #print( imp )        #py3
    print imp          #py2

nomPipe = "hola"

"""
os.mkfifo(nomPipe)
os.mkfifo(nomPipe+"-x")
os.mkfifo(nomPipe+"-o")
#"""


tablero=crearTablero(8)

imprimir("tablero inicial :")
imprimirTablero(tablero)


#os.mkfifo(nomPipe)

enviarTablero(tablero,J1['pieces'],nomPipe)

