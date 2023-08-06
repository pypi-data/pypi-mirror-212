from m_mock import m_random
from m_mock.test_case.common_utils import execute


class TestDate:
    def test_date(self):
        execute("@date('%Y-%m-%d %H:%M:%S', '+1d')")
        execute("@date('%Y-%m-%d %H:%M:%S', '+24h')")
        # 格式化
        execute("@date('%Y年-%m月-%d日 %H时:%M分:%S秒', '+2mon')")
        execute("@date('%Y年-%m月-%d日 %H时:%M分:%S秒', '+2min')")
        print(m_random.m_date.date('%y-%m-%d', '-20d'))
        print(m_random.m_date.date())

    def test_time(self):
        print(m_random.m_date.time('', '+2sec'))
        print(m_random.m_date.time('', '+4sec'))
        execute("@time('', '+4sec')")
        execute("@time")

    def test_now(self):
        print(m_random.m_date.now('year'))
        print(m_random.m_date.now('month'))
        print(m_random.m_date.now('week'))
        print(m_random.m_date.now('day'))
        print(m_random.m_date.now('hour'))
        print(m_random.m_date.now('minute'))
        print(m_random.m_date.now('second'))
        execute("@now('year')")
        execute("@now('month')")
        execute("@now('week')")
        execute("@now('day')")
        execute("@now('hour')")
        execute("@now('minute')")
        execute("@now('second')")
        execute("@now()")
        # 格式化
        execute("@now('year','%Y年-%m月-%d日 %H:%M:%S')")
        # 格式化
        execute("@now('week','%Y年 %m月 %d日 %H:%M:%S')")

