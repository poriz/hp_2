# HP2 (Hot Place List)
## 1. 프로젝트 개요
### 1) 프로젝트 소개
- **서울 공공 데이터 활용**
    : 서울시 공공데이터를 활용해 실시간 핫플레이스 장소의 인구밀도를 안내하는 서비스  
      서울시의 대표 명소 113군데의 인구밀도, 날씨, 미세먼지 등을 안내
- **명소의 현황 파악**
    : 현재 사람이 가장 많은 복잡한 명소와 사람이 적은 가장 한적한 장소를 정렬하여 서비스 이용자가 한눈에 명소의 현황을 파악
- **사용자 댓글 활성화**
    : 여러 사용자들이 실시간으로 핫플레이스에 대해 의견을 남길 수 있도록 댓글 입력란을 추가

### 2) 프로젝트 참여 인원
|이름|역할|Github주소|
|--|--|--|
|박단이|프론트(html/css)|https://github.com/Danee12|
|이영호|API, 백엔드, 디버깅, 시연 영상 녹화|https://github.com/mediwind|
|이우식|DB, 백엔드|https://github.com/yiReal|
|장태수|GIT 관리, 백엔드, 디버깅|https://github.com/poriz|
|황진민|API|https://github.com/hjm507|

## 2. 사용 기술 및 라이브러리
- Django & bs4
- Open API
- SQLite3 & ORM

## 3. 발생 Issue 해결 방법
1. OPEN API 응답
    1. 응답시간이 길어져서 데이터가 제대로 들어오지 않은 경우
        - 테스트 진행 시 데이터가 들어오는 최장시간이 30분이었기 때문에 AppSchduling을 사용하여 30분마다 API를 받아오도록 함.
    2. 데이터에 Null 값 존재
        - 예외 처리를 진행하여 데이터의 무결성을 확보

2. model migration 에러
    - 이미 존재하는 테이블 변경 과정에서 initial 파일에 이미 있기 때문에 에러가 났음
    - initial 파일을 수정함으로써 해결
  
## 4.결과 web
![Untitled](https://github.com/poriz/hp_2/assets/36216087/99d3f939-b4c1-4b1c-9b19-2d84ed128cb8)
