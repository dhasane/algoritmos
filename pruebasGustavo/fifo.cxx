#include <iostream>
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
using namespace std;

void send(char* pipe,char*  msg){
  int pipeM = open(pipe, O_WRONLY);
  write(pipeM,msg, strlen(msg)+1);
  close(pipeM);
}

char *get(char* pipe,char* msg){
  int pipeT = open(pipe, O_RDONLY);
  read(pipeT,msg,35);
  close(pipeT);
  return msg;
}

int main(){
  char *pipeT=(char*)"pipefifoT",*pipeM=(char*)"pipefifoM";
  char msg[35];
  while(true){
    get(pipeT,msg);
    send(pipeM,"a,0;c,2");
  }
}
