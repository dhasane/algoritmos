#include <iostream>
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <vector>
using namespace std;

struct jugador{
  string pieces;
  string adversary;
  int crown;
  int **dir;
  int **DIR;
};

jugador *J1;
jugador *J2;
char BLANCO='-';

int * makepos(int x, int y){
  int* pos=new int[2];
  pos[0]=x;
  pos[1]=y;
  return pos;
}

char **makeMove(char **tablero,vector<int*> m,jugador J){
  char** T=new char*[8];
  for(int i;i<8;i++){
    T[i]=new char[8];
  }
  int x,y;
  for(int i=0;i<8;i++){
    for(int j=0;j<8;j++){
      T[i][j]=tablero[i][j];
    }
  }
  if (!m.empty()){
    for(int i=1;i<m.size();i++){
      T[m[i][0]][m[i][1]]=T[m[i-1][0]][m[i-1][1]];
      T[m[i-1][0]][m[i-1][1]]=BLANCO;
      if (abs(m[i-1][0]-m[i][0])>1){
        x=(m[i-1][0]+m[i][0])/2;
        y=(m[i-1][1]+m[i][1])/2;
        T[x][y]=BLANCO;
      }
      if( m[i][0]==J.crown){
        T[m[i][0]][m[i][1]]==J.pieces[1];
      }
    }
  }
  return T;
}

vector<vector<int*>> recmov(char **tablero,jugador J,int i,int j){
  vector<vector<int*>> R;
  vector<vector<int*>>T;
  vector<int*> auxM;
  int **dir,lendir;
  char aux;
  if(tablero[i][j]>'Z'){
    dir=J.dir;
    lendir=2;
  }else{
    dir=J.DIR;
    lendir=4;
  }
  int i_,j_;
  bool C;
  auxM.push_back(makepos(i,j));
  auxM.push_back(makepos(i_,j_));
  for(int k=0;i<lendir;i++){
    i_=i+2*dir[k][0];
    j_=j+2*dir[k][1];
    C=i_>=0 && i_<8;
    C=C&&i_>=0 && i_<8;
    aux=tablero[i+dir[k][0]][j+dir[k][1]];
    C=C&&(aux==J.adversary[0]) || (aux==J.adversary[1]);
    C=C&&tablero[i_][j_]==BLANCO;
    if(C){
      T=recmov(makeMove(tablero,auxM,J),J,i_,j_);
      for(int l=0;l<T.size();l++){
        T[l].insert(T[l].begin(),makepos(i,j));
      }
      R.insert(R.end(),T.begin(),T.end());
    }
  }
  if(R.size()==0){
    vector<int*> aaa;
    aaa.push_back(makepos(i,j));
    R.push_back(aaa);
    return R;
  }
}

void send(char* pipe,char*  msg){
  int pipeM = open(pipe, O_WRONLY);
  write(pipeM,msg, strlen(msg)+1);
  close(pipeM);
}

char *get(char* pipe,char* msg){
  int pipeT = open(pipe, O_RDONLY);
  read(pipeT,msg,33);
  close(pipeT);
  return msg;
}

char **getTablero(char* pipe){
  char msg[33];
  char tablero[8][8];
  get(pipe,msg);
  int pos=0;
  for(int i=0;i<8;i++){
    for(int j=0;j<8;j++){
      if((i+j)%2==0){
        tablero[i][j]=msg[pos];
        pos++;
      }else{
        tablero[i][j]='-';
      }
    }
  }
}

void sendMove(char* pipe,vector<int*> M){
  char msg[M.size()*4];
  for(int i=0;i<M.size();i++){
    msg[i*4]=M[i][0]+97;
    msg[i*4+1]=',';
    msg[i*4+2]=M[i][1]+48;
    msg[i*4+3]=';';
  }
  msg[M.size()*4-1]=0;
  send(pipe,msg);
}

void init(){
  int **dir1=new int*[2];dir1[0]=new int[2];dir1[1]=new int[2];//{{1,1},{1,-1}};
  int **dir2=new int*[2];dir2[0]=new int[2];dir2[1]=new int[2];//{{-1,1},{-1,-1}};
  int **DIR=new int*[4];DIR[0]=new int[2];DIR[1]=new int[2];DIR[0]=new int[2];DIR[1]=new int[2];//{{1,1},{1,-1},{-1,1},{-1,-1}};
  dir1[0][0]=1;dir1[0][1]=1;dir1[1][0]=1;dir1[1][1]=-1;
  dir2[0][0]=-1;dir2[0][1]=1;dir2[1][0]=-1;dir2[1][1]=-1;
  DIR[0][0]=-1;DIR[0][1]=1;DIR[1][0]=-1;DIR[1][1]=-1;     DIR[2][0]=1;DIR[2][1]=1;DIR[3][0]=1;DIR[3][1]=-1;
  J1->pieces="xX";
  J1->adversary="oO";
  J1->crown=7;
  J1->dir=dir1;
  J1->DIR=DIR;

  J2->pieces="oO";
  J2->adversary="xX";
  J2->crown=0;
  J2->dir=dir2;
  J2->DIR=DIR;
}

int main(){
  char *pipeT=(char*)"pipefifoT",*pipeM=(char*)"pipefifoM";
  char msg[35];
  char *tablero;
  vector<int*> M;
  M.push_back(makepos(0,0));M.push_back(makepos(3,3));M.push_back(makepos(5,5));
  init();
  while(true){
    getTablero(pipeT);
    sendMove(pipeM,M);
  }
}
