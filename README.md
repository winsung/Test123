# Kakaopay 서버사전과제 Coupon Service REST API 개발

## Contents
* [개발 프레임워크](#ch-1)
* [문제](#ch-2)
* [문제해결 전략](#ch-3)
* [빌드 및 실행 방법](#ch-4)

### <a name="ch-1"></a>개발 프레임워크
````
 Python==3.7.6
 Flask==1.1.2
 flask-restplus==0.13.0
 Flask-JWT-Extended==3.24.1
 Flask-SQLAlchemy==2.4.3
 SQLAlchemy==1.3.17
 sqlite
````

### <a name="ch-2"></a>문제 
````
필수 문제
1. 랜덤한 코드의 쿠폰 N개 생성하여 DB에 보관하는 API 개발 [완료]
 => /coupon, POST, req_body={create_count}
2. 생성된 쿠폰중 하나를 사용자에 지급하는 API 개발 [완료]
 => /coupon, PUT, req_body{coupon_code, user_id}
3. 사용자에게 지급된 쿠폰을 조회하는 API 개발 [완료]
 => /coupon/bind_list, GET
4. 지급된 쿠폰중 하나를 사용하는 API 개발 (재사용 불가) [완료]
 => /coupon/use, POST, req_body={coupon_code}
5. 지급된 쿠폰중 하나를 사용 취소하는 API 개발 (취소쿠폰 재사용 가능) [완료]
 => /coupon/cancel/<coupon_code>, POST 
6. 발급된 쿠폰중 당일 만료된 전체 쿠폰 목록 조회 API 개발 [완료]
 => /coupon/expired-today, GET

선택 문제
7. 발급된 쿠폰중 만료 3일전 사용자에게 메세지 발송기능 구현 [완료]
 => Thread Timer 이용 24시간마다 만료 3일 전 조회 후 출력, 첫 구동시 1시간 단위로 날짜 변경을 확인하고 다음날로 이동시 24시간 Timer로 작동

제약 사항
8. 기능개발 [완료]
9. 단위 테스트 코드 개발 [부족한 완료]
10. README.md 추가 [완료]
11. JWT Token기반 API 이증 개발 및 Token 이용 호출 [완료]
 => 패스워드 bcrypt 저장 및 Authorization Bearer Header를 이용한 API 호출 구현
12. 100억개 이상 쿠폰 관리 저장 관리 구현 [미완료]
13. 10만개 이상 벌크 csv Import 기능 [미완료]
14. 대용량 트래픽을 고려한 시스템 구현 [미완료]
15. 성능테스트 결과 / 피드백 [미완료]
````

### <a name="ch-3"></a>문제해결 전략
````
1. 최대한 간단하게 시간을 안쓰는 방향으로 고려
2. 쿠폰코드는 uuid를 이용하여 생성 (kakaopay-xxxx-xxxx-xxxx-xxxx 형식)
3. 쿠폰의 상태는 CREATED, USED 만 존재
4. 쿠폰 테이블은 coupon_code, coupon_status, bind_user_id, expire_date 컬럼만 존재
5. 쿠폰 만료일은 생성일 +7 일
6. SQLAlchemy를 이용하여 sqlite로 DB 작성
7. 유저 부분도 user_id, password 컬럼만 존재. password는 bcrypt를 이용한 단방향 암호화 적용
8. flask_jwt_extended를 이용하여 jwt 연동
9. 원활한 테스트를 목적으로 swagger 연동위한 flask_restplus를 사용
10. access_token의 유지시간은 1일로 설정. 이유는 따로 refresh_token 구현까지 진행하지 않기 위해
11. 기본적으로 API Method는 생성시에 POST를 사용하였으나, 단일 주소에서 동작하는 update 부분에서도 POST를 사용.(use, cancel)
````

### <a name="ch-4"></a>빌드 및 실행 방법
````
1. 준비
 > $ virtualenv venv --python=3.7
 > $ source venv/bin/activate
 > $ pip install -r requirements.txt

2. 실행
 > $ python app.py

3. 테스트
 > $ python app.test.py

4. Swagger UI
 > http://localhost:5000
````
 
 
