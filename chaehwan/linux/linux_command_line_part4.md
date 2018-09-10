# The Linux Command Line Part4 - 쉘 스크립트 작성

# Chapter24. 첫 번째 쉘 스크립트

매번 일일이 커맨드라인에서 사용하는 데에는 한계 있음
-> 설계한 프로그램에 커맨드라인 툴들을 모아놓으면 쉘이 스스로 복잡한 작업들을 순차적으로 수행
"shell script"

## 쉘 스크립트란?

* 쉘 스크립트 : 명령어들이 나열되어 있는 파일
* 쉘은 쉘 스크립트를 읽어서 마치 커맨드라인에 직접 명령어를 입력하여 실행하는 것처럼 수행
* 커맨드 라인에서 할 수 있는 작업 대부분 스크립트에서 가능하고, 스크립트에서 할 수 있는 작업
  역시 커맨드라인에서 가능

## 쉘 스크립트 작성 방법

1) 스크립트 작성
2) 스크립트 파일을 실행파일로 설정
* 시스템은 텍스트 파일을 프로그램으로 처리하지 않음
* 스크립트에 실행 권한을 줘야 함
3) 쉘이 접근할 수 있는 장소에 저장하기
* 쉘은 경로명을 명시하지 않아도 실행 가능한 파일들이
  존재하는 특정 디렉토리를 자동으로 검색
  -> 이 디렉토리에 저장하여 실행

### 스크립트 파일 포맷

```bash
#!/bin/bash

# This is our first script.

echo 'Hello world!' # THis is a comment too
```

* \# 기호 다음에 나오는 내용은 무시(주석)
* 첫 번째 줄은 그냥 주석이 아님 #!은 특별한 조합(shebang)
    * #!(shebang)은 뒤따라오는 스크립트를 실행하기 위한
    인터프리터의 이름을 시스템에 알려줌
    * 모든 쉘 스크립트의 첫 줄에는 shebang이 반드시 
    포함되어야 함

### 스크립트에 실행 권한 설정

```bash
ls -l hello_world

chmod 755 hello_world

ls -l hello_world
```

permission을 755로 주면 모든 사용자에게 실행 권한 주어짐

### 스크립트 파일 저장 위치

hello_world을 입력하면 스크립트가 실행되지 않는다. 스크립트에 문제가 있는 것이
아니라 위치에 문제가 있는 것이다. 어떤 명령어가 입력되었을 때 경로가 주어지지
않으면 시스템은 실행 프로그램을 찾을 때마다 특정 디렉토리 목록을 검색한다. 
ls 명령어를 입력할 때도 모든 경로를 탐색한 후 ls가 실행되는 것이 아니다. 
/bin 디렉토리는 시스템이 자동 검색하는 디렉토리 중 하나이므로 ls 명령어가 
입력될 때, 시스템이 /bin/ls 디렉토리를 실행된다. 이것이 PATH 환경변수와 시스템이
실행 프로그램을 검색하는 데 있어 하는 역할이다.

```bash
echo $PATH
```

위 명령어를 입력했을 때 출력되는 디렉토리 목록에 스크립트 파일이 저장되어 있다면
문제는 해결된다. 

PATH 변수에 디렉토리를 추가하거나 PATH 폴더에 등록되어 있는 디렉토리에 파일을 옮겨
주면 된다.

PATH 변수에 디렉토리를 추가하는 것은 .bashrc 파일에 내용을 추가해주면 된다.
이렇게 되면 새로운 터미널 세션이 시작될 때마다 설정이 적용된다. 바로 적용을 해주고
싶으면 sourcing을 해주면 된다.

```bash
. .bashrc
```

여기서 .은 source 명령어는 같은 의미다.

### 스크립트를 저장하기 좋은 장소

* ~/bin 디렉토리는 개인적인 용도로 사용하려는 스크립트를 저장하기에
적합한 장소임
* 시스템상의 모든 사용자가 접근 가능한 스크립트를 작성하는 경우에는 
/usr/local/bin에 저장한다.
* 시스템 관리자용 스크립트는 /usr/local/sbin 디렉토리에 저장한다.

## 기타 포맷 방법

* 중요한 스크립트를 작성할 때 주요 목표 중 하나가 바로 '유지보수의 용의성'
* 쉽고 이해하기 쉬운 스크립트!

### 확장 옵션명(long 옵션명)

