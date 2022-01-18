import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import datetime
#사용자가 입력한 "종목명"을 company_code로 바꿔주는 클래스.
class Get_CompanyCode:
    def make_code(x):
        x = str(x)
        return '0' * (6-len(x)) + x

    def stock_list(company):
        stock_code = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]
        stock_code = stock_code[['종목코드', '회사명']]
        stock_code['종목코드'] = stock_code['종목코드'].apply(Get_CompanyCode.make_code)

        stock_code.rename(columns={'종목코드': 'code', '회사명': 'company'}, inplace=True)
        company_code = company
        code = stock_code[stock_code.company == company_code].code.values[0].strip()

        return code
#검색한 종목의 가격을 알려주는 클래스.
class Get_Price:
    def get_price_company(company_code, index):
        url = "https://finance.naver.com/item/main.nhn?code=" + company_code
        result = requests.get(url)
        bs_obj = BeautifulSoup(result.text, "html.parser")

        no_today = bs_obj.find("p", {"class": "no_today"})
        blind_now = no_today.find("span", {"class": "blind"})
        today_price = blind_now.text #현재가격
        
        no_yesterday = bs_obj.find("td", {"class": "first"})
        blind_yesterday = no_yesterday.find("span", {"class": "blind"})
        yesterday_price = blind_yesterday.text #전일가격

        table = bs_obj.find("table", {"class": "no_info"})
        trs = table.findAll("tr")
        first_tr = trs[0]
        first_tr_tds = first_tr.findAll("td")
        first_tr_tds_second_td = first_tr_tds[1]
        box1 = first_tr_tds_second_td.findAll("span")
        today_high = box1[1].text #당일고가

        second_tr = trs[1]
        second_tr_tds = second_tr.findAll("td")
        second_tr_tds_next_td = second_tr_tds[1]
        box2 = second_tr_tds_next_td.findAll("span")
        today_low = box2[1].text #당일저가

        third_tr_tds_third_td = first_tr_tds[2]
        volume = third_tr_tds_third_td.findAll("span")
        today_volume = volume[1].text #당일 거래량

        forth_tr_tds_td = second_tr_tds[2]
        deal_money = forth_tr_tds_td.findAll("span")
        today_money = deal_money[1].text #당일 거래대금

        up_down = bs_obj.find("p", {"class": "no_exday"})
        up_down_em = up_down.findAll("span")
        up_blind = up_down.findAll("span", {"class": "blind"})
        up_down_lists = []
        for idx, new in enumerate(up_down_em):
            up_down_list = new.get_text()
            up_down_list = re.sub("[\n]", "", up_down_list)
            up_down_lists.append(up_down_list)
        sign = ''
        if up_down_lists[1] == "상승":
            sign = '+'
        else:
            sign = '-'
        day_to_day_list = [up_down_lists[0] + " " + up_down_lists[2] + "(원)" + up_down_lists[1] + " " + sign + up_blind[1].text + "%"]
        upanddown = " ".join(day_to_day_list)
        # 총 7개(0~6) 리스트 배열
        list = [today_price, yesterday_price, today_high, today_low, today_volume, today_money, upanddown]

        return list[index]
