CC						=							gcc
CFLAGS		=							-W						-Wall			-ansi			-pedantic	-std=c99
CLIENT	=	client

$(CLIENT):client.o						gestion.o
								$(CC)			-o						$(CLIENT)							$^									$(CFLAGS)

gestion.o:gestion.c
								$(CC)			-o						$@						-c						$<						$(CFLAGS)


client.o:client.c
								$(CC)			-o						$@						-c						$<						$(CFLAGS)



clean			:							
																																																																rm						-rf					*.o
																								
clean_all							:							clean
																																																																rm						-rf					$(CLIENT)
