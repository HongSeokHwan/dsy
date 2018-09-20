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


typedef struct _Semaphore
{
    int value;
} Semaphore;

typedef struct _Condition
{
    int status;
} Condition;

Semaphore mutex;
Condition cond;
struct LinkedList mainlist;
void *producer(void *arg);
void *consumer(void *arg);


int main()
{
    init(&mainlist);
    mutex.value = 1;
    cond.status = 0;

    pthread_t threads[2];
    pthread_create(&threads[0], NULL, producer, NULL);
    pthread_create(&threads[1], NULL, consumer, NULL);

     for(int i = 0 ; i < 2 ; i++)
        pthread_join(threads[i], NULL);

    return 0;
}


void try()
{
    while(mutex.value <= 0);
    mutex.value--;
}


void increment()
{
    mutex.value++;
}


void wait(int status)
{
    mutex.value++;
    printf("%d", mutex.value);
    while(mutex.value != 1);
    while(mutex.value <= 0);
    mutex.value--;
}


void wakeup(int status)
{
    mutex.value++;
}


void *producer(void *arg)
{
    int i, data;

    for(i = 0 ; i < 1000 ; i++){
        try();

        if(mainlist.size == 100){
            printf("Ring is full! We should wait consumer!\n");
            wait();
        }

        data = i;
        insert(&mainlist, data);
        wakeup();

        increment();
    }
}


void *consumer(void *arg)
{
    int i, data;

    for(i = 0 ; i < 1000 ; i++){
        try();

        if(mainlist.size == 0){
            printf("Ring is empty! We should wait producer! \n");
            wait();
        }

        data = delete(&mainlist);
        wakeup();

        increment();

        printf("%dth data is %d\n", mainlist.size, data);
    }
}