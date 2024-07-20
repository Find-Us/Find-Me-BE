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

