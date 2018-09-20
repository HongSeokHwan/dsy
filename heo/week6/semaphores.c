#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>


typedef struct _Semaphore
{
    int value;
} Semaphore;

Semaphore mutex;

void *process_a(void *arg);
void *process_b(void *arg);


int main()
{
    mutex.value = 1;

    pthread_t threads[2];
    pthread_create(&threads[0], NULL, process_a, NULL);
    pthread_create(&threads[1], NULL, process_b, NULL);

    for(int i = 0; i < 2; i++)
        pthread_join(threads[i], NULL);

    return 0;
}


void P()
{
    while(1){
        if(mutex.value == 1){
            mutex.value--;
            return;
        }
    }
}


void V()
{
    mutex.value++;
}

void *process_a(void *arg)
{
    do{
        P();

        printf("Process A is complte!\n");

        sleep(5);

        V(mutex);

        sleep(3);
    } while(1);
}


void *process_b(void *arg)
{
    do{
        P(mutex);

        printf("Process B is complte!\n");

        sleep(10);

        V(mutex);

        sleep(3);
    } while(1);
}