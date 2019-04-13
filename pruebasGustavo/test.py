import os
import threading

def crearJugador(arg):#retorna la funcion del jugador y el nombre del jugador
    command=""
    name=""
    if arg[len(arg)-3:]==".py":
        name=arg[:len(arg)-3]
        command="python "+arg
        pipename="pipe"+name
    elif arg[len(arg)-4:]==".jar":
        name=arg[:len(arg)-4]
        command="java -jar "+arg
        pipename="pipe"+name
    else:
        name=arg
        command="./"+arg
        pipename="pipe"+arg
    os.mkfifo(pipename+'T')
    os.mkfifo(pipename+'M')
    print command
    thr = threading.Thread(target=lambda :os.system(command) )
    thr.start()

    def playerPipe(E,J):
        pipeT=open(pipename+'T','w')
        pipeM=open(pipename+'M','r')
        pipeT.write(E)
        pipeT.close()
        return pipeM.readline()
    return playerPipe


pl=crearJugador(raw_input("filename:"))

mensaje=''
while(True):
    mensaje=raw_input(':')
    print pl(mensaje,'x')
