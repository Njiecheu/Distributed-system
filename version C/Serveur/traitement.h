#ifndef __TRAITEMENT__
#define __TRAITEMENT__


#include <dirent.h>
#include <sys/stat.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <pthread.h>
#include <time.h>
#define MAX_SIZE 2048
#define MAX_CLIENTS 100 // nombre maximum de clients

pthread_mutex_t mutex; // mutex pour la protection des clients

//structure de donnees pour retourner la reponse au client
typedef struct Response{
    char nom_du_fichier[1200];
    char adresse_ip[24];
    int port;
} Response,*ResponseD;

//prototype des fonctions
int create_socket();
void deconnexion(int sockfd);
//fonction retournant une infos de connexion
ResponseD SearchKeys(char *keyword);
//fonction pour traiter les connexions portant sur le partage de repertoire par les clients
void *handle_client(void *arg);
//fonction pour rechercher un fichier 
void *handle_data(void *arg);
void receive_liste(int client_socket);
void logclient(struct sockaddr_in ip,char *action);
void rechercher(int socket,char *buffer);
#endif