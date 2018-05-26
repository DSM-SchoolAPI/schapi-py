# schapi-py
## Build Status
[![CircleCI](https://circleci.com/gh/DSM-SchoolAPI/schapi-py.svg?style=svg)](https://circleci.com/gh/DSM-SchoolAPI/schapi-py)

## 설치
```
$ pip install schapi
```

## Guide
아래는 **2018년 4월 3일 대덕소프트웨어마이스터고등학교 조식**을 출력합니다.
```
from schapi import SchoolAPI

api = SchoolAPI(SchoolAPI.Region.DAEJEON, 'G100000170')

meals = api.get_monthly_menus(2018, 4)

print(meals[3].breakfast)
# ['기장밥', '어묵국', '비엔나푸실리볶음', '메추리알떡조림', '포도맛요거트', '배추김치']
```

학교 타입의 기본값은 고등학교로 설정되어 있고, 다른 타입으로 설정하려면 SchoolAPI의 세 번째 파라미터로 Enum 클래스인 Type의 필드 중 하나를 전달하면 됩니다.

```
from schapi import SchoolAPI

api = SchoolAPI(SchoolAPI.Region.***, '***', SchoolAPI.Type.KINDERGARTEN)
```
