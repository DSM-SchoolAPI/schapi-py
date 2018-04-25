from enum import Enum
from functools import lru_cache
import ssl

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

from .datastructure import Meal

_url = 'http://{0}/sts_sci_md00_001.do?schulCode={1}&schulCrseScCode=4&schulKndScScore=04&schYm={2}{3:0>2}'


class Region(Enum):
    SEOUL = 'stu.sen.go.kr'
    BUSAN = 'stu.pen.go.kr'
    DAEGU = 'stu.dge.go.kr'
    INCHEON = 'stu.ice.go.kr'
    GWANGJU = 'stu.gen.go.kr'
    DAEJEON = 'stu.dje.go.kr'
    ULSAN = 'stu.use.go.kr'
    SEJONG = 'stu.sje.go.kr'
    GYEONGGI = 'stu.cbe.go.kr'
    KANGWON = 'stu.kwe.go.kr'
    CHUNGBUK = 'stu.cbe.go.kr'
    CHUNGNAM = 'stu.cne.go.kr'
    JEONBUK = 'stu.jbe.go.kr'
    JEONNAM = 'stu.jne.go.kr'
    GYEONGBUK = 'stu.gbe.go.kr'
    GYEONGNAM = 'stu.gne.go.kr'
    JEJU = 'stu.jje.go.kr'


class SchoolAPI:
    def __init__(self, region, school_code):
        """
        Args:
            region (Region)
            school_code (str)
        """
        self.region = region.value
        self.school_code = school_code

    def _get_ssl_context(self):
        context = ssl._create_unverified_context()

        return context

    def _get_menu_dict(self, data):
        daily_menus = re.findall('[가-힇]+\(\w+\)|[가-힇]+', data)

        menu_dict = dict()
        timing = [menu for menu in daily_menus if re.match('[조중석]식', menu)]
        # 조식, 중식, 석식 중 있는 데이터만

        for i in range(len(timing)):
            if i + 1 >= len(timing):
                # 마지막 메뉴
                menu_dict[timing[i]] = daily_menus[daily_menus.index(timing[i]) + 1:]
            else:
                menu_dict[timing[i]] = daily_menus[daily_menus.index(timing[i]) + 1: daily_menus.index(timing[i + 1])]

        return menu_dict

    def _dict_to_menu_list(self, menu_dict, keyword):
        try:
            return menu_dict.pop(keyword)
        except KeyError:
            pass

    @lru_cache()
    def get_monthly_menus(self, year, month):
        """
        Inquire monthly school meals

        Args:
            year (int) : Year to inquire
            month (int) : Month to inquire

        Returns:
            list: Monthly meal list
        """
        menus = [Meal()]

        context = self._get_ssl_context()
        resp = urlopen(_url.format(self.region, self.school_code, year, month), context=context)

        soup = BeautifulSoup(resp, 'html.parser')

        for data in [td.text for td in soup.find(class_='tbl_type3 tbl_calendar').find_all('td') if td.text != ' ']:
            meal = Meal()

            if len(data) > 1 and data != '자료가 없습니다':
                menu_dict = self._get_menu_dict(data)
                meal.breakfast = self._dict_to_menu_list(menu_dict, '조식')
                meal.lunch = self._dict_to_menu_list(menu_dict, '중식')
                meal.dinner = self._dict_to_menu_list(menu_dict, '석식')

            menus.append(meal)

        return menus