# 네이버금융 메인페이지에 있는 TOP종목(거래상위, 상승, 하락, 시가총액 상위) 15개씩 보여주는 클래스.
class Top_Price:
    def get_bs_obj():
        url = "https://finance.naver.com"
        result = requests.get(url)
        bs_obj = BeautifulSoup(result.text, "html.parser")

        return bs_obj
    
    def today_high():
        bs_obj = Top_Price.get_bs_obj()
        top_price = bs_obj.find("div", {"class": "section_sise_top"})
        high_tbody = top_price.find("tbody", {"id": "_topItems2"})
        high_price = high_tbody.findAll("tr", {"class": "up"})
        
        high_list = []
        for i in range(0,15):
            basic_info = high_price[i].get_text()
            sinfo = basic_info.split("\n")
            high_list.append('{}.'.format(i+1) + "\t종목이름 : " + sinfo[1] + "\n\t현재가격 : " + sinfo[2] + "\n\t상승가격 : " + sinfo[3] + "\n\t상승퍼센트 : " + sinfo[4] + "\n\n")
        return " ".join(high_list)

    def today_low():
        bs_obj = Top_Price.get_bs_obj()
        top_price = bs_obj.find("div", {"class": "section_sise_top"})
        low_tbody = top_price.find("tbody", {"id": "_topItems3"})
        low_price = low_tbody.findAll("tr", {"class": "down"})

        low_list = []
        for i in range(0,15):
            basic_info = low_price[i].get_text()
            sinfo = basic_info.split("\n")
            low_list.append('{}.'.format(i+1)+ "\t종목이름 : " + sinfo[1] + "\n\t현재가격 : " + sinfo[2] + "\n\t하락가격 : " + sinfo[3] + "\n\t하락퍼센트 : " + sinfo[4] + "\n\n")
        return " ".join(low_list)

    def today_trade():
        bs_obj = Top_Price.get_bs_obj()
        top_price = bs_obj.find("div", {"class": "section_sise_top"})
        trade_tbody = top_price.find("tbody", {"id": "_topItems1"})
        trade_rank = trade_tbody.findAll("tr")

        rank_list = []
        for i in range(0,15):
            basic_info = trade_rank[i].get_text()
            sinfo = basic_info.split("\n")
            rank_list.append('{}.'.format(i+1)+ "\t종목이름 : " + sinfo[1] + "\n\t현재가격 : " + sinfo[2] + "\n\t변동가격 : " + sinfo[3] + "\n\t변동퍼센트 : " + sinfo[4] + "\n\n")
        return " ".join(rank_list)
    
    def today_money():
        bs_obj = Top_Price.get_bs_obj()
        top_price = bs_obj.find("div", {"class": "section_sise_top"})
        money_tbody = top_price.find("tbody", {"id": "_topItems4"})
        money_rank = money_tbody.findAll("tr")

        rank_list = []
        for i in range(0,15):
            basic_info = money_rank[i].get_text()
            sinfo = basic_info.split("\n")
            rank_list.append('{}.'.format(i+1)+ "\t종목이름 : " + sinfo[1] + "\n\t현재가격 : " + sinfo[2] + "\n\t변동가격 : " + sinfo[3] + "\n\t변동퍼센트 : " + sinfo[4] + "\n\n")
        return " ".join(rank_list)