ex)
ls -ad
->
ls --all --directory

동일한 의미이므로 스크립트 작성 시에는 되도록 확장형을
사용하는 것이 스크립트의 가독성을 높임

### 들여쓰기 및 문장 연결

* 스크립트 파일을 작성할 때 긴 명령어는 여러 줄에 구분하여 입력하는 것이
가독성을 확실히 높임
* 백슬래시로 여러 줄에 표현 가능함


# Chapter25. 프로젝트 시작하기

## 1단계 : 간단한 HTML 문서 만들기

* 유지보수를 위해 여러 번 등장하는 문자열은 하나의 변수로 나타내기
* 상수 : 값이 변하지 않는 변수 ex) $HOSTNAME
  * 쉘에서도 실제 값이 변하지 않도록 지정하는 것이 가능
    declare -r TITLE="Page Title"(r은 일기 전용이라는 뜻)
* 다른 프로그래밍 언어와 달리 쉘은 변수에 할당되는 값의 데이터 형식을
  고려하지 않고 모두 문자열로 인식
  * declare -i 로 정수 값으로 선언하는 것이 가능은 함(잘 사용하지 않음)
* 변수 할당문에는 빈칸이 없어야 함
* 변수를 확장할 때 중괄호를 사용하기도 함
  * mv $filename $filename1 -> 오류
  * mv $filename ${filename}1 -> 중괄호를 활용하여 1이라는 숫자가
  filename이라는 변수명의 일부가 아님을 쉘이 인식하도록 함

## Here 문서 

* echo 말고 here document 혹은 here 스크립트라고 하는 방법으로도 텍스트 출력 가능
* I/O 리다이렉션의 추가적인 형태로 텍스트 본문을 스크립트에 삽입할 때 그리고 
  명령어의 표준 입력으로 보낼 때 사용
* 형식 : command << token
         text
         token
* token은 반드시 단독으로 사용해야 하고 그 줄에 어떠한 빈칸도 허용되지 않는다.
* here document의 장점은 shell이 인식하는 따옴표 및 쌍 따옴표의 의미가 사라진다는
  것이다. 그래서 자유롭게 인용 부호를 사용할 수 있다.
* << 기호를 <<-로 바꾸면 쉘은 here 문서에서의 선행되어 나오는 탭 기호들을
  무시하게 됨 -> 가독성을 위해 들여쓰기 가능

# Chapter26. 하향식 설계

* 프로젝트의 규모가 커지고 복잡해질수록 유지보수가 쉽지 않아진다.
  -> 크고 복잡한 작업ㅇ르 작고 간단한 단위로 나누는 것이 좋다.
* 최상위 단계를 정의하고 이러한 단계들을 구체적으로 나누어가는 과정
  -> "하향식 설계"
* 함수를 정의하는 방법은 두 가지 방법이 있음

function name {
      commands
      return
}

또는

name() {
    commands
    return
}

* 지역변수는 앞에 local이라는 단어를 붙임으로써 정의 가능

# Chapter27. 흐름 제어 : if 분기

## if의 사용

if commands; then
    commands
[elif commands; then
    commands ...]
[else 
    commands]
fi

참고) 명령어들은 종료될 때 종료 상태라는 값을 생성
      0 -> 성공
      그 외의 숫자 -> 실패
여기서 종료 상태는 명령어를 입력한 다음 echo $?을 입력하면 
정수 결과값을 얻을 수 있다. 예를 들어 true를 입력하면
성공인 0 값을 return 하는 것을 알 수 있다.

## test의 사용

* if 명령어와 가장 흔하게 사용되는 명령어
* test expression 또는 [expression]

### 파일 표현식

* 파일의 상태를 나타내는 표현식
  ex) file1 -ef file2 : file1과 file2는 동일한 inode 번호를 가진다.

참고) $FILE 매개변수가 표현식 내에서 사용될 때는 따옴표로 인용됨

ex) if [ -d "$FILE"] ; then echo "$FILE is a directory"; fi

### 문자열 표현식

* 문자열을 검사하는 표현식
  ex) -z sting : string의 길이는 0이다.
  ex) string1 == string2 : string1과 string2는 같다.

ex) if [-z "$ANSWER" ]; then echo "There is no answer."; fi

### 정수 표현식

* 정수를 이용한 표현식
* ex) integer1 -eq integer2 : integer1과 integer2는 같다.

