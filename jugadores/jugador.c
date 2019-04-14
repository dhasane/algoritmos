
# include "comunicacion.cxx"

char * pipeReceive ;
char * pipeSend;

// al cerrar el programa con ctrl-c
void signalCierre(int sig)
{
   unlink(pipeReceive);
   unlink(pipeSend);
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
    pipeReceive = (char*)malloc(sizeof(char)*strlen(argv[1]) );
    pipeSend    = (char*)malloc(sizeof(char)*strlen(argv[1]) );
    
    strcpy(pipeReceive, argv[1]);
    strcpy(   pipeSend, argv[1]);

    sprintf(pipeSend,"%s-%c",pipeSend,'x');

    mkfifo(pipeReceive, 0666); 
    mkfifo(pipeSend, 0666); 

    
    printf("reciviendo por : %s\n",pipeReceive);
  
    char arr1[80];
    char tablero [8][8];
    char jugador[2];

    // jugadas -------------------------------------------------
    
    int prim = 1 ;

    //while(1)
    {

    conseguirTablero(pipeReceive,tablero,jugador,80);
    imprimirTablero(tablero);

    if( prim )
    {
        sprintf(pipeSend,"%s%c",pipeSend,jugador[0]);
        printf("enviando por : %s\n",pipeSend);
        prim = 0;
    }

    send(pipeSend, "a,0;c,2");
    
    }

    // fin jugadas ---------------------------------------------

    free(pipeReceive);
    free(pipeSend);

    return 0; 
} 
