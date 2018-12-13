#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <signal.h>
#include <unistd.h>

#define SERV_TCP_PORT 	6003 //A number that we choose ourselves

#define MAX_LENGTH	2000 // Max number of bits we can send from the plc

int	sockfd;

void slut () {close(sockfd);exit(1);}

int
main(int argc, char *argv[])
{
	int					newsockfd;
	struct sockaddr_in	serv_addr, cli_addr;
	int					n, cli_size, childpid; // Defining multiple integer variables
	char				string[MAX_LENGTH];
	cli_size = sizeof(cli_addr); // Size of the client

	if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
		printf("Server: Can't open stream socket");
		exit(0); }

	serv_addr.sin_family = AF_INET;
	serv_addr.sin_addr.s_addr = htonl(INADDR_ANY); //This is here because we want to bind to any IP address that is available
	serv_addr.sin_port = htons(SERV_TCP_PORT); //htons stands for Host TO Network Short

	signal (SIGINT, slut);
	if (bind(sockfd, (struct sockaddr *) & serv_addr, 
                 sizeof(serv_addr)) < 0) {
		printf("Server: Can't bind local add\n");
		exit(0); }

	listen(sockfd, 5); //sockfd is the socket we want to listen in on, 5 is the maximum number of connections that can be established

	while (1) {
		newsockfd = accept(sockfd, (struct sockaddr *) & cli_addr, 
                                   &cli_size);
		if (!(childpid = fork())) { // Fork makes the server concurrent, we have to change this if we don't want a concurrent server
			close(sockfd);
			n = read(newsockfd, string, MAX_LENGTH);
			write(newsockfd, string, n); // This is what is sent back i.e. what we need to change to send a command back
			exit(0);
		}
		close(newsockfd);
	}

}
