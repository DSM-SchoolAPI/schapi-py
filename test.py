from unittest import TestCase as TC, main
import time

from schapi import SchoolAPI, Region


class APITestBase(TC):
    def setUp(self):
        self.api = SchoolAPI(Region.DAEJEON, 'G100000170')
        
        super(APITestBase, self).setUp()


class TestMeal(APITestBase):
    def test_monthly_menus(self):
        meals = self.api.get_monthly_menus(2018, 4)

        self.assertListEqual(
            meals[3].breakfast,
            ['기장밥', '어묵국', '비엔나푸실리볶음', '메추리알떡조림', '포도맛요거트', '배추김치']
        )

        self.assertListEqual(
            meals[3].lunch,
            ['기장밥', '순두부찌개', '닭봉데리야끼오븐구이', '실채도라지초무침', '견과류또띠아칩', '석박지']
        )

        self.assertListEqual(
            meals[3].dinner,
            ['기장밥', '청경채된장국', '영양돼지갈비찜', '도토리묵상추무침', '배추김치', '제주감귤쥬스']
        )

    def test_monthly_menus_memoization(self):
        before = time.time()
        self.api.get_monthly_menus(2018, 4)
        un_memoized = time.time() - before

        before = time.time()
        self.api.get_monthly_menus(2018, 4)
        memoized = time.time() - before

        self.assertLess(memoized, un_memoized * 0.0001)
        # 10000배 이상 빠름


if __name__ == '__main__':
    main()
