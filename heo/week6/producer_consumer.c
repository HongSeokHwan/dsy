#include <stdio.h>
#include <unistd.h>
#include <pthread.h>
#include <stdlib.h>
#include <stdbool.h>


struct Node{
    int data;
    struct Node* next;
};

struct LinkedList{
    int size;
    struct Node* head;
    struct Node* tail;
};

typedef struct _Semaphore
{
    int value;
} Semaphore;

void init(struct LinkedList* plist){
    plist->size = 0;
    plist->head = NULL;
    plist->tail = NULL;
}

bool isempty(struct LinkedList* plist){
    if(plist->size == 0)
        return true;
    else
        return false;
}

void insert(struct LinkedList* plist, int data)
{
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));

    newNode->data = data;
    newNode->next = NULL;

    if(isempty(plist)){
        plist->head = newNode;
        plist->tail = newNode;
    }

    else{
        plist->tail->next = newNode;
        plist->tail = newNode;
    }

    (plist->size)++;
}

int delete(struct LinkedList* plist){
    struct Node* delNode;
    int data;

    data = plist->head->data;
    delNode = plist->head;

    plist->head = plist->head->next;
    free(delNode);

    (plist->size)--;

    return data;
}

Semaphore mutex;
Semaphore full;
Semaphore empty;

struct LinkedList mainlist;
void *producer(void *arg);
void *consumer(void *arg);

int main()
{
    init(&mainlist);
    mutex.value = 1;
    full.value = 0;
    empty.value = 100;

    pthread_t threads[2];
    pthread_create(&threads[0], NULL, producer, NULL);
    pthread_create(&threads[1], NULL, consumer, NULL);

     for(int i = 0 ; i < 2 ; i++)
        pthread_join(threads[i], NULL);

    return 0;
}


void P(int* value)
{
    while((*value) <= 0);
    (*value)--;
}


void V(int* value, int size)
{
    (*value) += size;
}


void *producer(void *arg)
{
    int data = 0;

    do{
        data++;
        P(&empty.value);

        // when keep inserting items, you got into
        // infinite loop if there is no condition statement
        if(mutex.value != 0)
            P(&mutex.value);

        insert(&mainlist, data);

        if(empty.value <= 0){
            V(&mutex.value, 1);
            V(&full.value, 1);
            printf("Ring is full!\n");
        }

    } while(1);
}


void *consumer(void *arg)
{
    int data[10];

    do{
        P(&full.value);
        P(&mutex.value);

        for(int i = 0; i < 10; i++)
            data[i] = delete(&mainlist);

        sleep(2);

        printf("Output datas are\n");
        for(int i = 0; i < 10; i++)
            printf("%d\t", data[i]);
        printf("\t Now, ring has space\n");

        V(&mutex.value, 1);
        V(&empty.value, 10);
    } while(1);
}