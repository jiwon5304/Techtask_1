# TASK1


## Members
| 이름 | github                                    | 담당 기능      |
|-----|--------------------------------------------|------------ |
|박지원 |[jiwon5304](https://github.com/jiwon5304)   | 영화(리스트조회,상세조회,생성), 리뷰(생성,삭제,수정,조회), 리뷰추천(생성,삭제)|


## 사용 기술 및 tools
> - Back-End :  <img src="https://img.shields.io/badge/Python 3.8-3776AB?style=for-the-badge&logo=Python&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Django 4.0-092E20?style=for-the-badge&logo=Django&logoColor=white"/>&nbsp;
> - ETC :  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Github-181717?style=for-the-badge&logo=Github&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=Postman&logoColor=white"/>&nbsp;


## API
- [Postman Doc](https://documenter.getpostman.com/view/17234812/UVRAH6kt)


## 구현 기능

### 0. 사용자 생성 API
- 닉네임과 패스워드를 입력받아 회원가입을 진행합니다.
- 닉네임은 중복가입이 되지 않습니다.
- 패스워드는 유효성검사 후 bcrypt를 사용하여 암호화를 진행합니다.
- is_admin으로 관리자를 확인합니다.
- 로그인 성공하면 JWT 토큰을 발급합니다.

### 1. 영화 리스트 조회 API
- 로그인한 유저만 접근이 가능합니다.
- 기본 페이지네이션은 limit(10)&offset(0) 입니다.
- 장르검색값이 장르필드에 포함 & 개봉년도는 일치 & 검색어는 타이틀필드 포함을 기준으로 검색 및 필터링을 진행합니다.
- 장르 & 년도 & 검색어 입력이 동시에 진행되면 모두 만족하는(&조건)으로 조회합니다.
- rating 입력값이 up이면 평점이 낮은 것부터, down이면 높은 것부터, 입력값이 존재하지 않으면 id값 기준으로 정렬합니다.

### 2. 영화 상세 조회 API
- 로그인한 유저만 접근이 가능합니다.
- 영화 id를 기준으로 id(pk값), title, rating, genres, summary, review list(text)를 조회합니다.

### 3. 영화 생성 API
- 관리자만 영화 생성이 가능합니다.
- title, year, rating, genres, summary 를 입력받아 영화를 생성하고, 입력값이 하나라도 없을 시 에러를 반환합니다.
- 기본적으로 평점은 0.0 입니다.


### 4. 리뷰 상세조회 API
- 로그인한 유저만 접근이 가능합니다.
- 리뷰 id를 기준으로 id, text,rating,create_at을 조회합니다.
- 리뷰가 수정되었을 때를 고려하여 creat_at은 업데이트 된 시간으로 조회합니다.

### 5. 리뷰 생성 API
- 로그인한 유저만 접근이 가능합니다.
- 한 유저당 동일한 영화에 1개의 리뷰만 작성하도록 합니다.
- text, rating을 입력받아 리뷰를 생성하고, 입력값이 하나라도 없을 시 에러를 반환합니다.

### 6. 리뷰 수정 API
- 본인이 작성한 리뷰만 수정이 가능하도록 구현하였습니다.
- text, rating을 입력받아 리뷰를 수정하며, 입력값이 하나라도 없을 시 에러를 반환합니다.

### 7. 리뷰 삭제 API
- 본인이 작성한 리뷰만 삭제 가능하도록 구현하였습니다.
- 리뷰 id로 리뷰를 삭제합니다.

### 8. 리뷰 추천 생성 API
- 로그인한 유저만 접근이 가능합니다.
- 같은 댓글은 한 유저당 한번만 추천이 가능합니다.

### 9. 리뷰 추천 삭제 API
- 본인의 추천만 해제가 가능합니다.
- 리뷰 id로 추천 해제를 진행합니다.


### 10. 영화 정보 저장
- 해당 정보들 중 영화정보(title, year, rating, genres, summary)를 데이터베이스에 저장합니다.


## 설치 및 실행 방법
### Local 개발 및 테스트용

1. 해당프로젝트를 clone 하고, 프로젝트 폴더로 들어간다.
    ```bash
    git clone https://github.com/jiwon5304/tech_task_1.git
    cd techtask
    ```
    
2. 가상 환경을 생성하고 프로젝트에 사용한 python package를 받는다.
    ```bash
    conda create -n task python=3.8 
    conda actvate task
    pip install -r requirements.txt
    ```

3. 데이터베이스에 테이블을 생성한다.
    ```bash
    python manage.py migrate
    ```

4. 서버를 실행한다.
    ```bash
    python manage.py runserver 0:8000
    ```

## 폴더 구조
```bash
├── README.md
├── config
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── decorator.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── db.sqlite3
├── db_upload.py
├── manage.py
├── movielist.json
├── movies
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   └──__init__.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── my_settings.py
└── users
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── migrations
    │   ├── 0001_initial.py
    │   └── __init__.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    └── views.py

```


# Reference
- 본 과제는 저작권의 보호를 받으며, 문제에 대한 정보를 배포하는 등의 행위를 금지 합니다.
