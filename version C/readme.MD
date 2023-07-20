Dans cette version C du repertoire centralisé, nous avons deux dossiers : 
 - un dossier client qui contient le code du client et de toutes les fonctions qui sont associées à ce dernier
 - un dossier serveur qui contient le code du serveur
 - un Makefile pour compiler les différents fichier client et serveur

pour compiler le client et le serveur on utilise la commande make aussi bien dans le dossier du client 
que dans celui du serveur. Une fois cela fait on lance le serveur à l'aide de la commande
./serveur.c ensuite on lance le client à l'aide de la commande ./client.c start avant tout ça se rassurer que 
l'on se trouve dans les repertoires contenant les exécutables du client et du serveur

Le client une fois connecté au serveur, il partage un dossier et ce dossier ne doit pas être vide
une fois le partage effectuée; les clients connectés au serveur pourront rechercher un fichier en particulier et ce dernier répondra en renvoyant le nom du fichier s'il existe suivi de l'adresse IP et du numéro de port
du client possédant le fichier recherché s'il n'existe pas le client recevra un message le cas échéant. lorsque le fichier demandé existe le client contacte directement le client possédant le fichier afin de le télécharger. on pourra aussi visualiser les logs du client et du serveur.
