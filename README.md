# 프로젝트 계획 이유
------------------------------------------------------------------------------------------
>주식매매를 직접 하다보면 HTS나 어플리케이션을 통해서 얻는 정보만으로는 만족하지 못할때가 많습니다.
>제가 직접 매매를 할 때도 직접 검색을 하거나 네이버 증권에서 정보를 얻어가기도 했습니다. (물론 지금은 매매를 하진않습니다😂😂)
>그래서 제 첫 프로젝트는 주식 매매를 하는 사람들에게 도움이 되는 무언가를 만들고 싶었고, 직접 매매를 하며 불편했던 점을 생각해보고 제작하게 되었습니다.
>
>그래서 해당 프로그램은 직접 네이버 증권에 들어가지 않더라도 정보를 얻을 수 있도록 하였고,
>자주 사용하는 기능을 위주로 크롤링을 하였습니다.
>또한, 텔레그램 챗봇을 버튼형 챗봇으로 구현하였기 때문에 사용자들이 좀 더 간편하게 조작하여 정보를 얻을 수 있습니다.

# 프로젝트를 시작하기 위해...
----------------------------------
1. finance_def.py를 위해 필요한 설치

+ Requests 설치
```
$ npm install requests
$ pip3 install requests
```
+ BeautifulSoup 설치
```
$ npm install BeautifulSoup4
$ pip3 install BeautifulSoup4
```
+ pandas 설치
```
$ npm install pandas
$ pip3 install pandas
```

2. telegram_bot 을 위해 필요한 설치

+ python-telegram-bot 설치
```
$ npm install python-telegram-bot
$ pip3 install python-telegram-bot
```

+ telegram 설치
```
$ npm install telegram
$ pip3 install telegram
```

# korean_finance 사용자 기능
--------------------------
[시작단계]
--------------------------
1. 시작하기 -> 해당 텔레그램 챗봇의 기능을 시작합니다.
    - CallbackQueryHandler를 통해 main 함수를 실행합니다.
  
2. 설명듣기 -> 해당 텔레그램 챗봇의 설명을 듣습니다.
    - CallbackQueryHandler를 통해 about 함수를 실행합니다.
    - 뒤로가기 버튼을 누르면 시작단계로 돌아갑니다.

[시작 이후]
--------------------------
1. 상승종목 -> 네이버 증권의 상승종목 Top 15를 보여줍니다.
  
2. 하락종목 -> 네이버 증권의 하락종목 Top 15를 보여줍니다.
  
3. 시총상위 -> 네이버 증권의 시총상위 Top 15를 보여줍니다.
  
4. 거래상위 -> 네이버 증권의 거래량 상위 Top 15를 보여줍니다.
  
5. 코스피
    - 코스피 지수 클릭 -> 현재 코스피 지수, 거래량, 거래대금, 장중 최고/최저, 52주 최고/최저를 보여줍니다.
    - 시황뉴스 클릭 -> 코스피 시황뉴스 Top 5를 보여줍니다.

6. 코스닥
    - 코스닥 지수 클릭 -> 현재 코스닥 지수, 거래량, 거래대금, 장중 최고/최저, 52주 최고/최저를 보여줍니다.
    - 시황뉴스 클릭 -> 코스닥 시황뉴스 Top 5를 보여줍니다.

7. 종목검색 -> /v 종목이름 을 입력합니다. 현재가격, 전일종가, 당일고가/저가, 거래량, 거래대금, 전일대비를 보여줍니다.

8. 뉴스 -> 뉴스의 제목과 링크를 띄워줍니다.
    - Today News
    - 시황·전망 Top 5
    - 기업·종목분석 Top 5
    - 해외 증시 Top 5
    - 채권·선물 Top 5
    - 공시·메모 Top 5
    - 환율 Top 5

# korean_finance 주요 기능

1. Inlinekeyboard
    - InlinekeyboardButton : 챗봇에 버튼을 생성해주는 기능. 내부 인자로는('명칭', callback_data='변수명')을 사용.
    - InlinekeyboardMarkup : 레이아웃을 구성하는 기능

2. CallbackQueryHandler
    - Telegram 콜백 쿼리를 처리하는 핸들러 클래스.
    - pattern : 테스트할 정규식 패턴, 콜백 또는 유형을 지정합니다.
    - 콜백쿼리핸들러를 사용하여 버튼을 눌러도 새로운 메세지가 나오는 것이 아닌, 해당 메세지 부분에서 내용변경
   
3. CommandHandler
    - 사용자가 직접 명령어를 입력하면 해당 명령을 처리하는 핸들러 클래스.

# 실행 화면

