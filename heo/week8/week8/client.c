#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/types.h>

#define PORT 50000
#define BUFSIZE 1024

struct packet {
    char data[BUFSIZE];
    int dataSize;
    int dataSeq;
};

void main(int argc, char* argv[])
{
    int sock;
    struct sockaddr_in serv_addr;
    int serv_addr_size;

    char buff_rcv[BUFSIZE];
    char buff_send[BUFSIZE];

    if((sock = socket(AF_INET, SOCK_DGRAM, 0)) == -1){
        printf("socket failed\n");
        exit(1);
    }

    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET; // IPv4 IP
    serv_addr.sin_port = htons(PORT); // port number
    serv_addr.sin_addr.s_addr = inet_addr(127.0.0.1); // 32bit IPv4 address

    while(1){
        printf("INPUT: ");
        fgets(buff_send, BUFSIZE, stdin);

        sendto(sock, argv[1], strlen(argv[1])+1, 0,
            (struct sockaddr*)&serv_addr, sizeof(serv_addr));
        
        serv_addr_size = sizeof(serv_addr);
        recvfrom(sock, buff_rcv, BUFSIZE, 0, 
            (struct sockaddr*)&serv_addr, &serv_addr_size);
        printf("receive: %s\n", buff_rcv);
    }
    close(sock);
}
