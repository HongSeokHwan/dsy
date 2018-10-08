#ifndef QUEUE_H
#define QUEUE_H

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>

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

typedef SEGMENT element;

typedef struct queue {
    int front;
    int rear;
    int size;
    int capacity;
    SEGMENT* array;
} Queue;

extern Queue* create_queue(int capacity);

extern int is_full(Queue* queue);

extern int is_empty(Queue* queue);

extern void enqueue(Queue* queue, SEGMENT item);


extern SEGMENT dequeue(Queue* queue);

#endif
