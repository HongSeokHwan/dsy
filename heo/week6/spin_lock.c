#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <stdbool.h>


void *process_a(void *arg);
void *process_b(void *arg);

bool flag[2] = {false, false};
int turn = 0;
int shared_array[5] = {0,0,0,0,0};


int main()
{
    pthread_t threads[2];
    pthread_create(&threads[0], NULL, process_a, NULL);
    pthread_create(&threads[1], NULL, process_b, NULL);

    for(int i = 0; i < 2; i++)
        pthread_join(threads[i], NULL);

    return 0;
}


void *process_a(void *arg)
{
    int i = 0;
    int j = 1;

    do{
        flag[i] = true;
        turn = j;

        while(flag[j] && turn == j);

        for(int i = 0; i < 5; i++)
                shared_array[i] = 1;

        printf("Process A is complte!\n");
        printf("Shared array's values are: ");
        for(int i = 0; i < 5; i++)
            printf("%d", shared_array[i]);
        printf("\n\n");

        sleep(5);

        flag[i] = false;

        sleep(3);
    } while(1);
}


void *process_b(void *arg)
{
    int i = 1;
    int j = 0;

    do{
        flag[i] = true;
        turn = j;

        while(flag[j] && turn == j);

        for(int i = 0; i < 5; i++)
                shared_array[i] = 2;

        printf("Process B is complte!\n");
        printf("Shared array's values are: ");
        for(int i = 0; i < 5; i++)
            printf("%d", shared_array[i]);
        printf("\n\n");

        sleep(10);

        flag[i] = false;

        sleep(3);
    } while(1);
}