#include "traitement.h"
void deconnexion(int sockfd){

    shutdown(sockfd,SHUT_RDWR);
    close(sockfd);
    printf("[+]Deconnexion au serveur.\n");
}


//creation de la socket
int create_socket(){

    int sockfd = socket(AF_INET, SOCK_STREAM,0);
    if (sockfd < 0)
    {
        perror("[-]Echec de creation du Socket");
        return -1;
    }
    printf("[+]socket a ete cree.\n");
    return sockfd;

}


ResponseD SearchKeys(char *keyword){

   ResponseD data;
   memset(&data,0,sizeof(data));
   FILE *fp;
   fp = fopen("repertoire.txt", "r");
   if(fp == NULL) {
      printf("Erreur : le fichier n'existe pas ou ne peut pas être ouvert.\n");
      exit(EXIT_FAILURE);
   }
   char line[2100];
  
   int i=1;
   while((fgets(line,2100,fp)!=NULL)){
      if(strstr(line, keyword)!=NULL) {
        printf("ligne %d trouve :%s",i,line);
        fscanf(fp,"%s %s %d",data->nom_du_fichier,data->adresse_ip,&data->port);
        exit(EXIT_SUCCESS);
      }
      i++;
   }
   fclose(fp);
   return data;
}
   


void receive_liste(int client_socket){

// Ouverture du fichier en lecture
FILE *fp = fopen("repertoire.txt", "a+");
if (fp == NULL) {
   printf("Erreur: Impossible d'ouvrir le fichier.");
   exit(EXIT_FAILURE);
}

// recevoir du fichier via la socket
Response data;
while((recv(client_socket, &data, sizeof(Response), 0)!=0)) {
  //printf("fichier partage:%s",data.nom_du_fichier);
   fprintf(fp,"%s %s %d\n",data.nom_du_fichier,data.adresse_ip,data.port);
}

// Fermeture du fichier et de la socket
fclose(fp);
//shutdown(client_socket,SHUT_RDWR);
//close(client_socket);

}


void *handle_client(void *arg) {
    int client_socket = *(int *)arg;
    pthread_mutex_lock(&mutex);
      receive_liste(client_socket);
    pthread_mutex_unlock(&mutex);
    close(client_socket); 
    return arg;
}

void *handle_data(void *arg)
{
      char message[1024];
      fprintf(stdout,"Thread de recherche lance\n");
   // initialisation à zéro du message
      int client_socket = *(int *)arg;
      recv(client_socket, message,sizeof(message), 0);
      printf("mot cherche: %s\n",message);
      rechercher(client_socket,message);
    // send(client_socket,message,sizeof(message),0);      
   close(client_socket);
   return arg;
}


void logclient(struct sockaddr_in ip,char *action){
   FILE *fp=fopen("log.txt","a");
   time_t timer;
   struct tm* info;
   char timestamp[30];
   time(&timer);
   info=localtime(&timer);
   strftime(timestamp,sizeof(timestamp),"%Y-%m-%d %H:%M:%S",info);
   char temp[MAX_SIZE];
   if(fp==NULL){
      perror("Echec d'ouverture de fichier log.txt");
   }
  
   sprintf(temp,"%s:%d",inet_ntoa(ip.sin_addr),htons(ip.sin_port));
   fprintf(fp,"[ %s ]    %s    %s\n",timestamp,temp,action);
   fclose(fp);

}

void rechercher(int socket,char *buffer){
// Ouvrir le fichier de répertoire central en mode lecture
    FILE* fp = fopen("repertoire.txt", "r");
    if(fp == NULL) {
        perror("erreur d'ouverture de repertoire.txt");
        exit(EXIT_FAILURE);
    }

    // Chercher dans le fichier la liste des clients qui possèdent le fichier
    char ligne[256];
    char* nom_fichier;
    char* ip;
    char* port;
    int nb_resultats = 0;
    char* resultat[256];
    while(fgets(ligne, sizeof(ligne), fp) != NULL) {
        // Extraire le nom de fichier, l'adresse IP et le port de chaque ligne
        nom_fichier = strtok(ligne, " ");
        ip = strtok(NULL, " ");
        port = strtok(NULL, " \n");

        // Vérifier si le nom de fichier correspond à celui recherché
        if(strcmp(nom_fichier, buffer) == 0) {
            // Ajouter l'adresse IP et le port à la liste des résultats
            char* res = malloc(strlen(ip) + strlen(port) + 2);
            sprintf(res, "%s:%s", ip, port);
            resultat[nb_resultats++] = res;
        }
    }

    // Fermer le fichier de répertoire central
    fclose(fp);

    // Envoyer le nombre de résultats au client
   //  if(send(socket, &nb_resultats, sizeof(nb_resultats), 0) == -1) {
   //      perror("send");
   //      exit(EXIT_FAILURE);
   //  }

    // Envoyer la liste des résultats au client
    for(int j = 0; j < nb_resultats; j++) {
        if(send(socket, resultat[j], strlen(resultat[j]) + 1, 0) == -1) {
            perror("send");
            exit(EXIT_FAILURE);
        }
    }

    // Libérer la mémoire allouée pour la liste des résultats
    for(int j = 0; j < nb_resultats; j++) {
        free(resultat[j]);
    }

    printf("Recherche terminee.\n");

}