## 현대식 테스트

bash의 최신 버전에서는 test의 역할을 대신하는 합성 명령어를 지원한다.
형식 : [[expression]]
이 expression에는 아래와 같은 식이 들어간다.

string1 =~ regex 

string1이 확장 정규 표현식인 regex에 부합하면 참을 반환한다.

ex) if [[ "$INT" =~ ^-?[0-9]+$ ]]; then ...

## 정수 테스트

bash에서는 [[expression]] 뿐만 아니라 (()) 도 지원한다. 
(()) 은 산술식의 참 여부를 검사한다.

ex) if ((1)); then echo "It is true"; fi

## 표현식 조합

표현식은 논리 연산자를 이용함으로써 조합 가능

논리 연산           test            [[]], (())
AND                 -a                &&
OR                  -o                ||
NOT                 !                 !

ex) if [ $INT -ge $MIN_VAL -a $INT -le $MAX_VAL ]; then ...

## 제어 연산자 : 분기의 또 다른 방법

command1 && command2 : command1 과 command2가 모두 실행되면 command1이 성공했다는 의미
(comman1이 성공하면 command2 실행)

command1 || command2 : command1 과 command2가 모두 실행되면 command1이 실패했다는 의미
(comman1이 실패하면 command2 실행)

ex) mkdir temp && cd temp
temp 라는 디렉토리를 생성하고 성공하면 현재 작업 디렉토리를 temp로 바꾸라는 의미

ex) [-d temp] || mkdir temp
테스트가 실패하면 temp 디렉토리가 생성

[-d temp] || exit 1 
temp라는 디렉토리가 존재하지 않으면 스크립트는 종료 상태1을 반환하고 종료

# Chapter28. 키보드 입력 읽기

## read : 표준 입력에서 값 읽어오기

* 표준 입력으로 들어온 내용을 한 줄씩 읽어올 때 사용
* read [-options] [variable...]
* ex) read int : int 변수에 값이 입력된다.
* read var1 var2 var3  과 같이 여러 변수에 값을 할당하는 것도 가능
  -> 예상하는 값보다 더 적게 값을 입력 받으면 나머지 변수들을 빈 값으로 채운다.

참고) READ 명령어는 파이프라인과 함께 사용할 수 없다.
-> 파이프라인은 서브 쉘을 생성하는데 이 서브 쉘은 쉘과
쉘 환경에 대한 복사본으로 파이프라인으로 명령어를 실행할 때
사용된다. 
그리고 프로세스가 종료되면 해당 환경 복사본도 함께 삭제된다.
그러므로 서브 쉘은 부모 프로세스의 환경을 절대 변경하지 않음을
의미한다. read 명령은 환경의 일부가 되는 변수에 값을 할당하는데
그 명령이 종료되면 서브 쉘과 그 환경이 모두 사라지고 변수 할당에
대한 효력도 잃게 된다.

## IFS로 입력 필드 구분하기

IFS(입력 필드 구분자)
ex) 스페이스, 탭, 개행 문자

아래와 같은 방식으로 IFS를 설정해줄 수 있다.

IFS = ":"

# Chapter29. 흐름 제어 : while 루프와 until 루프

## while

* while문의 형식 : while commands; do commands; done 
* 명령어 목록의 종료 상태를 확인한다. 종료 상태가 0인 
  동안에는 루프 내의 명령어를 실행한다.

ex) 

```bash
while [ $count -le 5 ]; do
        echo $count
        count = $((count+1))
done
echo "Finished"
```

## 루프 탈출

break문을 사용한다.

ex)

```bash
if [[ $REPLY == 0 ]]; then
        break
fi      
```

## until

* while문과 다르게 0이 아닌 종료 상태를 만났을 때 루프를 종료하는 대신에
계속 수행된다.
* until 루프는 종료 상태 값으로 0을 받을 때까지 계속된다.

ex)

```bash
until [ $count -gt 5 ]; do
        echo $count
        count = $((count+1))
done
echo "Finished"
```

## 루프를 이용한 파일 읽기

done 구문 다음에 리다이렉션 연산자를 사용하면 된다.

ex) 

```bash
while read distro version release; do
    # ~
done < distros.txt
```

# Chapter30. 문제 해결

## 논리 오류

### 방어적 프로그래밍

예를 들어 아래와 같은 상황이라면?

```bash 
cd $dir_name
rm *
```

