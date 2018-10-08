#include <stdio.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/queue.h>

#include "tcp.h"


struct connection_info {
    int portnumber;
    LIST_ENTRY(connection_info) link;
} connection_info;

struct queue_head {
    LIST_HEAD(connection_info_list, connection_info) head;
};

struct queue_head syn_queue;
struct queue_head accept_queue;


int tcp_listen(int socket_fd, int backlog_size)
{
    LIST_INIT(&syn_queue.head);
    LIST_INIT(&accept_queue.head);

}

int main()
{
    int server_socket;
    struct sockaddr_in server_address;
    struct sockaddr_in router_address;
    SEGMENT receiving_buffer[BUFSIZ];
    SEGMENT sending_buffer[BUFSIZ];
    char buffer[BUFSIZ];
    int sent;
    int received;
    int address_length;
    int binding_result;

    server_socket = socket(AF_INET, SOCK_DGRAM, 0);

    memset(&server_address, 0, sizeof(server_address));
    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = htonl(INADDR_ANY);
    server_address.sin_port = htons(50001);

    binding_result = bind(server_socket,
                         (struct sockaddr *)&server_address,
                         sizeof(server_address));
    if (binding_result < 0)
    {
        fprintf(stderr, "binding failed\n");
        return -1;
    }

    while (1)
    {
        address_length = sizeof(router_address);
        received = recvfrom(server_socket,
                            buffer,
                            sizeof(buffer),
                            0,
                            (struct sockaddr*)&router_address,
                            &address_length);
        if (received < 0)
        {
            fprintf(stderr, "reception failed\n");
            return -1;
        }
        printf("received data : %s", buffer);

        sent = sendto(server_socket,
                      buffer,
                      received,
                      0,
                      (struct sockaddr*)&router_address,
                      sizeof(router_address));
        if (sent < 0)
        {
            fprintf(stderr, "transmission failed\n");
            return -1;
        }
    }
    close(server_socket);
    return 0;
}
