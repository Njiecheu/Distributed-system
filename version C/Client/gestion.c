#include "gestion.h"
#include <unistd.h>
#include <dirent.h>
#include <sys/stat.h>
#include <sys/types.h>

# define DT_REG	    8


void directory(char *chemin){
    
    struct dirent *dir;
    //opendir permet d'ouvrir un repertoire
    DIR *d=opendir(chemin);

    if(d)
    {   
        FILE *file=fopen("liste.txt","w+");
        if(file==NULL){
            perror("Impossible d'ouvrir le fichier");
            exit(EXIT_FAILURE);
        }


        while((dir=readdir(d))!=NULL)
        {
            
            if(dir->d_type==DT_REG)
            {   
                fprintf(file,"%s\n",dir->d_name);
                                    
            }
        }
        fclose(file);
        closedir(d);

    }
    else{
        printf("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!CE DOSSIER N'EXISTE PAS!!!!!!!!!!!!!!!!!!!!!!!!!!!\n");
    }
}

void send_liste(int client_socket,char ip_adress[24],int port){
    Response reponse;
    strcpy(reponse.adresse_ip,ip_adress);
    reponse.port=port;
    // Ouverture du fichier en lecture
    FILE *fp = fopen("liste.txt", "r+");

    if (fp == NULL) {
    printf("Erreur: Impossible d'ouvrir le fichier.");
    exit(1);
    }
    // Envoi du fichier via la socket
    printf("Liste des fichiers partages:\n");
    while(fgets(reponse.nom_du_fichier,1024,fp)!=NULL){
        retirer_(reponse.nom_du_fichier);
        printf("                            -%s\n",reponse.nom_du_fichier);
        send(client_socket, &reponse, sizeof(Response),0);
    }
    printf("[+]Data sent :-)\n");

    // Fermeture du fichier et de la socket
    fclose(fp);
    close(client_socket);
}



int connexion(int sockfd, struct sockaddr_in addr){
    int connex;

     if((connex=connect(sockfd, (struct sockaddr*)&addr, sizeof(addr)))<0){
        perror("[-]Echec de connexion au serveur");
        logfile("Echec de connexion au serveur");
        return -1;
    }
    else{
         printf("[+]Connexion au serveur reussie.\n");
         logfile("connexion au serveur reussie");
    }
  
    return connex; 
}


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

void retirer_(char *mot){
   size_t len=0;
   while (mot[len]!='\n')
   {
      len++;
   }
   mot[len]='\0';

}

void logfile(char *action){
   FILE *fp=fopen("log.txt","a");
   time_t timer;
   struct tm* info;
   char timestamp[30];
   time(&timer);
   info=localtime(&timer);
   strftime(timestamp,sizeof(timestamp),"%Y-%m-%d %H:%M:%S",info);
   if(fp==NULL){
      perror("Echec d'ouverture de fichier log.txt");
   }
  
   fprintf(fp,"[ %s ]  %s\n",timestamp,action);
   fclose(fp);

}