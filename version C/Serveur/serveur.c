#include "traitement.h"
 //le port 5000 sera pour partager un repertoire
 //le port 6000 sera pour rechercher un fichier
 //le port 7000 sera pour le partage de fichier


int main(int argc,char **argv) {
    int server_socket;//socket serveur de partage de la liste
    int  client_socket;//socket client pour le partage de repertoire
    struct sockaddr_in server_address ;
    struct sockaddr_in client_address;
    pthread_t tid;
    //pthread_t sid[10];


    if (argc==2){
        if(strcmp(argv[1],"start")==0){
             // créer un socket serveur
                if ((server_socket = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
                    perror("socket share");
                    exit(1);
                }
                
                // configurer le serveur de recuperation de liste
                memset(&server_address, 0, sizeof(server_address));
                server_address.sin_family = AF_INET;
                server_address.sin_port = 5000;
                server_address.sin_addr.s_addr = htonl(INADDR_ANY);

                // lier le socket serveur de partage de repertoire à l'adresse 
                if (bind(server_socket, (struct sockaddr *)&server_address, sizeof(server_address)) == -1) {
                    perror("bind 5000");
                    exit(1);
                }
                // écouter les connexions des clients
                if (listen(server_socket, 5) == -1) {
                    perror("listen 5000");
                    exit(1);
                }else{
                    printf("Le serveur de partage de repertoire est demarre  sur le port %d\n",server_address.sin_port);
                }
                int menu_number;
                    unsigned int client_address_length = sizeof(struct sockaddr_in);
                while (1) {
                
                    // accepter les connexions des clients pour le partage de leur liste
                    if (
                        (client_socket = accept(server_socket,
                                        (struct sockaddr *)&client_address, 
                                        &client_address_length)) == -1 ){          
                        perror("accept");
                        continue;
                    }
                        // créer un thread pour gérer le client qui envoie sa liste
                    if(client_socket>0){
                        
                        recv(client_socket,&menu_number,sizeof(int),0);

                        if(menu_number==1){
                            logclient(client_address,"shared");
                            pthread_create(&tid, NULL, handle_client, &client_socket);
                        }
                        else if(menu_number==2){
                            logclient(client_address,"search");
                            pthread_create(&tid, NULL, handle_data, &client_socket);   
                        }
                        else{
                            printf("c'est tout pour le moment\n");
                        }
                        
                    }   
                        pthread_join(tid,NULL); 
                    
                    
                }

                close(server_socket); // fermer le socket serveur
            
        }
        else if(strcmp(argv[1],"logserver")==0){
            printf("log du serveur\n");
            system("tail -n20 -f log.txt");
        }

          else if(strcmp(argv[1],"filter")==0){
            
            char filter[255];
            printf("entrer le mot a filtrer");
            scanf("%255s",filter);
            system("grep -i  log.txt");
        }

        else{
            printf("commande introuvable\n[CMD]:./serveur runserver|logserver\nrunserver:commande pour demarrer le serveur\nlogserver:commande pour afficher les logs du serveur\nfilter:pour filtrer les logs\n");
        }
    }
    return 0;
}
