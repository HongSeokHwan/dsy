#include <stdio.h>
typedef struct 
{
    // 0 = ready, 1 = blocked
    int status = 0;
} process;

typedef struct
{
    int value;
    struct process *L;
} semaphore;


int main()
{
    semaphore
}

void init()
{

}

void P(semaphore)
{
    S.value--;

    if(S.value < 0)
    {
        //add this process to S.L
        // block();
    }
}


void S(semaphore)
{
    S.value++;

    if(S.value <= 0)
    {
        //remove a process P from S.L
        // wakeup(P)
    }
}