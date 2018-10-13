from unittest import TestCase as TC, main
import time

from schapi import SchoolAPI


class APITestBase(TC):
    def setUp(self):
        self.api = SchoolAPI(SchoolAPI.Region.DAEJEON, 'G100000170')
        
        super(APITestBase, self).setUp()


class TestMeal(APITestBase):
    def test_monthly_menus(self):
        meals = self.api.get_monthly_menus(2018, 10)

        self.assertListEqual(
            meals[1].breakfast,
            ['흰밥(쌀밥)', '소고기미역국', '떡갈비몽떡잠발라소스볶음', '야채계란말이', '사케이유산균요구르트', '깍두기']
        )

        self.assertListEqual(
            meals[3].breakfast,
            ['시리얼(혼합)', '우유', '어린잎채소샐러드/흑임자드레싱', '치킨너겟/소스', '미니크로와상']
        )

        self.assertListEqual(
            meals[3].dinner,
            ['낙지덮밥', '미소국', '층층이등심돈까스/소스', '콘야채샐러드', '파인애플', '배추김치']
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
