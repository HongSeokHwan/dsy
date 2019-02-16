#include <stdio.h>
#include <pthread.h>
#include <stdatomic.h>
#include <unistd.h>

atomic_int lock = 0;
int expected = 0;
int shared_resource = 5;

void acquire_spin_lock(){
   while (atomic_compare_exchange_weak(&lock, &expected, 1) != 0);
}

void release_spin_lock(){
    lock = 0;
}

void* acquire(void *data){
    acquire_spin_lock();
    printf("current: %d\n", shared_resource);
    printf("acquire thread entered\n");
    shared_resource--;
    printf("shared_resource: %d\n", shared_resource);
    release_spin_lock();
}

void* release(void *data){
    acquire_spin_lock();
    printf("current: %d\n", shared_resource);
    printf("release thread entered\n");
    shared_resource++;
    printf("shared_resource: %d\n", shared_resource);
    release_spin_lock();
}

void test_thread_creation(int status){
    int success_status = 0;
    if (status != success_status){
        perror("thread creation failed");
        return;
    }
    printf("%d\n", status);
}

int main(){
    pthread_t threads[2];
    int is_success = -1;
    is_success = pthread_create(
                &threads[0],
                NULL,
                acquire,
                NULL
            );
    test_thread_creation(is_success);
    is_success = pthread_create(
                &threads[1],
                NULL,
                release,
                NULL
            );
    test_thread_creation(is_success);
    return 0;
}
