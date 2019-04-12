
// C program to implement one side of FIFO 
// This side writes first, then reads 

# include "comunicacion.cxx"

char * myfifo ;

// al cerrar el programa con ctrl c, para evitar que el manager siga tomando
// el talker como conectado
void signalCierre(int sig)
{
   unlink(myfifo);
   printf("\n");
   exit(1);
}

int main(int argc, char **argv)
{ 
    if( argc != 2)
    {
        printf("cantidad de argumentos incorrecto \n- %s (nombre pipe) \n",argv[0] );
        exit(0);
    }
    signal(SIGINT, signalCierre);

    int fd; 
    myfifo = argv[1];
    mkfifo(myfifo, 0666); 
  
    char arr1[80];
    char tablero [8][8];
    char jugador[2];
    
    conseguirTablero(myfifo,tablero,jugador,80);
    imprimirTablero(tablero);
    
    //enviarTablero(myfifo,tablero,jugador,80);

    return 0; 
} 
