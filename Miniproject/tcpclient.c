#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <netdb.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

#define SERV_TCP_PORT 	6003

#define MAX_LENGTH	2000

int
main(int argc, char *argv[])
{
	int             sockfd;
	struct sockaddr_in serv_addr;
	int 			n;
	char            string[MAX_LENGTH];
	struct hostent *hostptr;
	
	if (argc <= 1) {
		printf("Use: %s server_name\n", argv[0]);
		exit(0);
	}
	if ((hostptr = gethostbyname(argv[1])) == NULL) {
		printf("\ngethostdyname error: %s\n", argv[1]);
		exit(1);
	}

	/*
	serv_addr.sin_family = AF_INET; 
	serv_addr.sin_addr.s_addr = inet_addr("130.225.50.10"); 
	serv_addr.sin_port = htons(SERV_UDP_PORT);
	*/

	serv_addr.sin_family = AF_INET;
	serv_addr.sin_addr.s_addr = 
              ((struct in_addr *) (hostptr->h_addr))->s_addr;
	serv_addr.sin_port = htons(SERV_TCP_PORT);

	if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
		printf("client: can't open stream socket\n");
		exit(0);
	}
	if (connect(sockfd, (struct sockaddr *) & serv_addr, 
                    sizeof(serv_addr)) < 0) {
		printf("client: can't connect to server\n");
		exit(0);
	}
	write(sockfd, "agjsdfkjhdsgfkjg", strlen("agjsdfkjhdsgfkjg"));
	n=read(sockfd, string, MAX_LENGTH);
	string[n]=0;


	printf("recivet string: %s\n", string);

	close(sockfd);
}