#뉴스 클래스
class Get_News:
    def get_bs_obj():
        url = "https://finance.naver.com/news"
        result = requests.get(url)
        bs_obj = BeautifulSoup(result.text, "html.parser")
        return bs_obj

    def main_news():
        bs_obj = Get_News.get_bs_obj()
        news_area = bs_obj.find("div", {"class": "left01"})
        main_news_area = news_area.find("div", {"class": "main_news"})
        main_news_area_li = main_news_area.findAll("li")
        news_titles = []
        news_urls = []

        for idx, new in enumerate(main_news_area_li):
            news_title = new.get_text()
            news_title = re.sub("[\n]", "", news_title)
            news_titles.append('{}.'.format(idx+1) + news_title)
        for new in main_news_area.find_all("li"):
            news_url = new.find("a")["href"]
            news_urls.append(" "+"https://finance.naver.com/" + news_url + "\n\n")
        
        result = []
        for i, j in zip(news_titles, news_urls):
            result.append(i + j)
        return " ".join(result)

    def condition_news():
        bs_obj = Get_News.get_bs_obj()
        news_area = bs_obj.findAll("div", {"class":"summary_block"})
        market_list = news_area[0].find("ul")
        market_list_li = market_list.findAll("li")
        news_titles = []
        news_urls = []
        for idx, new in enumerate(market_list_li):
            news_title = new.get_text()
            news_title = re.sub("[\n\t]", "", news_title)
            news_titles.append('{}.'.format(idx+1) + news_title)
        for new in market_list_li:
            news_url = new.find("a")["href"]
            news_urls.append(" " + "https://finance.naver.com/" + news_url[:75] + "\n\n")
        result = []
        for i, j in zip(news_titles, news_urls):
            result.append(i + j)
        return " ".join(result)

    def analyze_news():
        bs_obj = Get_News.get_bs_obj()
        news_area = bs_obj.findAll("div", {"class":"summary_block"})
        market_list = news_area[1].find("ul")
        market_list_li = market_list.findAll("li")
        news_titles = []
        news_urls = []
        for idx, new in enumerate(market_list_li):
            news_title = new.get_text()
            news_title = re.sub("[\n\t]", "", news_title)
            news_titles.append('{}.'.format(idx+1) + news_title)
        for new in market_list_li:
            news_url = new.find("a")["href"]
            news_urls.append(" " + "https://finance.naver.com/" + news_url[:75] + "\n\n")
        result = []
        for i, j in zip (news_titles, news_urls):
            result.append(i + j)
        return " ".join(result)

    def overseas_news():
        bs_obj = Get_News.get_bs_obj()
        news_area = bs_obj.findAll("div", {"class": "summary_block"})
        market_list = news_area[2].find("ul")
        market_list_li = market_list.findAll("li")
        news_titles = []
        news_urls = []
        for idx, new in enumerate(market_list_li):
            news_title = new.get_text()
            news_title = re.sub("[\n\t]", "", news_title)
            news_titles.append('{}.'.format(idx+1) + news_title)
        for new in market_list_li:
            news_url = new.find("a")["href"]
            news_urls.append(" " + "https://finance.naver.com/" + news_url[:75] + "\n\n")
        result = []
        for i, j in zip(news_titles, news_urls):
            result.append(i + j)
        return " ".join(result)

    def bond_news():
        bs_obj = Get_News.get_bs_obj()
        news_area = bs_obj.findAll("div", {"class": "summary_block"})
        market_list = news_area[3].find("ul")
        market_list_li = market_list.findAll("li")
        news_titles = []
        news_urls = []
        for idx, new in enumerate(market_list_li):
            news_title = new.get_text()
            news_title = re.sub("[\n\t]", "", news_title)
            news_titles.append('{}.'.format(idx+1) + news_title)
        for new in market_list_li:
            news_url = new.find("a")["href"]
            news_urls.append(" " + "https://finance.naver.com/" + news_url[:75] + "\n\n")
        result = []
        for i, j in zip(news_titles, news_urls):
            result.append(i + j)
        return " ".join(result)

    def memo_news():
        bs_obj = Get_News.get_bs_obj()
        news_area = bs_obj.findAll("div", {"class": "summary_block"})
        market_list = news_area[4].find("ul")
        market_list_li = market_list.findAll("li")
        news_titles = []
        news_urls = []
        for idx, new in enumerate(market_list_li):
            news_title = new.get_text()
            news_title = re.sub("[\n\t]", "", news_title)
            news_titles.append('{}.'.format(idx+1) + news_title)
        for new in market_list_li:
            news_url = new.find("a")["href"]
            news_urls.append(" " + "https://finance.naver.com/" + news_url[:75] + "\n\n")
        result = []
        for i, j in zip(news_titles, news_urls):
            result.append(i + j)
        return " ".join(result)

    def rate_news():
        bs_obj = Get_News.get_bs_obj()
        news_area = bs_obj.findAll("div", {"class": "summary_block"})
        market_list = news_area[5].find("ul")
        market_list_li = market_list.findAll("li")
        news_titles = []
        news_urls = []
        for idx, new in enumerate(market_list_li):
            news_title = new.get_text()
            news_title = re.sub("[\n\t]", "", news_title)
            news_titles.append('{}.'.format(idx+1) + news_title)
        for new in market_list_li:
            news_url = new.find("a")["href"]
            news_urls.append(" " + "https://finance.naver.com/" + news_url[:75] + "\n\n")
        result = []
        for i, j in zip(news_titles, news_urls):
            result.append(i + j)
        return " ".join(result)
