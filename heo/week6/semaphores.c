#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>


typedef struct _Semaphore
{
    int value;
} Semaphore;

Semaphore mutex;
int shared_array[5] = {0,0,0,0,0};
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
    while(mutex.value <= 0);
    mutex.value--;
}


void V()
{
    mutex.value++;
}


void *process_a(void *arg)
{
    do{
        P();

        for(int i = 0; i < 5; i++)
            shared_array[i] = 1;

        printf("Process A is complete!\n");
        printf("Shared array's values are: ");
        for(int i = 0; i < 5; i++)
            printf("%d", shared_array[i]);
        printf("\n\n");

        sleep(5);

        V(mutex);

        sleep(3);
    } while(1);
}


void *process_b(void *arg)
{
    do{
        P(mutex);

        for(int i = 0; i < 5; i++)
            shared_array[i] = 2;

        printf("Process B is complete!\n");
        printf("Shared array's values are: ");
        for(int i = 0; i < 5; i++)
            printf("%d", shared_array[i]);
        printf("\n\n");
        
        sleep(10);

        V(mutex);

        sleep(3);
    } while(1);
}