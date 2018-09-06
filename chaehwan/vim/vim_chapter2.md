# The vimrc File and Vim runtime directories

## vimrc

vim은 굉장히 커스터마이징하기가 쉽다. 핵심은 vimrc 파일에 있다.
먼저 :help vimrc로 도움말을 먼저 확인해보자.

운영체제별로 파일의 이름과 위치를 확인할 수 있다. vimrc 파일이 
시작될 때 load 되서 초기화되는 파일이다. 그러므로 우리는 vimrc
파일에 설정한 설정대로 작업하는 것이 가능하다. 그냥 설정 파일일
뿐이다. 만약 우리가 파일을 하나 만들어서 source하면 똑같은 방식으로
동작한다.

:help source를 입력해보자. source는 파일에서 명령어를 읽어서 실행하는
명령어다. 그러므로 별도의 파일을 만들고 source 명령어를 적용하면 같은
효과라고 볼 수 있다.

vimrc 파일에는 주석을 달아주는 것이 좋다. 본인이 나중에 보기도 좋고
협업에도 도움이 된다.

## runtime path

vim을 커스터마이징할 때 꼭 이해해야 하는 것 중 하나가 runtime path다.
굉장히 중요하다. 먼저 :h 'runtimepath' 로 도움말을 먼저 확인하도록  하자. 
도움말 내용 중 아래와 같이 나오는 부분이 runtimepath의 구조다.

This is a list of directories which will be searched for runtime
files:
          filetype.vim  filetypes by file name |new-filetype|
          scripts.vim   filetypes by file contents |new-filetype-scripts|
          autoload/     automatically loaded scripts |autoload-functions|
          colors/       color scheme files |:colorscheme|
          compiler/     compiler files |:compiler|
          doc/          documentation |write-local-help|
          ftplugin/     filetype plugins |write-filetype-plugin|
          indent/       indent scripts |indent-expression|
          keymap/       key mapping files |mbyte-keymap|
          lang/         menu translations |:menutrans|
          menu.vim      GUI menus |menu.vim|
          pack/         packages |:packadd|
          plugin/       plugin scripts |write-plugin|
          print/        files for printing |postscript-print-encoding|
          spell/        spell checking files |spell|
          syntax/       syntax files |mysyntaxfile|
          tutor/        files for vimtutor |tutor|

:set runtimepath를 입력하면 runtimepath를 확인할 수 있다.

어떤 시스템을 활용할 때 세 가지 정도의 방법이 있다. 첫째, 그냥 시스템의 default값을
사용하는 방법 그리고 두 번째, 설정 값을 바꾸어서 사용하는 방법, 세 번째, 아예 시스템 
내부의 파일을 수정하는 방법이다. 

vim을 사용할 때 세 번째 방법은 상당히 위험하다. 그리고 vim은 굳이 세 번째 방법을 택하지
않아도 되도록 설계가 되어 있다. 그냥 홈 디렉토리에서 모든 작업을 할 수 있다. 홈 디렉토리 
내부의 

## rtp

# Vim Modes Introduction

mode는 다른 IDE와 비교했을 때 Vim이 가지는 큰 차이점 중 하나다. 그리고 굉장히 강력하다.

:help intro를 입력한 다음 5장으로 가면 mode에 대한 설명을 볼 수 있다.

그렇게 중요한 것은 아니지만 command mode는 normal mode를 말하고,
command line mode는 하단에 :이 생기는 명령을 입력하는 모드를 말한다.

만약 insert 모드에 있고 지금 딱 하나의 명령을 내리고 싶고 싶다면
ctrl + o 를 누르면 조금 더 빠르다. insert Normal 모드라고 하는데 
insert 모드로 작업하다가 normal 모드에서의 명령을 딱 하나 내리고 싶으면 
ctrl + o를 누르면 된다. 예를 들어 한 칸 밑으로 내려가기 위해 j를 누르는
등의 상황에 사용 가능하다.

# Insert Mode 

먼저 :help insert.txt로 insert에 대한 도움말을 확인해도록 하자.

## 단축키에 대한 도움말 확인하기

:h i_CTRL-A

i를 접두어로 주고 단축키에 대해 help 명령을 입력하면 insert모드에서의 단축키를
확인할 수 있다.

CTRL-A : 이전에 삽입한 내용을 삽입한다.
CTRL-W : 단어 단위로 내용이 삭제된다. 굉장히 유용하다.
CTRL-T : 탭 크기만큼 해당 라인을 뒤로 밀어준다. 
CTRL-D : 탭 크기만큼 밀었던 라인을 다시 앞으로 당겨온다. 
(일반 모드면 창을 내리는 명령어지만 삽입 모드이므로 다르게 적용된다.)
CTRL-V : CTRL-V를 입력하면 다음에 입력하는 문자는 문자 그대로 그 내용이 삽입된다.
(CTRL+V를 입력하고 Tab을 입력하면 expandtab 옵션이 있더라도 Tab이 삽입된다.)

## insert 모드에서의 옵션

insert 모드에는 다양한 옵션이 있다.

1) textwidth

대개 80으로 설정하고 꼭 global setting(전역 설정)일 필요는 없다.

2) expandtab

프로그래머에겐 중요한 설정이다. tab 대신 space가 삽입되도록 한다.
진짜 tab을 입력하려면 ctrl + v 를 입력한 다음 tab 을 입력하면 된다.

## ins-special-special(Special special keys)

먼저 :help ins-ins-special을 입력한다.
도움말을 확인해보면 ins-ins-special은 insert 모드이지만 ins-ins-special
이라면 잠시 insert 모드를 멈추고 명령을 실행했다가 다시 돌아가는 명령을 말한다.
예를 들어 화살표 키의 경우 insert 모드이더라도 이동이 가능하다.

## ins-completion(insert mode completion)

vim에 있는 굉장히 유용한 기능 중 하나다.
자동 완성 기능이다. 

CTRL + N : 단어를 입력하다가 CTRL + N을 누르면 전방으로 일치하는 단어를 목록으로 보여준다.
다른 IDE에서 옵션을 켜면 자동으로 목록을 보여주는 것처럼 CTRL + N을 누르면 목록이 보여지고 
목록 중 화살표로 선택해서 엔터를 치면 된다.

CTRL + P : 단어를 입력하다가 CTRL + P을 누르면 후방으로 일치하는 단어를 목록으로 보여준다.

complete 옵션을 설정하면 더욱 원하는대로 커스터마이징이 가능하다.

CTRL + X + CTRL + L : CTRL + N 그리고 CTRL + P 처럼 자동 완성을 보여주는데 단어 단위가 아니라
전체 명령 한 줄 단위로 보여준다.

CTRL + X + CTRL + F : 파일 이름을 자동 완성해준다.

# gvim --remote-silent

gvim(GUI)을 사용한다면 위의 명령어를 통해서 외부 명령어를 실행할 수 있다.

# Destruction is good

# Using a Vim macro to edit Many Files 

참고) Practical Vim 요약 - 매크로
출처 : https://nolboo.kim/blog/2017/02/10/practical-vim/

# Vim macros and Global Commands



참고)
손에 잡히는 Vim - 김선영 저자
Vim Videos - Derek Wyatt 
밤앙개의 vim 강좌 
https://m.blog.naver.com/PostList.nhn?blogId=nfwscho&categoryNo=45&logCode=0