#ifndef __Gestion__
#define __Gestion__

#include <dirent.h>
#include <sys/stat.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <pthread.h>
#include <sys/stat.h>
#include <sys/types.h>  
#include "gestion.h"
#include <time.h>

//prototype des fonctions
void directory(char *chemin);
void send_liste(int client_socket,char ip_adress[24],int port);
int connexion(int sockfd, struct sockaddr_in addr);
int create_socket();
void deconnexion(int sockfd);
void retirer_(char *mot);
typedef struct Response{
    char nom_du_fichier[1200];
    char adresse_ip[24];
    int port;
} Response,*ResponseD;
void logfile(char *action);


#endif