#코스피, 코스닥 클래스
class Kos:
    def kospi_main():
        url = "https://finance.naver.com/sise/sise_index.naver?code=KOSPI"
        result = requests.get(url)
        bs_obj = BeautifulSoup(result.text, "html.parser")
        kospi_main = bs_obj.find("div", {"class": "subtop_sise_detail"})
        kospi_main_div = kospi_main.find("div", {"id": "quotient"})
        kospi_price = kospi_main_div.find("em", {"id": "now_value"}) #현재 코스피 지수
        
        kospi_trade = kospi_main.findAll("td", {"class": "td"})
        kospi_trade2 = kospi_main.findAll("td", {"class": "td2"})   
        
        kospi_list = []
        kospi_list.append("현재 코스피 지수 : " + kospi_price.text + "\n\n거래량(천주) : " + kospi_trade[0].text + "\n\n거래대금(백만) : " + 
                        kospi_trade2[0].text + "\n\n장중최고 : " + kospi_trade[1].text + "\n\n장중최저 : " + kospi_trade2[1].text + "\n\n52주 최고 : " + 
                        kospi_trade[2].text + "\n\n52주 최저 : " + kospi_trade2[2].text)
        return " ".join(kospi_list)
    
    def kosdaq_main():
        url = "https://finance.naver.com/sise/sise_index.naver?code=KOSDAQ"
        result = requests.get(url)
        bs_obj = BeautifulSoup(result.text, "html.parser")
        kosdaq_main = bs_obj.find("div", {"class": "subtop_sise_detail"})
        kosdaq_main_div = kosdaq_main.find("div", {"id": "quotient"})
        kosdaq_price = kosdaq_main_div.find("em", {"id": "now_value"}) #현재 코스닥 지수

        kosdaq_trade = kosdaq_main.findAll("td", {"class": "td"})
        kosdaq_trade2 = kosdaq_main.findAll("td", {"class": "td2"})

        kosdaq_list = []
        kosdaq_list.append("현재 코스닥 지수 : " + kosdaq_price.text + "\n\n거래량(천주) : " + kosdaq_trade[0].text + "\n\n거래대금(백만) : " + kosdaq_trade2[0].text + 
                        "\n\n장중최고 : " + kosdaq_trade[1].text + "\n\n장중최저 : " + kosdaq_trade2[1].text + "\n\n52주 최고 : " + kosdaq_trade[2].text + 
                        "\n\n52주 최저 : " + kosdaq_trade2[2].text)
        return " ".join(kosdaq_list)

    def kospi_news():
        url = "https://finance.naver.com/sise/sise_index.naver?code=KOSPI"
        result = requests.get(url)
        bs_obj = BeautifulSoup(result.text, "html.parser")

        news_main = bs_obj.find("div", {"id": "contentarea"})
        news_main_1 = news_main.find("div", {"id": "contentarea_left"})
        news_main_div = news_main_1.find("div", {"class": "box_type_m"})
        news_main_li = news_main_div.findAll("li")
        news_titles = []
        news_urls = []
        
        for idx, new in enumerate(news_main_li):
            news_title = new.get_text()
            news_title = re.sub("[\n]", "", news_title)
            news_titles.append('{}.'.format(idx+1) + news_title)
        for new in news_main_div.find_all("li"):
            news_url = new.find("a")["href"]
            news_urls.append(" " + "https://finance.naver.com/" + news_url[:75] + "\n\n")
        result = []
        for i, j in zip(news_titles, news_urls):
            result.append(i+j)
        return " ".join(result)
    
    def kosdaq_news():
        url = "https://finance.naver.com/sise/sise_index.naver?code=KOSDAQ"
        result = requests.get(url)
        bs_obj = BeautifulSoup(result.text, "html.parser")

        news_main = bs_obj.find("div", {"id": "contentarea"})
        news_main_1 = news_main.find("div", {"id": "contentarea_left"})
        news_main_div = news_main_1.find("div", {"class": "box_type_m"})
        news_main_li = news_main_div.findAll("li")
        news_titles = []
        news_urls = []
        
        for idx, new in enumerate(news_main_li):
            news_title = new.get_text()
            news_title = re.sub("[\n]", "", news_title)
            news_titles.append('{}.'.format(idx+1) + news_title)
        for new in news_main_div.find_all("li"):
            news_url = new.find("a")["href"]
            news_urls.append(" " + "https://finance.naver.com/" + news_url[:75] + "\n\n")
        result = []
        for i, j in zip(news_titles, news_urls):
            result.append(i+j)
        return " ".join(result)