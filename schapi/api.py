from enum import Enum
from functools import lru_cache

import aiohttp
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

from .datastructure import Meal

_url = 'https://{}/sts_sci_md00_001.do?schulCode={}&schulCrseScCode={}&schulKndScScore=0{}&schYm={}{:0>2}'


class SchoolAPI:
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

    class Type(Enum):
        KINDERGARTEN = 1
        ELEMENTARY = 2
        MIDDLE = 3
        HIGH = 4

    def __init__(self, region, school_code, type=Type.HIGH):
        """
        Args:
            region (Region)
            school_code (str)
        """
        self.region = region
        self.school_code = school_code
        self.type = type

    def _get_formatted_url(self, year, month):
        return _url.format(self.region.value, self.school_code, self.type.value, self.type.value, year, month)

    def _get_menu_dict(self, data):
        daily_menus = re.findall('[가-힇]+\(\[가-힇]+\)|[가-힇]+', data)

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

    def _get_menus_from_soup(self, soup):
        menus = [Meal()]

        for data in [td.text for td in soup.find(class_='tbl_type3 tbl_calendar').find_all('td') if td.text != ' ']:
            meal = Meal()

            if len(data) > 1 and data != '자료가 없습니다':
                menu_dict = self._get_menu_dict(data)
                meal.breakfast = self._dict_to_menu_list(menu_dict, '조식')
                meal.lunch = self._dict_to_menu_list(menu_dict, '중식')
                meal.dinner = self._dict_to_menu_list(menu_dict, '석식')

            menus.append(meal)

        return menus

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
        resp = urlopen(self._get_formatted_url(year, month))
        soup = BeautifulSoup(resp, 'html.parser')

        return self._get_menus_from_soup(soup)

    @lru_cache()
    async def get_monthly_menus_async(self, year, month):
        async with aiohttp.ClientSession() as session:
            async with session.get(self._get_formatted_url(year, month)) as res:
                resp = await res.text()
                soup = BeautifulSoup(resp, 'html.parser')

                return self._get_menus_from_soup(soup)

    def tabulate(self, year):
        for month in range(1, 13):
            self.get_monthly_menus(year, month)