dir_name이 존재한다면 딱히 문제 될 것은 없다. 하지만 그렇지 않으면 cd 명령은 실패하고
다음 줄로 이동해서 현 작업 디렉토리의 모든 파일을 삭제한다.
서버의 중요한 부분을 망가뜨릴 수 있다.

```bash 
cd $dir_name && rm * 
```

위와 같은 방식으로 고치면 cd 명령이 실패하면 rm 명령이 실행되지 않는다. 하지만 
여전히 dir_name 변수가 설정되어 있지 않거나 비어 있으면 홈 디렉토리 파일들이 
삭제되는 결과를 얻게 될 수도 있다.

```bash 
[[ -d $dir_name ]] && cd $dir_name && rm *
```

이렇게 고쳐주는 것이 더욱 적절하다.

### 입력값 검증

프로그램이 입력을 받는 경우 일반적으로 좋은 프로그래밍 규칙은 어떤
입력 값이든 처리 가능해야 한다는 것이다.

꼭 유효한 입력만을 허용하도록 주의 깊게 확인해야 한다.

## 테스팅

### 스텁(stub)

스크립트 개발의 최초 단계에서 작업의 절차를 확인하기 위해 가치 있는
기법이다.

아직 개발되지 않는 코드를 대치해 작업의 절차를 확인하는 기법이다.

참고) 메소드 스텁 - 위키백과
출처: https://ko.wikipedia.org/wiki/%EB%A9%94%EC%86%8C%EB%93%9C_%EC%8A%A4%ED%85%81

### 테스트 케이스

효과적인 테스트를 위해 엣지 케이스(edge case) 와 코너 케이스(corner case)를 반영하여 
입력 데이터와 작동 상태를 주의 깊게 선택하는 것이 필요하다. 

## 디버깅

"문제" ? 프로그래머의 예상대로 수행되지 않는 스크립트를 의미한다.

### 문제 발생 지역 발견

긴 스크립트에서 문제가 되는 스크립트 영역을 종종 격리하는 게 유용하다.
코드 분리는 실제 원인에 대한 실마리를 제공한다.

코드를 격리시키는 데 쓰이는 한 가지 기법은 스크립트 일부를 주석화하는 것이다.
그러고 나서 버그에 영향을 주는 코드가 제거되었는지 다시 테스팅한다.

### 트레이싱

버그는 종종 스크립트 내의 예상치 못한 논리적 흐름인 경우가 있다.
ex) 스크립트의 일부가 전혀 실행되지 않거나 잘못된 시간 
    혹은 잘못된 순서로 실행되는 경우

프로그램의 실제 흐름을 보기 위해 "트레이싱(tracing)"이라는 기법을
사용한다.

트레이싱의 한 가지 방법은 스크립트 내에 실행 위치를 표시하는 정보
메세지를 포함시키는 것이다.
ex) echo "preparing to delete files" >&2

일반적인 출력과 그 메세지들을 구분하기 위해 표준 오류로 전달한다.

그리고 bash는 -x 옵션이나 set 명령어에 -x 옵션으로 트레이싱 방법을
제공한다.
ex) #!/bin/bash -x

이렇게 되면 트레이싱을 활성화하여 확장이 적용된 명령어를 볼 수 있다.

전체 영역이 아닌 특정 영역에 대해 시행하려면 

```bash
set -x # Turn on tracing 
# ~
# code 
# ~
set +x # Turn off tracing
```

set 명령어와 -x 옵션을 사용할 수 있다.

### 실행 중에 값 확인 

echo문으로 실행 중에 스크립트 내부 동작을 
확인할 변수의 내용을 표시하는 것도 유용한 방법이다.

# Chapter31. 흐름 제어: case 분기

## case 

case 명령어는 단어의 값을 확인하고 그 값과 일치하는 
패턴을 찾는다. 일치하는 패턴이 있으면 해당 패턴의 
명령들을 실행한다. 일치하는 패턴을 찾은 후에는
더 이상 패턴을 찾지 않는다.

### 패턴

case에서 사용한는 패턴은 경로명 확장에서 사용되는
패턴과 동일하다.
ex) a) : a 와 일치하는 단어
ex) ???) 정확히 세 글자로 이루어진 단어

### 패턴 결합

수직바를 구분자로 사용하여 여러 패턴을 결합하여 사용하는 것도 가능하다.
ex) q|Q)

