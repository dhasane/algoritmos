

#include <stdio.h> 
#include <string.h> 
#include <fcntl.h> 
#include <sys/stat.h> 
#include <sys/types.h> 
#include <unistd.h> 

// general ---
# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <stdbool.h>

// pipes -----
# include <fcntl.h>
# include <sys/stat.h>
# include <unistd.h>
# include <signal.h>


// abre el pipe "pipe", envia un mensaje "txt" a traves de este y cierra el pipe
// sin retorno
void send(char* pipe, char txt[])
{
   int fd;
   fd = open(pipe, O_WRONLY);
   write(fd, txt, strlen(txt)+1);
   close(fd);
}

// recive datos a traves de pipe "pipe"
// retorna un string con los datos, por referencia
void receive(char* pipe, char* ret, int tam)
{
    //size_t tam = sizeof(ret)/sizeof(*ret);
    char txt[tam];
    int fd;
    strcpy(txt," ");
    fd = open(pipe, O_RDONLY);
    read(fd, txt, sizeof(txt));
    close(fd);
    //printf("\n---------------: %s\n", txt);
    strcpy(ret,txt);
}

void conseguirTablero(char* pipe, char tablero[][8], char * jugador , int tam)
{
    //int tam = 80 ;
    //char arr1[80];
    char* arr1 = (char*)malloc(sizeof(char)*tam);

    receive(pipe,arr1,tam);

    //printf("User2: %s", arr1);
    int pos = 0; 
    int par = 0 ; 

    if (strlen(arr1) > 1)
    {
        for( int a = 0 ; a < 8 ;a++ )
        {
            par = a % 2;
            for ( int b = 0 ; b < 8 ; b++ )
            {
                if ( par % 2 == 0)
                {
                    tablero[a][b] = arr1[pos];
                    pos++;
                }
                else 
                {
                    tablero[a][b] = '-';
                }
                //printf("%c",tablero[a][b]);   
                par ++;

            }
            //printf("\n");
        }
    }

    free(arr1);
    
}

void enviarTablero(char* pipe,char tablero[][8], char* jugador, int tam)
{
    char* envio = (char*)malloc(sizeof(char)*tam);
    int par = 0 ; 

    for( int a = 0 ; a < 8 ;a++ )
    {
        
        par = a % 2;
        for ( int b = 0 ; b < 8 ; b++ )
        {
            if ( par % 2 == 0)
            {
                
                strcat(envio,(const char*)tablero[a][b]);
            }
            par ++;

        }
    }

    strcat(envio,jugador);

    printf("%s\n",envio);

}

void imprimirTablero(char tablero[][8])
{
    for( int a = 0 ; a < 8 ;a++ )
    {
        for ( int b = 0 ; b < 8 ; b++ )
        {
            
            printf("%c",tablero[a][b]);

        }
        printf("\n");
    }
}