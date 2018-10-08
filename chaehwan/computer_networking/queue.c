#include <stdio.h>
#include <stdlib.h>

#include "tcp.h"
#include "queue.h"


Queue* create_queue(int capacity)
{
    Queue* queue = (Queue*)malloc(sizeof(Queue));
    queue->capacity = capacity;
    queue->front = 0;
    queue->size = 0;
    queue->array = (SEGMENT*)malloc(queue->capacity * sizeof(SEGMENT));
    return queue;
}

int is_full(Queue* queue)
{
    if (queue->size == queue->capacity){
        return 1;
    }
    else {
        return 0;
    }
}

int is_empty(Queue* queue)
{
    if (queue->size == 0){
        return 1;
    }
    else {
        return 0;
    }
}

void enqueue(Queue* queue, SEGMENT item)
{
    if (is_full(queue)){
        printf("overflow\n");
        return;
    }
    else {
        queue->rear = (queue->rear + 1) % (queue->capacity);
        queue->array[queue->rear] = item;
        queue->size = queue->size + 1;
    }
}

SEGMENT dequeue(Queue* queue)
{
    if (is_empty(queue)){
        printf("underflow\n");
    }
    SEGMENT item = queue->array[queue->front];
    queue->front = (queue->front + 1) % (queue->capacity);
    queue->size = queue->size -1;
    return item;
}