ex)
```bash
case $REPLY in
      0)  echo "Program terminated"
          exit
          ;;
      1)  echo "Hostname: $HOSTNAME"
          uptime
          ;;
      # ...
esac
```

# Chapter32. 위치 매개변수

## 커맨드라인 항목 접근

* shell은 위치 매개변수라는 변수의 집합을 제공함
* 인자가 없는 경우에도 $0은 항상 커맨드라인의 첫번째 항목을 가지고 있음

### 인자 수 확인

* shell은 인자의 수를 넘겨주는 $#을제공함 

### shift : 다수의 인자에 접근

* shift 명령어는 실행될 때마다 각 매개변수가 하나씩 다음으로 이동하도록
  한다.

## 위치 매개변수 제어

* $* : 항목 1부터 시작하여 위치 매개변수 목록으로 확장된다. 이것을 쌍따옴표로 둘러싸면,
  쌍 따옴표 내의 문자열 모두가 위치 매개변수로 확장되고 각각 IFS 쉘 변수의 첫 번째 문자에
  의해 구분됨
* $@ : 항목 1부터 시작하여 위치 매개변수 목록으로 확장된다. 이것을 쌍따옴표로 둘럴싸면,
  각 위치 매개변수는 쌍 따옴표로 구분된 단어로 확장된다.

# Chapter33. 흐름 제어 : for 루프

* 반복 중에 작업 순서를 처리하는 수단을 제공한다는 점에서
  while과 until loop와 차이가 있음

## for : 전통적인 쉘 형식

for variable [in words]; do
      commands
done

ex)
```bash
for i in A B C D; do
    echo $i;
done
```

## for : C 언어 형식

for ((expression1; expression2; expression3 )); do
      commands
done

ex)
```bash
for (( i=0; i<5; i=i+1 )); do
        echo $i
done
```

# Chapter34. 문자열과 수

## 매개변수 확장

* 매개변수 확장은 커맨드라인보다 쉘 스크립트에서 주로 사용

### 기본 매개변수

```bash
a="foo"
echo "$a_file" # failed
echo "${a}_file" # executed
```

$a로 입력하면 그 변수가 가진 값으로 확장된다. 하지만 쉘이
혼동할 수 있는 다른 텍스트와 인접해 있다면 중괄호로 감싸주는
것이 필요하다.

### 빈 변수를 관리하기 위한 확장

* ${parameter:-word}
  parameter가 설정되지 않거나 비어 있다면, 이 확장 결과는 word
  ex) echo ${foo:-"substitute value if unset"}

* ${parameter:=word}
  parameter가 설정되지 않거나 비어 있다면, 이 확장 결과는 word
  ```bash
  foo=
  echo ${foo:="default value if unset"}
  \> default value if unset
  ```
* ${parameter:?word}
  parameter가 설정되지 않거나 비어있다면, 이 확장으로 오류가 발생하며
  스크립트는 종료될 것이다. 그리고 word의 값은 표준 출력으로 보내진다.
  ```bash
  foo=
  echo ${foo:?"paramter is empty"}
  bash: foo: parameter is empty
  ```
* ${parameter:+word}
  parameter가 설정되지 않거나 비어있다면, 아무런 결과를 표시하지 않는다.
  만약 parameter가 비어있지 않다면, parameter는 word값으로 대체된다.
  ```bash
  foo=
  echo ${foo:+"substitute value if unset"}
  ```
  
### 변수명을 반환하는 확장

* prefix로 시작하는 이미 존재하는 변수의 이름을 반환

```bash
echo ${!BASH*}
```

### 문자열 연산

* 문자열을 조작하기 위해 사용
* ex) ${#parameter} : 문자열의 길이로 확장

## 산술 연산

* $((expression)) : 산술 연산에 대한 확장의 기본 형태다.
* 기수 ex) 0xff, 기본 연산 5 / 2, 대입 foo = 5 등이 들어갈 수 있다.
* bc : 복잡한 연산이 필요하거나 부동소수점 연산이 필요할 때 사용한다.
  (bc 자체가 스크립트고 다양한 기능을 제공한다.)


# Chapter35. 배열

* 배열 : 하나 이상의 값을 가지고 있는 변수

```bash
a[1] = foo
echo ${a[1]}
```

## 배열에 값 할당

두 가지 방법
* name[subscript]=value
* name=(value1 value2 value3 ...)

