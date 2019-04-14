
// general ---
# include <stdio.h> 
# include <string.h>  
# include <stdlib.h>

// pipes -----
# include <fcntl.h>
# include <unistd.h>

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
// retorna un string con los datos, por referencia -> ret
void receive(char* pipe, char* ret, int tam)
{
    char txt[tam];
    int fd;
    strcpy(txt," ");
    fd = open(pipe, O_RDONLY);
    read(fd, txt, sizeof(txt));
    close(fd);
    strcpy(ret,txt);
}

void conseguirTablero(char* pipe, char tablero[][8], char * jugador , int tam)
{
    char* arr1 = (char*)malloc(sizeof(char)*tam);

    receive(pipe,arr1,tam);

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
                par ++;
            }
        }
    }

    free(arr1);
}

void enviarTablero(char* pipe,char tablero[][8], char* jugador, int tam)
{
    char* envio = (char*)malloc(sizeof(char)*tam);
    int par = 0 ; 
    const char* g ; 

    for( int a = 0 ; a < 8 ;a++ )
    {
        par = a % 2;
        for ( int b = 0 ; b < 8 ; b++ )
        {
            if ( par % 2 == 0)
            {
                g = &tablero[a][b];
                strcat(envio,g);
            }
            par ++;

        }
    }

    strcat(envio,jugador);

    printf("%s\n",envio);

}

void imprimirTablero(char tablero[][8])
{
    printf(" |0|1|2|3|4|5|6|7|\n");
    for( int a = 0 ; a < 8 ;a++ )
    {
        printf("%d",a);
        for ( int b = 0 ; b < 8 ; b++ )
        {
            printf("|%c",tablero[a][b]);
        }
        printf("|\n");
    }
}