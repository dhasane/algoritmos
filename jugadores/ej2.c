

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

    myfifo = argv[1];
  
    char arr1[80], arr2[80]; 
    while (1) 
    { 
        fgets(arr2, 80, stdin); 
        send(myfifo, arr2);
    } 
    return 0; 
} 
