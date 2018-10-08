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

void main(){
    int sock;
    struct sockaddr_in serv_addr;
    struct sockaddr_in cli_addr;
    int cli_addr_size;

    char buff_rcv[BUFSIZE];
    char buff_send[BUFSIZE];

    if((sock = socket(PF_INET, SOCK_DGRAM, 0)) == -1){
        printf("socket failed\n");
        exit(1);
    }

    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = PF_INET; // IPv4 IP
    serv_addr.sin_port = htons(PORT); // port number
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY); // 32bit IPv4 address

    if(bind(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr))){
        printf("bind failed\n");
        exit(1);
    }

    while(1){
        cli_addr_size = sizeof(cli_addr);
        recvfrom(sock, buff_rcv, BUFSIZE, 0, 
            (struct sockaddr*)&cli_addr, &cli_addr_size);

        sprintf(buff_send, "%s%s", buff_rcv, buff_rcv);
        sendto(sock, buff_send, strlen(buff_send)+1, 0,
            (struct sockaddr*)&cli_addr, sizeof(cli_addr));
    }
}