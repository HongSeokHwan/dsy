# Heap

완전 이진 트리
array로 구현 가능
A.heap_size 속성을 가짐
A[1]은 루트

parent 함수
left 함수
right 함수

최소 힙과 최대 힙이 있음

max_heapify
build_max_heap
max_heap_insert
heap_extract_max

# Piority Queue

insert
maximum
extract_max
increase_key

insert
minimum
extract_min
decrease_key

https://medium.freecodecamp.org/learning-to-test-with-python-997ace2d8abe

https://wikidocs.net/29

# 우선순위 큐란?

도로에서 차량의 우선순위
ex) 앰뷸런스

사례 : 
네트워크 패킷 중 네트워크 관리와 관련된 것은 우선순위
운영체제에서 시스템 프로세스는 응용 프로세스보다 우선 순위를 가짐

큐에 우선순위를 도입한 자료구조

스택과 큐와 비교 가능 (어떤 요소가 먼저 삭제되는가?))

컴퓨터의 여러분야에서 사용
ex) 
네트워크 트래픽 제어
운영체제에서의 작업 스케줄링
등

배열, 연결 리스트 등으로도 구현 가능하지만 힙으로 가장 효율적으로 구현 가능

연산 
insert
remove
find
isEmpty
isFull
display

우선순위를 변경하는 연산은? 

// 그저 대소 관계 말고 특정 기준에 의해 처리하도록 구현 가능할까?

힙을 사용하면 

O(logN)

힙 : 부모 노드의 키 값이 자식의 노드의 키 값보다 항상 큰 완전 이진 트리

(힙은 중복된 값을 허용한다.)

완전 이진 트리이기 때문에 중간에 비어 있는 요소의 값은 없다. 

프로그램의 구현을 쉽게 하기 위해 배열의 첫 번째 인덱스 0은 사용x 


