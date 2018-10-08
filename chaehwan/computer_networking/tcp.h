#ifndef TCP_H
#define TCP_H

#define MSS 10

typedef struct TCP_SEGMENT {
    uint16_t source_port;
    uint16_t destination_port;
    int sequence_number;
    int acknowledgement_number;
    int ACK;
    int SYN;
    int FIN;
    int checksum;
    int receive_window;
    char *data;
} SEGMENT;

typedef struct TCP_CONTROL_BLOCK {
    // state;
    int sequence_number;
    int send_base;
    int last_byte_received;
    int last_byte_read;
    int last_byte_sent;
    int last_byte_acked;
    // receive window;
    // congestion window;
    // timer;
} TCB;

#endif
