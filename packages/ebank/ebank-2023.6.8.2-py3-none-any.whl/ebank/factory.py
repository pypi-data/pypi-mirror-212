from encoo.logger import Logger

from ebank.utils.filesearch import FileSearch
from ebank.utils import sfun as util
from ebank import constants as CONSTANTS


class Factory:

    """（根目录）\(银行名称)\(日期)\[H|T]_网银账号_yyyyMMdd-yyyyMMdd[.xls|.pdf|.xlsx]
    """

    def __init__(self, trans_file):
        self.__logger = Logger("ebank factory")

        self.__trans_file = trans_file
        self.bank_name = util.get_bankname(trans_file, CONSTANTS.BANK_NAME_IDX)

    def to_sqlite(self):
        '''判断该银行存在处理类'''
        if self.bank_name in CONSTANTS.BANK_TRANS_CLS.keys():
            trans_cls = CONSTANTS.BANK_TRANS_CLS.get(bank_name)
            cur_cls = globals()[trans_cls]

            # 调用具体处理类
            cur_cls(file_path=fp).to_sqlite()
        else:
            self.__logger.error(f"to_sqlite no cls for {bank_name}")

    def query_sqlite(self):
        pass


if __name__ =="__main__" :    
    Factory(r"D:\Repos\华夏银行\20230606\H_12592000000000515_20230201-20230228_流水.xls").to_sqlite()

    