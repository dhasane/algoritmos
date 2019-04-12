

// general ---
# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <stdbool.h>

// pipes -----
# include <fcntl.h>
# include <sys/stat.h>
# include <unistd.h>


# define MAX 100

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
// retorna un string con los datos
char* receive(char* pipe, char* ret)
{
   //char* ret = (char*) malloc (sizeof(char)*(MAXR) );
   char txt[MAX];
   int fd;
   strcpy(txt," ");
   
   fd = open(pipe, O_RDONLY);

   read(fd, txt, sizeof(txt));

   close(fd);

   strcpy(ret,txt);
}


void recibirTablero()
{

}

int main(int argc, char **argv)
{
    if( argc != 2)
    {
        printf("cantidad de argumentos incorrecto \n- %s (nombre pipe) \n",argv[0] );
        exit(0);
    }
    char * nombrePipe = argv[1];
    //recibirTablero();

    char* texto ;

    while(1)
    {
        receive(nombrePipe, texto );
    }

    return 0; 
}