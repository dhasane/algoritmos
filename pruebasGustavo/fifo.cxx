#include <iostream>
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
using namespace std;


int main(){
  int pipeT,pipeM;
  char *msg="mensaje",*tablero;
  cout<<"...";
  while(true){
    pipeT = open("pipefifoT", O_RDONLY);
    pipeM = open("pipefifoM", O_WRONLY);
    read(pipeT,tablero,20);
    cout<<tablero;
    write(pipeM,msg, strlen(msg)+1);
    close(pipeM);
    close(pipeT);

  }
}
