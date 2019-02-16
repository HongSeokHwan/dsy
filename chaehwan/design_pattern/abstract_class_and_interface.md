# 추상 클래스와 인터페이스

문법 자체는 굉장히 간단하다. 대신 왜 필요하고 어떻게 활용하는지에 시간이 필요할 뿐이다.

# 추상 클래스

추상 메소드 : 선언만 있고 구현이 없는 메소드
추상 클래스 : 추상 메소드를 하나라도 가지고 있다면 추상 클래스
(java에서 추상 메소드와 추상 클래스는 abstract 키워드로 표시한다.)

원래 클래스는 클래스를 바탕으로 new 명령어로 인스턴스를 생성하는데 추상 클래스의 경우 객체를 생성할 수 없다. 
만약 객체를 생성한다면 내용이 없는 메소드를 가지게 되는 셈이기 때문에 의미가 없다. 그렇다면 왜 추상 클래스가 
필요한가? 

클래스는 원래 객체를 생성하기 위함이지만 객체를 생성하는 것만이 목적은 아니다. 다른 서브클래스를 정의하기 사용되는
것도 클래스의 중요한 목적 중 하나다. 추상클래스는 서브클래스를 정의하는데에만 사용이 된다. 실제 구현은 서브클래스에서
이루어진다.

예를 들면 Event라는 클래스가 있을 때 다음과 같이 Event 클래스를 상속받는 하위 클래스들이 있다.

OneDayEvent(딱 하루의 일)
DeadlineEvent(기한이 있는 일)
DurationEvent(특정 기간동안의 일)

이때 사실상 Event 클래스는 코드의 중복을 막기 위해 각 하위 클래스의 공통적인 부분을 담고 있을 뿐이고 실제로 그 클래스 자체가 
객체로 생성되어 사용될 일은 없다. 그리고 3개의 하위 클래스에 대해 isRelevant라는 해당 기간 또는 시점에 속하는지를 확인하는 
함수를 사용한다면? 각 클래스 내부에 내용을 구현해서 사용할 수 있을 것이다. 하지만 이들 공통의 부모인 Event 클래스 타입의 배열에서 객체를 관리하고 각 요소의 isRelevant 메소드를 호출한다면? 바로 오류다. Event 클래스에는 isRelevant 메소드가 정의되어 있지 않기 때문이다.
그러므로 실제로 Event 객체가 사용되지는 않지만 그래서 메소드도 호출되지 않지만 자식들이 가지는 공통의 메소드를 추상메소드로 내용 없이 선언해주는 것이다. 일종의 표시인 셈이다. 그러면 다른 자식 클래스를 선언할 때도 이와 같은 메소드를 포함해야 한다는 것도 알려주는 역할을 한다.

착각해서는 안되는 것은 추상 클래스는 선언부 즉 내용은 다 가지지만 구현부만 비워두는 것이다. 그래서 생성자 등을 모두 포함하고 있다. 미완성 설계도라는 말이 적절한 비유라고 볼 수 있다.

아래는 추상 클래스에 대한 훌륭한 설명글이다.

참고)

추상 클래스의 개념과 활용
출처 : http://egloos.zum.com/nix102guri/v/521733

java 다형성
출처 : http://freestrokes.tistory.com/75

# 인터페이스

추상 클래스는 추상 메소드를 하나라도 가지고 있으면 추상 클래스라고 한다. 그말은 추상 클래스 내부에는 추상 메소드 말고도 다른 추상 메소드가 아닌 일반적인 메소드가 있을 수 있다는 것이다. 인터페이스는 추상 클래스와 크게 다르지 않지만 추상 클래스의 극단적인 형태라고 볼 수 있다.

인터페이스 : 추상 메서드만을 가진 순수한 추상 클래스
(예외적으로 static final 데이터 멤버(상수)를 가질 수 있다. 여기서 final 이라는 말은 값을 변경할 수 없다는 말이다. 그래서 일반적으로 상수를 의미한다. C언어로 보면 #define이다.)

```java
public interface Payable{
    public double calcSalary();
    public boolean salaried();
    public static final double DEDUCTIONS = 25.5;
}

public class Professor implements Payable{
    ...
    public double calcSalary(){
        //
    }
    public boolean salaried(){
        //
    }
}
```

java에서 상위 클래스를 상속할 때 extends 키워드를 사용한다. 그리고 추상클래스의 경우 추상 메소드가 아닌 다른 메소드들도 포함하고 있기 때문에 extends 키워드로 상속 받는다. 그런데 인터페이스의 경우 추상 메소드만을 가지므로 실제 내부를 구현하라는 뜻으로 implements를 키워드로 사용한다.

인터페이스에서 잠시 벗어나서 정렬 알고리즘 중 bubble sort 생각해본다면 bubble sort는 정렬할 데이터에 따라 bubble sort의 로직이 달라지는 것은 아니다. 그런데 단지 자료형이 달라졌다는 이유만으로 bubble sort 자체를 매번 다시 구현해야 한다면 상당히 번거롭다고 할 수 있다. 이렇게 특정 데이터에 대해서만 사용 가능한 것을 generic하지 않다고 말한다. 반면, 어떤 데이터가 들어와도 대응 가능하다면 매번 구현할 필요가 없고, generic하다고 말할 수 있다. 이렇게 되면 코드의 재사용성이 향상된다.

어떻게 하면 그것이 가능할까? 만약 정렬을 한다면 그 데이터 자체는 크기가 비교가 가능하다는 것이다. 그렇다면 다음과 같이 인터페이스 선언이 가능하다.

```java
public interface Comparable{
    int compareTo(Object o);
}
// Comparable 인터페이스는 자바에 이미 정의되어 있다.
```

그리고 이미 정의한 버블 소트는 다음과 같이 수정이 가능하다.그리고 Shape 클래스 Comparable 인터페이스를 implements하면 수정한 generic한 버블 소트를 
적용하는 것이 가능하다.

```java
// before
public void bubbleSort(){
    for (int i = n; i > 0; i--){
        for (int j = 0; j < i; j++){
            if (shapes[j].computeArea() > shapes[j+1].computeArea()){
                Shape tmp = shapes[j]
                shapes[j] = shapes[j+1]
                shapes[j+1] = tmp
            }
        }
    }
}
// after
public void bubbleSort(Comparable[] data, int size){
    for (int i = n; i > 0; i--){
        for (int j = 0; j < i; j++){
            if (data[j].computeArea() > data[j+1].computeArea()){
                Shape tmp = data[[j]
                data[j] = data[j+1]
                data[j+1] = tmp
            }
        }
    }
}
```

인터페이스를 implements 하면 인터페이스도 그 클래스에 대해 상위 클래스처럼 동작하기 때문에 Comparable 타입의 객체가 담긴 배열열을 정렬하는 것은 이상할 것이 없다. 물론 어떤 규칙에 대해 버블 소트를 적용할 것인지 정해주어야 하기 때문에 Shape 클래스 내부에는 compareTo 메소드 내부가 구현되어 있어야 한다.

```java
public int compareTo(Object other){
    double myArea = computeArea();
    double yourArea = ((Shape)other).computeArea()
    if (myArea < yourArea) return -1;
    else if (myArea == yourArea) return 0;
    else return 1;
}
```

정리하면 인터페이스는 어떤 데이터가 갖추어야 할 기본 요건이 되는 것이다. 그리고 이 요건을 만족하면 generic하게 로직을 적용할 수 있게 되는 것이다.

참고)

java 인터페이스의 개념과 사용법
출처 : http://blog.naver.com/PostView.nhn?blogId=bahamutjin&logNo=90091427506

