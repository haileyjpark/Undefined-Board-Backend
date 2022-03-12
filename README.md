# Board_Project



## 개발기간 
2022/03/01~진행중


## 팀원
 
**_FE_** : [유환석](https://github.com/GrassHopper42/undefined)




**_BE_** : 박정현




 
## 서비스 소개
 
> 게시판 미니 프로젝트 입니다.


## 기술 스택
 
Front-End : TypeScript, React.js


 
Back-End : Python, Django, DRF, MySQL, Miniconda, AWS RDS, AWS EC2


 
## 협업 툴
Common : Git, Github, Jira, Notion



## 구현 사항

> * 카카오 소셜 로그인
> * 게시글 조회, 등록, 수정, 삭제
> * 게시글 카테고리 필터링
> * 게시글 검색 기능 (태그를 이용한 검색, 키워드를 이용한 검색)
> * 쿠키를 사용한 게시글 조회수 중복 방지 
> * 댓글 & 대댓글 조회, 등록, 수정, 삭제
> * 댓글 & 게시글 좋아요





## Project Structure


 ```bash
 .
├── Board
│   ├── __init__.py
│   ├── __pycache__
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── README.md
├── board_project.pem
├── core
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   ├── models.py
│   ├── tests.py
│   ├── utils.py
│   └── views.py
├── manage.py
├── postings
│   ├── __init__.py
│   ├── __pycache__
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── __init__.py
│   │   └── __pycache__
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── requirements.txt
├── secrets.json
├── update-readme.sh
├── users
│   ├── __init__.py
│   ├── __pycache__
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── __init__.py
│   │   └── __pycache__
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── token.py
│   ├── urls.py
│   └── views.py
└── virtualenv
    ├── bin
    │   ├── activate
    │   ├── activate.csh
    │   ├── activate.fish
    │   ├── easy_install
    │   ├── easy_install-3.6
    │   ├── pip
    │   ├── pip3
    │   ├── pip3.6
    │   ├── python -> python3
    │   └── python3 -> /usr/bin/python3
    ├── lib64 -> lib
    ├── pyvenv.cfg
    └── share
 ```
