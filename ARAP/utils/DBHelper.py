import pymysql
import threading
import configparser


class MyHelper(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    # x线程安全的单例模式
    def __new__(cls, *args, **kwargs):
        if not hasattr(MyHelper, "_instance"):
            with MyHelper._instance_lock:
                if not hasattr(MyHelper, "_instance"):
                    MyHelper._instance = object.__new__(cls)
        return MyHelper._instance

    def connection(self):
        try:
            config = configparser.ConfigParser()
            config.read("../config.ini")

            self.conn = pymysql.connect(host=config.get("Mysql", "host"),
                                        port=int(config.get("Mysql", "port")),
                                        user=config.get("Mysql", "user"),
                                        passwd=config.get("Mysql", "password"),
                                        db=config.get("Mysql", "db_name"),
                                        charset=config.get("Mysql", "charset"))
        except Exception as e:
            print(e)
        self.cls = self.conn.cursor()

    def free(self):
        self.cls.close()
        self.conn.close()

    def executeUpdate(self, sql, param=[]):
        try:
            self.connection()
            row = self.cls.execute(sql, param)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        finally:
            self.free()
        return row

    def executeQuery(self, sql, param=[]):
        try:
            self.connection()
            self.cls.execute(sql, param)
            result = self.cls.fetchall()
        except Exception as e:
            print(e)
        finally:
            self.free()
        return result