```bash
days=(Sun Mon Tue Wed Thu Fri Sat)
```

## 배열 연산

### 배열의 모든 내용 출력 

첨자 *와 @는 배열의 모든 원소를 접근하는 데 사용 가능하다. @ 기호가 더 유용하다.

```bash
animals=("a dog" "a cat" "a fish")
for i in ${animals[@]}; do echo $i; done
```

### 배열 원소 수 확인

```bash
a[100]=foo
echo ${#a[@]} # number of array elements
echo ${#a[100]} # length of element 100
```

### 배열 끝에 원소 추가

```bash
foo = (a b c)
echo ${foo[@]}
foo += (d e f)
echo ${foo[@]}
```

### 배열 삭제

배열을 삭제하려면 

```bash
foo = (a b c d e f)
echo ${foo[@]}
unset foo
echo ${foo[@]}
```

원소를 삭제하려면

```bash
foo = (a b c d e f)
echo ${foo[@]}
unset 'foo[2]'
echo ${foo[@]}
```

참고) bash의 man 페이지에서 array를 검색하면 도움말을 확인할 수 있다.

# Chapter36. 그 외 유용한 툴들

## 그룹 명령과 서브쉘

* bash에서 명령어들을 그룹화하여 함께 사용할 수 있는 방법 2가지
  * 그룹 명령
    {command1; command2; [ command3; ...]}
  * 서브쉘
    (command1; command2; [ command3; ...])
* 두 방식의 차이점은 그룹 명령은 중괄호, 서브쉘은 괄호를 사용한다는 것이다.
* 중괄호의 경우 반드시 스페이스로 명령어와 구분되어야 하고 마지막 명령어는 중괄호가
  닫히기 전에 세미콜론이나 개행으로 끝나야 한다

## 리다이렉션 수행

* 그룹 명령과 서브쉘은 중요한 차이점은 있지만 모두 리다이렉션을 조절하기 위해 사용된다.

```bash
ls -l > output.txt
echo "Listing of foo.txt"
cat foo.txt >> output.txt
```

위의 내용을 아래와 같이 사용할 수 있다.

```bash
{ ls -l; echo "Listing of foo.txt"; cat foo.txt; } > output.txt
```

파이프라인과 함께 사용하면 강력할 수 있다.

```bash
{ ls -l; echo "Listing of foo.txt"; cat foo.txt; } | lpr
```

### 프로세스 치환

* 그룹 명령은 그 명령들을 현재 쉘에서 실행하지만 서브쉘은 현재 쉘의 복사본인
  자식 쉘에서 명령을 수행한다는 것이 차이다.
  그래서 서브쉘이 종료될 때 복사된 환경도 사라진다. 그리고 서브쉘의 환경에서 
  발생한 모든 변경된 부분들도 사라진다.
  (파이프라인의 명령어는 항상 서브쉘에서 실행된다.)
* 이러한 문제를 해결하기 위해 쉘은 프로세스 치환이라는 개념을 제공한다.
  두 가지 방식으로 표현할 수 있는데 표준 출력을 생성하는 프로세스인 경우
  <(list)
  또는 표준 입력을 가져오는 프로세스인 경우
  \>(list)
  이고 list는 명령어들의 목록을 나타낸다.
  ex) echo <(echo "foo")

## 비동기 실행

* 하나 이상의 작업을 수행할 때 적합
* 비동기 실행을 도와주는 빌트인 명령어 : wait
* ex) wait $pid

## 네임드 파이프(Named Pipes)

* 특수한 종류의 파일을 생성할 수 있다.
* 두 프로세스를 연결하기 위해 사용되고 다른 종류의 파일들처럼 
  파일로써 사용 가능하다.

```bash
mkfifo pipe1
ls -l pipe1
```

사용하는 방법은

```bash
ls -l > pipe1
cat < pipe1
```

첫 명령어를 입력하면 멈춘 것처럼 보인다. 이유는 파이프 말미에
아무런 데이터를 받지 못했기 때문이다. 이러한 현상을 파이프가 
블록되었다고 하는데 프로세스를 끝에 붙이는 것이 해결이 가능하다.
두 번째 명령어를 입력해주면 입력을 읽어들이기 시작해서 
첫 번째 터미널에서 생성된 디렉토리 목록은 두 번째 터미널에서
cat 명령의 출력으로 나타난다.