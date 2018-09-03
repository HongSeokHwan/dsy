## 상속의 단점과 Strategy Pattern

### 추상 클래스와 인터페이스
#### 추상 클래스
- 추상 클래스는 **클래스**의 일종
- 상속 받은 정보를 부모 클래스로부터 Look-up 하여 살펴봐야 하기 때문에 인터페이스 보다 비싼 연산
- 정수 / 멤버 / 정의되지 않은 메소 / 정의된 메소드를 지닐 수 있음
- 메소드와 멤버를 어느 접근제한자로든 설정할 수 있음
- 추상 클래스를 상속 받는 서브 클래스는 반드시 상속 받은 abstract method를 정의해주어야 함
    - cf) 추상 클래스 역시 다른 추상 클래스를 상속 받을 수 있는데 이 때는 부모 추상 클래스의 abstract method를 **반드시 정의해줄 필요는** 없음
- 서브 클래스는 한 번에 한 개의 추상 클래스만을 상속 받을 수 있음
- abstract method를 정의할 때 자식 클래스는 해당 method의 접근 제한자 level을 같거나 혹은 더 낮게 재설정할 수 있음
```
abstract class MotorVehicle
{
    int fuel;

    int getFuel()
    {
        return this.fuel;
    }

    abstract void run();
}

class Car extends MotorVehicle
{
    void run()
    {
        print("Wrroooooooom");
    }
}
```
<br>

#### 인터페이스
- 인터페이스는 일종의 **계약**이자 **빈 껍데기**. method들의 코드가 아닌 몸체만 존재하는 패턴과 같은 것
- 인터페이스는 단순히 이름들의 나열이기 때문에 아주 적은 CPU만을 소모. 따라서 Look-up 작업을 할 필요가 없음
- 정수 / 정의되지 않은 메소드를 지닐 수 있음
- 모든 메소드들은 public level로 정의되어야 함
- 인터페이스는 부모 인터페이스를 extend할 수 있는데 이 때 부모 인터페이스의 method를 구현할 필요 없음
    - 인터페이스는 method 구현이 불가하기 때문
- 서브 클래스는 한 번에 여러 개의 인터페이스를 사용할 수 있음
- 인터페이스를 사용하는 서브 클래스는 반드시 method를 같은 접근 제한 레벨인 public으로 정의해주어야 함
```
interface MotorVehicle
{
    void run();

    int getFuel();
}

class Car implements MotorVehicle
{
    int fuel;

    void run()
    {
        print("Wrroooooooom");
    }

    int getFuel()
    {
        return this.fuel;
    }
}
```
<br><br>

### 상속의 단점
- 상위 클래스 기능에 버그가 생기거나 기능의 추가/변경 등으로 변화가 생겼을 때 상위 클래스를 상속 받는 하위 클래스가 정상적으로 작동할 수 있을지에 대한 예측이 힘듬
    - 하위 클래스는 상위 클래스의 부분 집합이기 때문에
- 상속 구조가 복잡해질 수록 그 영향에 대한 예측이 힘들어짐
- 상위 클래스에서 의미 있었던 기능이 하위 클래스에서는 의미 없는 기능일 수 있음
- 하위 클래스는 반드시 상위 클래스로부터 물려 받은 기능들을 제공해야 함 + 하위 클래스에서 기능들이 추가됨
    - 기능 확장에 따라 상위 클래스에서 파생된 클래스들이 많아지고, 그 규모가 커짐에 따라 일관성 있게 작성하지 않은 클래스들에 대한 이해도는 점차 복잡해지고 사용에 어려움이 생길 수 있음
<br><br>

### Strategy Pattern
- 알고리즘군을 정의하고 각각을 캡슐화하여 교환해서 사용할 수 있도록 만듦
- 일반적으로 서브 클래스를 만드는 방법을 대신하여 유연성을 극대화시키는 용도로 사용
- Strategy Pattern에서 class의 행위와 그 알고리즘은 run time시 변경될 수 있음
- Strategy pattern에서 우리는 다양한 strategy를 나타내는 객체들과 수행하는 행위가 strategy에 따라 달라지는 context 객체를 생성
- Strategy 객체는 context 객체의 수행 알고리즘을 변경하는 역할 수행
<br>

- 인터페이스 생성
```
public interface Strategy {
    public int doOperation(int num1, int num2);
}
```
- 같은 인터페이스를 사용하는 concrete class들을 생성 (*concrete class: 지니고 있는 method들이 모두 정의되어 있는 class*)
```
public class OperationAdd implements Strategy{
    @Override
    public int doOperation(int num1, int num2){
        return num1 + num2;
    }
}

public class OperationSubstract implements Strategy{
    @Override
    public int doOperation(int num1, int num2){
        return num1 - num2;
    }
}

public class OperationMultiply implements Strategy{
    @Override
    public int doOperation(int num1, int num2){
        return num1 * num2;
    }
}
```
- Context 클래스 생성
```
public class Context{
    private Strategy strategy;

    public Context(Strategy strategy){
        this.strategy = startegy;
    }

    public int executeStrategy(int num1, int num2){
        return strategy.doOperation(num1, num2);
    }
}
```
- Strategy가 바뀔 때 마다의 변화를 보기 위해 main 함수에서 Context 클래스 사용해봄
```
public class StrategyPatternDemo{
    public static void main(String[] args){
        Context context = new Context(new OperationAdd());
        System.out.println("10 + 5 = " + context.executeStartegy(10, 5)); // 15

        context = new Context(new OperationSubstract());
        System.out.println("10 - 5 = " + context.executeStartegy(10, 5)); // 5

        context = new Context(new OperationMultiply());
        System.out.println("10 * 5 = " + context.executeStartegy(10, 5)); // 50
    }
}
```
<br>