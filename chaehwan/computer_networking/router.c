#include <stdio.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <arpa/inet.h>

#include "tcp.h"


void set_address(struct sockaddr_in *address,
                 in_addr_t ip,
                 uint16_t portnumber);

void route(struct sockaddr_in *sender_address,
           struct sockaddr_in *router_address,
           struct sockaddr_in *receiver_address,
           int *router,
           char *buffer);

int main()
{
    int router_socket;
    struct sockaddr_in client_address;
    struct sockaddr_in router_address;
    struct sockaddr_in server_address;
    char buffer[BUFSIZ];
    int binding_result;

    router_socket = socket(AF_INET, SOCK_DGRAM, 0);

    // binding router address
    memset(&router_address, 0, sizeof(router_address));
    set_address(&router_address, htonl(INADDR_ANY), 50000);

    binding_result = bind(router_socket,
                         (struct sockaddr *)&router_address,
                         sizeof(router_address));
    if (binding_result < 0)
    {
        fprintf(stderr, "binding failed\n");
        return -1;
    }

    // binding server address
    memset(&server_address, 0, sizeof(server_address));
    set_address(&server_address, inet_addr("127.0.0.1"), 50001);

    while (1)
    {
        route(&client_address,
              &router_address,
              &server_address,
              &router_socket,
              buffer);
        route(&server_address,
              &router_address,
              &client_address,
              &router_socket,
              buffer);
    }
    close(router_socket);
    return 0;
}

void set_address(struct sockaddr_in *address, in_addr_t ip, uint16_t portnumber)
{
    address->sin_family = AF_INET;
    address->sin_addr.s_addr = ip;
    address->sin_port = htons(portnumber);
}

void route(struct sockaddr_in *sender_address,
           struct sockaddr_in *router_address,
           struct sockaddr_in *receiver_address,
           int *router,
           char *buffer)
{
    int address_length;
    int received;
    int sent;
    address_length = sizeof(sender_address);
    received = recvfrom(*router,
                        buffer,
                        sizeof(buffer),
                        0,
                        (struct sockaddr*)sender_address,
                        &address_length);
    if (received < 0)
    {
        fprintf(stderr, "reception failed\n");
        return;
    }
    printf("received data : %s", buffer);

    sent = sendto(*router,
                  buffer,
                  received,
                  0,
                  (struct sockaddr*)receiver_address,
                  sizeof(*receiver_address));
    printf("sent : %d\n", sent);
    if (sent < 0)
    {
        fprintf(stderr, "transmission failed\n");
        return;
    }
}
