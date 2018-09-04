# The Linux Command Line Part1 - Learning the Shell

# Introduction에 나오는 인상 깊은 문장들

"Freedom is the power to decide what your computer does, and the only way to have this freedom is to know 
what your computer is doing. Freedom is a computer that is without secrets, one where everything can be known 
if you care enough to find out."

"It's been said that “graphical user interfaces make easy tasks easy, while command line interfaces make difficult 
tasks possible” and this is still very true today."

# Chapter1. What is a Shell?

Shell을 영어사전에 검색하면 조개껍데기, 껍질과 같은 뜻이 나온다. 이는 운영체제의 동작을 통제하는
프로그램인 커널의 외부 형태이기 때문이다. 쉽게 말하면 사용자가 운영체제와 소통하기 위한 인터페이스라고
생각하면 된다. 꼭 Command line의 형태이어야 하는 것은 아니고 Graphical한 형태일 수도 있다. 
커맨드 라인이라면 간단하게 keyboard 입력을 받아서 os가 실행한다고 생각해도 무관하다.

## terminal 형태

User@ComputerName:

@ 앞의 User 자리에 현재 사용자의 이름이 들어가고 ComputerName 자리에 컴퓨터이름이 들어간다. 

## Command history

터미널에서 윗쪽 화살표 키를 입력하면 기존에 입력했던 명령어들을 확인할 수 있다. 계속 눌러보면
기존에 입력했던 명령어들이 하나씩 보이는 것을 볼 수 있다. 그리고 다시 아래쪽 화살표를 누르면
입력했던 명령어 다음에 입력했던 명령어를 볼 수 있다. Command history 즉 명령어 이력을 확인할 
수 있다.

## 간단한 명령어들

date : 현재 날짜와 시간을 출력한다.
cal : 달력 형태로 날짜와 시간을 보여준다.
df : 디스크의 빈 공간을 확인할 수 있다.
free : 메모리의 빈 공간을 확인할 수 있다.
exit : 종료

df, free와 같은 명령어들에서 굉장히 편하게 현재 컴퓨터의 정보를 파악할 수 있다는 것을 느낄 수 있다.

## 가상 콘솔

# Chapter2. Navigation

리눅스에서는 어떻게 파일 시스템을 옮겨 다닐 수 있을까?

중요한 명령어는 pwd, cd, ls이다.
* pwd(print working directory)
* cd(change directory)
* ls(list directory contents)

어떤 말의 약어인지 파악하면 감이 온다.

리눅스의 파일 시스템은 트리의 형태를 띄고 있다. 윈도우와 다르게 하나의 트리, 하나의 계층적 구조를 가진다.
저장장치와 상관이 없다. 저장장치는 관리자의 의도에 따라 붙였다(mount) 떼어냈다가 할 수 있을 뿐이다.

처음 리눅스 파일 시스템을 익히는 입장에서는 트리 형태의 미로라고 생각하면 된다. 트리의 어디쯤 위치하고
있는지 알고 싶을 때 사용하는 명령어가 pwd다. 즉 현재 위치하고 있는 디렉토리를 확인할 수 있다.

pwd(print working directory)

cf) 처음 log in을 하면 home directory에서 시작한다. 각 계정마다 home directory가 있고 그 디렉토리가
그 User가 쓰기 작업을 할 수 있는 유일한 공간이다.

어떤 가지가 붙어있고 어디로 갈 수 있는지 확인하는 명령어가 ls이다. 어떤 디렉토리와 연결되어 있는지
확인할 수 있다.

ls(list directory contents)

그리고 실제로 옮겨가는 명령어가 cd다. 

cd(change directory)

cd (pathname)

pathname 자리에 옮겨갈 경로의 이름을 넣어주면 된다. 

이 때 경로의 이름을 적어주는 2가지 방법이 있는데 바로 절대경로와 상대경로다.

두 경로의 차이는 기준이 무엇인가 하는 것이다. 

먼저, 절대경로는 root directory를 기준으로 한다. root directory는 트리의 가장 상단에 위치하는
디렉토리를 말한다. 그래서 절대경로를 사용해서 디렉토리를 옮기려면 root directory에서부터 옮기려는
디렉토리명이나 파일명까지 입력해주면 된다.

```bash
cd /usr/bin
```

위의 /usr/bin에 가장 앞에 오는 / (슬래시 기호)는 root directory를 뜻한다. 그래서 root 디렉토리 하위의
 usr 디렉토리 하위의 bin 디렉토리로 이동하겠다는 뜻이다.

두번째, 상대경로는 기준이 현재 작업하고 있는 디렉토리가 된다. 

```bash
cd .
cd .. 
```

.(점/dot)은 현재 작업하고 있는 디렉토리를 말한다. 
..(점점/dotdot)은 현재 작업하고 있는 디렉토리의 바로 상위 디렉토리를 말한다.
그래서 위 명령어는 현재 디렉토리라는 명령어 그리고 상위 디렉토리로 이동하라는
뜻이 된다.

```bash
cd ./bin
cd bin
```

그리고 위 명령어에서 cd ./bin 즉 현재 디렉토리의 하위 디렉토리인 bin 디렉토리로 이동하라는 명령어는
./ 을 생략하고 사용하는 것이 가능하다.

cf) 도움이 되는 단축키들

```bash
cd ~ 
cd -
cd ~user_name
```
위 명령어는 위에서부터 
cd ~ : home directory로 이동하라
cd - : 이전에 작업하던 디렉토리로 이동하라
cd ~user_name : user_name에 해당하는 사용자의 home directory로 이동하라

cf) 리눅스 파일 시스템에서의 주의사항
* 파일명에 .(점/dot)이 붙는 경우 숨김 파일이다. 즉 ls 명령어를 입력해도 안 보인다.
  ls -a를 입력하면 된다.
* 리눅스는 대소문자를 구분한다.
* Linux는 파일 확장자 개념이 없다!
  어떻게 이름을 지어도 상관 없지만 응용프로그램의 경우 대개 확장자명을 붙인다.
* 파일명에 스페이스를 넣지 말도록 한다. 나중에 후회한다. _(underscore)를 사용하도록 한다.
  리눅스 파일시스템에서 따로 막지는 않지만 사용하지 않는 것이 좋다. 확인해보니 공백 이전까지만
  파일명을 인식한다. ex) test space -> test

