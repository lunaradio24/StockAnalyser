import requests
from bs4 import BeautifulSoup

# NAVER 증권 > 시가총액 사이트에서 html을 txt로 받아서 BeautifulSoup을 이용하면 parser로 lxml을 이용해 분석을 쉽게 해준다.
url = "https://finance.naver.com/sise/sise_market_sum.nhn?page=1"
res = requests.get(url)
soup = BeautifulSoup(res.text, 'lxml')

# 해당 페이지에 나와있는 talbe에서 상위 50개 기업 이름을 받아온다.
stockTop50_corp = soup.find("table", attrs={"class": "type_2"}).find("tbody").find_all("a", attrs={"class": "tltle"})

# 각 기업에서 얻고자 하는 정보
ParamList = ['매출액', '영업이익', '당기순이익', 'ROE(지배주주)', 'PER(배)', 'PBR(배)']


def getDataOfParam(param, sub_soup):
    """위의 ParamList에 있는 각 param을 받아서 sub_soup의 table에서 그 param 해당하는 row를 찾아 출력한다.

    Args:
        param ([type]): [description]
        sub_soup ([type]): [description]

    Returns:
        [type]: [description]
    """
    sub_tbody = sub_soup.find("table", attrs={"class": "tb_type1 tb_num tb_type1_ifrs"}).find("tbody")
    sub_title = sub_tbody.find("th", attrs={"class": param}).get_text().strip()

    # param에 매핑되는 row 검색 => 상위 이동 => 해당 row의 모든 td 컬럼 가져오기
    dataOfParam = sub_tbody.find("th", attrs = {"class":param}).parent.find_all("td")

    # dataOfParam에 있는 row를 list [ ]로 저장
    value_param = [i.get_text().strip() for i in dataOfParam]
    
    # param과 그에 해당하는 value_param을 출력 
    print(sub_title, " : ",value_param)

    return value_param 


for index, stock in enumerate(stockTop50_corp):

    # stockTop50_corp에 들어있는 stock 이름 출력
    print('\n')
    print(index+1, ".", stock.text)

    # 해당 stock의 "href" 속성값을 가져와 finance.naver.com에 이어붙인 link로 request와 BeautifulSoup 실행
    link = "https://finance.naver.com/"+stock["href"]       # a tag 내에서 "href" 속성값을 가져온다.
    sub_res = requests.get(link)                            # 링크를 통해 우리가 원하는 기업별 데이터 페이지 데이터 크롤링
    sub_soup = BeautifulSoup(sub_res.text, 'lxml')

    # 해당 stock의 table에서 최근 4년 연간실적, 분기실적의 시기를 text로 가져와 출력
    sub_thead = sub_soup.find("table", attrs={"class":"tb_type1 tb_num tb_type1_ifrs"})
    if sub_thead is not None:
        sub_thead = sub_thead.find("thead").find_all("th", attrs={"scope":"col", "class":""})
    print("연간/분기 실적 : ", [i.get_text().strip() for i in sub_thead])
    
    # 해당 stock에서 함수 getDataOfParam를 실행
    for idx, pText in enumerate(ParamList):

        param = " ".join(sub_soup.find('strong', text=pText).parent['class'])
        value_param = getDataOfParam(param, sub_soup)





