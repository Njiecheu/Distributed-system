CC	=	gcc
CFLAGS	=	-W		-Wall		-ansi	-pedantic	-std=c99	-pthread
SERVEUR	=	serveur

$(SERVEUR):serveur.o	traitement.o
			$(CC)	-o						$(SERVEUR)							$^					$(CFLAGS)

traitement.o:traitement.c
			$(CC)			-o						$@						-c						$<						$(CFLAGS)


serveur.o:serveur.c
			$(CC)			-o						$@						-c						$<						$(CFLAGS)



clean:							
				rm						-rf					*.o
																								
clean_all:							clean
				rm						-rf				$(SERVEUR)
