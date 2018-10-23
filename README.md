# chat_project
Simple Chatting project

### Spec
* python3
* django
* django-rest-framework
* bootstrap 4
* jquery
* heroku

### Features
* [x] 유저등록
* [x] 로그인
* [x] 로그아웃
* [x] 내 채팅방 리스트 보기
* [x] 채팅방 상세보기
* [x] 메세지 보내기
* [x] 사용자 추가하기
* [x] 사용자 제거하기
* [ ] 대화 검색하기
* [ ] 실시간 메세지보기
* [ ] 링크 url일 경우 click 가능하게 하기.
* [ ] 읽지 않은 메세지 확인하기 
* [ ] 메세지 전송시 Task queue를 사용하여 메세지 내용 메일로 전달하기.
* [ ] frontend와 backend의 분리하기.
* [ ] docker-compose를 세팅해서 local환경과 production 환경 세팅 공통화 하기
* [ ] pytest를 통해서 unit test 코드 작성하기.

### Folder Structures
```bash
.
├── Procfile ## heroku config file
├── README.md
├── app ## default app
│   ├── __init__.py
│   ├── forms.py
│   ├── settings.py
│   ├── urls.py
│   ├── utils.py
│   ├── views.py
│   └── wsgi.py
├── db.sqlite3 ## local database
├── log ## heroku local log folder
│   └── development.log
├── manage.py
├── messengers ## messengers app
│   ├── __init__.py
│   ├── admin.py
│   ├── migrations  ## migration folder
│   │   ├── 0001_initial.py
│   │   ├── 0002_auto_20181023_0156.py
│   │   └── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── templates
│   │   └── rooms ## templates folder
│   │       ├── detail.html
│   │       ├── index.html
│   │       ├── javascript.html
│   │       ├── layout
│   │       ├── lib
│   │       ├── list.html
│   │       ├── modal.html
│   │       ├── nav.html
│   │       ├── sidebar.html
│   │       └── styles.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── requirements.txt ## python lib
├── runtime.txt ## python version
├── static  ## static files
│   ├── auth
│   │   └── style.css
│   └── messengers
│       ├── index.css
│       └── index.js
├── templates  ## template folder
│   └── app
│       ├── javascript.html
│       ├── join.html
│       ├── login.html
│       └── styles.html
└── users  ## custom user app
    ├── __init__.py
    ├── admin.py
    ├── migrations
    │   ├── 0001_initial.py
    │   └── __init__.py
    └── models.py
```

### VIEW URL PATH

* /: GET
    > 채팅 리스트가 보이는 페이지 API
* /login: GET, POST
    > GET 요청시 login 페이지가 로딩되고 POST 요청시에 login이 되며 완료 후에 `/` 으로 이동시키는 API
* /logout: GET
    > logout API
* /join: GET, POST
    > 회원 가입 API
* rooms: GET
    > 채팅 리스트가 보이는 페이지 API
* rooms/<<int:pk>>: GET
    > 해당 채팅방의 메세지를 볼수 있는 페이지 뷰

### API

* api/rooms/<<int:pk>>?: GET, POST
    > 채팅방의 리스트를 확인하고, 생성하는 API
* api/rooms/<<int:pk>>/users : POST, DELETE
    > 채팅방에 유저를 추가하거나 삭제시 사용하는 API
* api/messages/<<int:pk>>?: GET, POST
    > 채팅 메세지를 확인하고 생성하는 API

### Authentication
* django session authentication

### Test url
* https://hidden-escarpment-77819.herokuapp.com


### WARNING
* heroku를 dev 서버로 사용할 경우 nested template에 대해서 path를 잘 못찾는 에러 발생
    * 임시로 중첩된 template 사용 금지. 추후 수정
    * heroku에서 중첩된 template folder에 대한 `TemplateDoesNotExists` 오류 수정

### HOW TO
* 대화 검색하기
    * THINK: 
        * 메세지의 대한 검색의 경우 글자가 많아 질 경우 검색이 느려질수 있음. column에 Index를 건다 하더라도 글자수가 많은 경우 카테고라이징 안되어서 검색 속도에 차질이 생김.
        * 메세지에 index 할 경우 DB에 index에 대한 용량이 많이 생김.
    * SOLVE:
        * 메세지의 경우는 elasticsearch와 같은 검색 엔젠을 사용해서 메세지를 tokenizers를 사용해서 토큰별로 검색이 가능하도록 수정 https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-tokenizers.html#analysis-tokenizers
        * 추후에 더 느릴 경우 형태소 분석을 통해 조사와 같은 불필요한 데이터를 지워서 저장하는 방식으로 변경해서 검색 속도 개선.

* 실시간 메세지보기
    * THINK:
        * web socket을 사용해서 진행하면 connection을 계속 연결할수 있어서 좋을 것 같지만 지금 사용하는 django에서는 web socket을 지원하지 않음
        * web socket을 따로 구성 할 경우에 database에 대한 scheme 관리 필요.
    * SOLVE:
        * django에서 web socket을 사용하지 못하는대신 django-channel이란 프로젝트를 통해 django에서도 websocket을 쓸수 있는 형태 지원: **공부필요**
        * web socket과 django web server 사이에 api 통신을 통해서 database에 대한 access를 한곳에서 처리. => 이럴경우 API 통신 이기 떄문에 failover에 대한 처리 필요.
    
* 링크 url일 경우 click 가능하게 하기.
    * SOLVE:
        * django에 있는 custom filter 기능을 통해서 `wrapped_a_tag_url_filter` 필터를 생성해서 python url 정규식에 [ `http(s)?://(\S+)` ] 매치 되었을 경우 replace하는 방식으로 변경
* 읽지 않은 메세지 확인하기 
    * SOLVE:
        * 유저별로 room에 머무른 마지막 시간 (다른 방 선택시 기존방은 다른방 선택 한 시간이 마지막 시간)을 기록 해서 로그인 시에 room별로 message의 created_at과 비교해서 갯수를 보여줌
    
* 메세지 전송시 Task queue를 사용하여 메세지 내용 메일로 전달하기.
    * SOLVE:
        * python celery를 세팅해서 메세지 전송시 이메일로 보내지는 task 생성하기. BROKER로는 디폴트 세팅인 database 대신 rabbitmq나 redis를 사용.
        * 메일 서버의 경우 gmail 계정을 생성해서 google의 메일서버 사용.
