import sqlite3

from encoo.logger import Logger

from ebank import constants as CONSTANTS
from ebank.utils import sfun as util
from ebank.utils.filesearch import FileSearch


class Factory:

    __logger = Logger("ebank factory")

    """（根目录）\(银行名称)\(日期)\[H|T]_网银账号_yyyyMMdd-yyyyMMdd[.xls|.pdf|.xlsx]
    """

    def __init__(self, trans_file):
        self.trans_file = trans_file
        self.bank_name = util.get_bankname(trans_file, CONSTANTS.BANK_NAME_IDX)

    def to_sqlite(self):
        '''判断该银行存在处理类'''
        if self.bank_name in CONSTANTS.BANK_TRANS_CLS.keys():
            class_name = CONSTANTS.BANK_TRANS_CLS.get(self.bank_name)
            module_meta = __import__(
                "ebank.trans", globals(), locals(), f"[{class_name}]")
            class_meta = getattr(module_meta, class_name)

            # 调用具体处理类
            class_meta(file_path=self.trans_file).to_sqlite()
        else:
            self.__logger.error(f"to_sqlite no cls for {self.bank_name}")

    @staticmethod
    def query_trans_bydate(start_date, end_date):
        try:
            conn = sqlite3.connect(CONSTANTS.SQLITE3_PATH)
            cur = conn.cursor()
            sql = CONSTANTS.SQL_QUERY_TRANS_BYDATE.format(start_date, end_date)
            cur.execute(sql)
            result = cur.fetchall()
            print(result)
            conn.commit()

            cur.close()
            conn.close()
        except Exception as ex:
            print(ex)


if __name__ == "__main__":
    Factory.query_trans_bydate("2023-02-10", "2023-02-10")
