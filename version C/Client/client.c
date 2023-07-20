#include "gestion.h"

int main(int argc,char **argv){ 

if(argc==3){
    int sock;
    char buffer[1024];
    //Response data;
    struct sockaddr_in addr;
    char *tache;
    //connexion au serveur
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = inet_addr("192.168.43.227");
    addr.sin_port = 5000;
    char nom_fichier[1024];
    
   //menu pour permettre au clien de choisir l'operation qui souhaite effectuer
   int menu_number=0;
   printf("********************MENU******************\n");
   printf("             1-Share directory\n");  
   printf("             2-Search file\n");  
   printf("             3-View Logs\n");  
   printf("             4-Quit\n");  
  
  while(menu_number!=4 || (menu_number>=1 && menu_number<4) ) {

        printf("               Enter your choice:");  
        scanf("%d",&menu_number);
        
        switch (menu_number)
        {
            case 1:
                    printf("****************Share***********************\n");
                    sock = create_socket();  
                    printf("                Enter directory:");
                    scanf("%1024s",buffer);
                    directory(buffer);
                    connexion(sock,addr);
                    tache=malloc(strlen(buffer)+20);
                    send(sock,&menu_number,sizeof(int),0);
                    send_liste(sock,argv[1],atoi(argv[2])); 
                    printf("                You have shared: %s\n",buffer);
                    sprintf(tache,"%s %s",buffer,"has been shared");
                    logfile(tache);
                    close(sock);
                    free(tache);
                break;
            case 2:
                     tache=malloc(strlen(nom_fichier)+20);
                    printf("****************Search***********************\n");                
                    printf("                 Enter key word:");
                    scanf("%1024s",nom_fichier);
                    sock = create_socket();  
                    connexion(sock,addr);
                    send(sock,&menu_number,sizeof(int),0);
                    sprintf(tache,"%s %s",nom_fichier,"has been searched");
                     logfile(tache);
                    send(sock,nom_fichier,1024,0);
                    printf("                Client list who owned file :\n"); 
                     while(recv(sock,buffer,255,0)!=0){
                    printf("                                                    %s :\n                                                          -%s\n", nom_fichier, buffer);  
                    memset(&buffer,0,255);  
                    }
                     free(tache);
                deconnexion(sock);
                    
                break;
            case 3: printf("                 Client Logs\n");
                    system("tail -n10 log.txt");
                    printf("\n");
                break;
            case 4:
                printf("*********************Stop**************************\n");
                break;
            case 0:
                break;
            default:
                menu_number=0;
                printf("!!!Invalid choice. Try again\n");
                break;
            }
        }
   }
   else{
                
   }
}
