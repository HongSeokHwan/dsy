#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <assert.h>
#include <stdatomic.h>


typedef struct thread_info{
    pthread_t thread_id;
    void* (*thread_function)(void*);
    void* args;
} thread_info;

typedef struct thread_info element;

//typedef int element;
//typedef int key;

typedef struct node{
    element data;
    struct node *prev;
    struct node *next;
} node;

typedef struct{
    node* head;
} list_head;

list_head* create_head(void){
    list_head* head_node;
    head_node = (list_head*)malloc(sizeof(list_head*));
    head_node->head = NULL;
    return head_node;
}

void insert(list_head* head_node, element data){
    node* new_node = (node*)malloc(sizeof(node));
    new_node->data = data;
    new_node->next = head_node->head;
    if (head_node->head != NULL){
        head_node->head->prev = new_node;
    }
    head_node->head = new_node;
    new_node->prev = NULL;
}

// item->data != id should be edited
node* search(list_head* head_node, pthread_t id){
    node* item = head_node->head;
    printf("thread_id : %d\n", (int)item->data.thread_id);
    while (item != NULL && item->data.thread_id != id){
        item = item->next;
    }
    return item;
}

void delete(list_head* head_node, pthread_t id){
    node* item = search(head_node, id);
    if (item->prev != NULL){
        item->prev->next = item->next;
    }
    else {
        head_node->head = item->next;
    }
    if (item->next != NULL){
        item->next->prev = item->prev;
    }
}

void traverse(list_head* head_node){
    node* temp;
    printf("list : (");
    temp = head_node->head;
    while (temp != NULL){
        printf("%d ", (int)temp->data.thread_id);
        temp = temp->next;
        if (temp != NULL){
            printf(", ");
        }
    }
    printf(") \n");
}

void enqueue(list_head* head_node, element data){
    node* new_node = (node *)malloc(sizeof(node));
    new_node->data = data;
    new_node->next = NULL;
    if (head_node->head == NULL){
        head_node->head = new_node;
    }
    else {
        node* temp;
        temp = head_node->head;
        while (temp->next != NULL){
            temp = temp->next;
        }
        temp->next = new_node;
    }

}

int is_empty(list_head* head_node){
    if (head_node->head == NULL){
        printf("list is empty\n");
        return 1;
    }
    else {
        return 0;
    }
}

element dequeue(list_head* head_node){
    node *front = head_node->head;
    element item;
    if (!is_empty(head_node)){
        item = front->data;
        head_node->head = head_node->head->next;
        free(front);
        return item;
    }
}

/*
void test_insert(){
    list_head* task_queue = create_head();
    insert(task_queue, 3);
    assert (task_queue->head->data == 3);
    insert(task_queue, 5);
    assert (task_queue->head->data == 5);
}

void test_delete(){
    list_head* task_queue = create_head();
    insert(task_queue, 3);
    insert(task_queue, 5);
    delete(task_queue, 3);
    node* result = search(task_queue, 3);
    assert (result == NULL);
    delete(task_queue, 5);
    result = search(task_queue, 5);
    assert (result == NULL);
}

void test_search(){
    list_head* task_queue = create_head();
    insert(task_queue, 3);
    insert(task_queue, 5);
    node* result = search(task_queue, 3);
    assert (result != NULL);
    result = search(task_queue, 5);
    assert (result != NULL);
}

void test_enqueue(){
    list_head* task_queue = create_head();
    enqueue(task_queue, 3);
    assert (task_queue->head->data == 3);
    enqueue(task_queue, 5);
    assert (task_queue->head->data == 3);
}


void test_dequeue(){
    list_head* task_queue = create_head();
    enqueue(task_queue, 3);
    enqueue(task_queue, 5);
    element result = dequeue(task_queue);
    assert (result == 3);
}

void test_list_operation(){
    test_insert();
    test_delete();
    test_search();
    test_enqueue();
    test_dequeue();
}
*/

void create_thread(pthread_t *thread, void *(*start_routine)(void *), void *args);

typedef struct {
    atomic_int value;
    list_head *thread_list;
} semaphore;

void initialize_semaphore(semaphore* S, int value){
    S->value = value;
    S->thread_list = create_head();
}

typedef struct arguments{
    semaphore S;
    list_head* task_list;
} arguments;

void set_arguments(arguments* args, semaphore S, list_head* task_list){
    args->S = S;
    args->task_list = task_list;
}

void acquire(semaphore* S){
    atomic_fetch_sub(&S->value, 1);
}

void release(semaphore* S){
    atomic_fetch_add(&S->value, 1);
}

void block(pthread_t thread_id){
    pthread_cancel(thread_id);
    printf("thread cancelled\n");
}

void wakeup(thread_info TCB){
    create_thread(&TCB.thread_id, TCB.thread_function, (void *)TCB.args);
    printf("thread restarted\n");
}

void wait(arguments* args, pthread_t thread_id){
    thread_info TCB;
    //search through the task_queue;
    node* result = search(args->task_list, thread_id);
    TCB = result->data;
    acquire(&args->S);
    if (args->S.value < 0){
        enqueue(args->S.thread_list, TCB);
        block(thread_id);
    }
}

void signal(semaphore* S){
    thread_info TCB;
    release(S);
    if (S->value <= 0){
        TCB = dequeue(S->thread_list);
        wakeup(TCB);
    }
}

void* thread_execution(void* data){
    pthread_t thread_id = pthread_self();
    printf("thread started\n");
    wait(data, thread_id);
    printf("waiting thread list : (");
    //arguments *args = (arguments *)data;
    //traverse(args->S.thread_list);
    printf(")\n");
    signal(data);
}

void test_thread_creation(int status){
    int success_status = 0;
    if (status != success_status){
        perror("thread creation failed");
        return;
    }
    printf("%d\n", status);
}

thread_info store_thread_info(pthread_t *thread, void *(*start_routine)(void *),
                              void *args){
    thread_info TCB;
    TCB.thread_id = (pthread_t)thread;
    TCB.thread_function = start_routine;
    TCB.args = args;
    return TCB;
}

void create_thread(pthread_t *thread, void *(*start_routine)(void *), void *args){
    thread_info TCB;
    int is_success = -1;
    TCB = store_thread_info(thread, start_routine, NULL);
    is_success = pthread_create(
            thread,
            NULL,
            start_routine,
            args
        );
    test_thread_creation(is_success);
}

int main(){

    list_head* task_queue = create_head();

    semaphore shared;
    initialize_semaphore(&shared, 5);

    pthread_t threads[10];
    arguments args;
    set_arguments(&args, shared, task_queue);
    for (int i = 0; i < 10; i++){
        create_thread(&threads[i], thread_execution, (void *)&args);
    }

    return 0;
}

