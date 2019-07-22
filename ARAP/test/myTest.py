import configparser
import datetime
import unittest

from ARAPDao import ARAPDao


class MylTest(unittest.TestCase):
    def test1(self):
        config = configparser.ConfigParser()
        config.read("../config.ini")
        print(config.sections())
        port = config.get("Mysql", "port")
        print(int(port))

    def test2(self):
        arap = ARAPDao()
        # row = arap.add_payment("d63190d1-cecc-3aaa-b30f-3c843469b9eb", 10,
        #                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        # row = arap.add_receive("11c139c0-0f22-31f4-a880-25d30f0f1d61", 100,
        #                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        # re = arap.query_purchase_pay_remain("d63190d1-cecc-3aaa-b30f-3c843469b9eb")
        re = arap.query_sell_receive_remain("11c139c0-0f22-31f4-a880-25d30f0f1d61")
        print(re)

    def test3(self):
        _time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        _time = datetime.datetime.now()
        delta = datetime.timedelta(days=7)
        _time - delta
        print(_time > (_time - delta))

    def test4(self):
        rarp=ARAPDao()
        res = rarp.query_receive(None,4)
        print(res)
