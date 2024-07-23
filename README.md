# Find-Me-BE
Backend

## 파트
1. 로그인 파트 (+마이페이지) - 정재
2. 커뮤니티 파트 - 성민
3. 추천 파트 - 영빈

## 작명 형식
- apple => Apple
- give up => Give Up

## 기능 명세서
1. 사용자 인증
- 회원가입: 이름, 생년월일, 닉네임, 아이디, 비밀번호, 비밀번호 확인, 이메일(+ 통신사 인증)
- 로그인: 아이디, 비밀번호
- 로그아웃: 로그인 된 상태였을 때 가능

2. 마이 페이지
- 닉네임: 회원가입시 작성한 닉네임
- 그림: 레벨에 맞는 그림을 불러오는 기능
- 레벨: 사용자에 레벨 정보를 불러오는 기능
- 자기소개: 자기소개 (짧게 50자 정도) 작성 기능, 작성된 자기소개 정보 불러오는 기능
- 북마크 기능: 테스트 결과 창에서 북마크한 컨텐츠를 불러오는 기능

3. 커뮤니티
- 포스트 작성: 로그인 된 사용자에 한해서 제목, 내용을 입력하여 작성 가능 (사진도 가능하면 ㄱㄱ)
- 포스트 불러오기: 로그인 된 사용자에 한해서 다른 사용자들이 쓴 포스트 들을 보여주는 기능
- 포스트 삭제: 자신이 작성한 글을 삭제할 수 있는 기능
- 댓글 불러오기: 로그인 된 사용자에 한해서 포스트에 달린 댓글을 불러오는 기능
- 댓글 기능: 로그인 된 사용자에 한해서 포스트에 댓글을 달 수 있는 기능
- 추천 기능: 로그인 된 사용자에 한해서 게시글 당 한번씩 추천을 누를 수 있음

4. 추천
- 기능: 프론트에서 넘겨준 결과값에 따라서 해당되는 데이터들을 넘겨주기, 북마크 기능



## API 명세서
#### 추천 컨텐츠 점수 기반 그룹 선정
- URL: /Recommend/
- Method: POST
- 설명: scores 배열을 받아 각 그룹(A,B,C,D)의 합을 계산하고 최대 점수를 가진 그룹을 선정함. 점수가 동일한 경우 랜덤으로 그룹을 선택함.
- Request Body: json형태 { "scores": [integer, integer,...,integer] // 12개의 정수 배열}
- Response: json형태 {"result": "A" | "B" | "C" | "D" //A = 외로움, B = 지침, C = 짜증남, D =  즐거움}


#### 추천 컨텐츠 제공
- URL: /Recommend/Content/
- Method: POST
- 설명: keyword로 받은 그룹(A,B,C,D)에 따라 추천 컨텐츠를 제공함. content_type에 따라서 영화, 책, 노래, 또는 모든 컨텐츠를 무작위로 반환함.
- Request Body: json형태 
{
    "keyword": "A" | "B" | "C" | "D", 
    "content_type": "movie" | "book" | "song" | "all" // 요청할 컨텐츠 유형
}
- Response: json형태
{
    "movies": [
        {
            "id": "int",
            "title": "string",
            "actors": "string",
            "description": "string",
            "image": "url"
        },
    ],
    "books": [
        {
            "id": "int",
            "title": "string",
            "author": "string",
            "description": "string",
            "image": "url"
        }
    ],
    "songs": [
        {
            "id": "int",
            "title": "string",
            "singer": "string",
            "image": "url"
        }
    ]
}


#### 컨텐츠 저장
- URL:/Recommend/Save/
- Method: POST
- 설명: 주어진 데이터를 기반으로 컨텐츠를 저장함.
- Request Body: json 형태
{
    "nickname": "string", // 사용자의 닉네임
    "content_type": "string", // "movie", "book", "song" 중 하나
    "title": "string",
    "actors": "string (optional)", // 비어있어도 됨
    "author": "string (optional)", // 얘도
    "singer": "string (optional)", // 얘도
    "description": "string (optional)", // 얘도
    "image_url": "string (optional)"
}
- Response: json 형태
{
    "message" : "Content saved successfully"
}


#### 저장된 컨텐츠 조회
- URL: /Recommend/Get_saved/<str:nickname>/
- Method: GET
- 설명: 주어진 닉네임으로 저장된 모든 컨텐츠를 반환함.
- Response: json 형태
[
    {
        "nickname": "string",
        "content_type": "string",
        "title": "string",
        "actors": "string",
        "author": "string",
        "singer": "string",
        "description": "string",
        "image_url": "string"
    }
]


#### 저장된 컨텐츠 삭제
- URL: /Recommend/Delete/
- Method: DELETE
- 설명: 주어진 닉네임과 타이틀을 기반으로 컨텐츠를 삭제함.
- Request Body: json 형태
{
    "nickname": "string",
    "title": "string"
}
- Response: json 형태
{
    "message": "해당 컨텐츠를 삭제하였습니다."
}
