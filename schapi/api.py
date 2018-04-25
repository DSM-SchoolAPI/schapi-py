from enum import Enum
import ssl

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

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

