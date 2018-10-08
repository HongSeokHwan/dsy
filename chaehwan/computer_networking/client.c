#include <stdio.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <stdlib.h>

#include "tcp.h"


int main()
{
    int client_socket;
    struct sockaddr_in server_address;
    char buffer[BUFSIZ];
    int input_length;
    int sent;
    int address_length;

    Queue* sending_buffer = create_queue(1024);
    Queue* receiving_buffer = create_queue(1024);

    client_socket = socket(AF_INET, SOCK_DGRAM, 0);

    memset(&server_address, 0, sizeof(server_address));
    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = inet_addr("127.0.0.1");
    server_address.sin_port = htons(50000);

    while (1)
    {
        input_length = read(0, buffer, BUFSIZ);
        if (input_length > 0){
            buffer[input_length] = '\0';
            if (!strcmp(buffer, "quit\n")){
                break;
            }

            printf("original Data : %s", buffer);

            sent = sendto(client_socket,
                          buffer,
                          strlen(buffer),
                          0,
                          (struct sockaddr *)&server_address,
                          sizeof(server_address));
            if (sent < 0)
            {
                fprintf(stderr, "sendto error\n");
                return -1;
            }

            address_length = sizeof(server_address);
            input_length = recvfrom(client_socket,
                                    buffer,
                                    sizeof(sending_buffer),
                                    0,
                                    NULL,
                                    NULL);
            if (input_length < 0)
            {
                fprintf(stderr, "recvfrom error\n");
                return -1;
            }
        }
        buffer[input_length] = '\0';

        printf("echoed Data : %s", buffer);
    }
    close(client_socket);
    return 0;
}

