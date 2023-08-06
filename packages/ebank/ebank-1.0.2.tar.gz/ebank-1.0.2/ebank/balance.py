import sqlite3
from abc import ABC, abstractmethod
from datetime import datetime

import constants as CONSTANTS
from encoo.logger import Logger
from utils import sfun


class BaseBalance(ABC):

    _logger = Logger("BaseBalance")

    def __init__(self, file_path, row_start_idx):

        # 文件路径
        self.file_path = file_path
        # 开始取数行索引
        self.row_start_idx = row_start_idx

        # 银行名称
        self.bank_name = ""
        # 本方户名
        self.acc_name = ""
        # 账号
        self.acc_no = ""

        # 查询时间
        self.query_date = ""
        # 可用余额
        self.balance = ""

        # 币种
        self.currency = ""
        self.task_id = ""

        self.excel_sheet = sfun.read_xl(self.file_path)
        # 从文件路径中加载信息
        self.__from_filepath()

    def __from_filepath(self):
        """ 从路径中获取信息
        "D:\Repos\工商银行\20230604\工行江苏省分行1_20230605_余额.xlsx"
        """
        try:
            fps = self.file_path.split("\\")
            self.bank_name = fps[CONSTANTS.BANK_NAME_IDX]

        except Exception as ex:
            self._logger.error(f"BaseBalance __from_filepath {ex}")

    @abstractmethod
    def build_self(self, row_idx):
        pass

    def extract(self) -> list[tuple]:
        row_list = []

        try:
            self.task_id = datetime.now().strftime("%Y%m%d%H%M%S")
            for row_idx in range(self.row_start_idx, self.excel_sheet.nrows):
                # 调用子类实现的方法
                self.build_self(row_idx)

                trans_row = (self.file_path,
                             self.bank_name,
                             self.acc_name,
                             self.acc_no,
                             self.balance,
                             self.query_date,
                             self.currency,
                             self.task_id,
                             datetime.now(),
                             datetime.now(),
                             1)

                row_list.append(trans_row)
            # end for
        except Exception as ex:
            self._logger.error(f"BaseTrans extract  {ex}")
        # end try
        return row_list

    def to_sqlite(self) -> None:
        rows = self.extract()
        self._logger.info(f"BaseBalance to_sqlite {rows}")
        try:
            conn = sqlite3.connect(CONSTANTS.SQLITE3_PATH)
            cur = conn.cursor()
            sql = CONSTANTS.SQL_INSERT_BALANCE
            cur.executemany(sql, rows)
            conn.commit()

            cur.close()
            conn.close()
        except Exception as ex:
            self._logger.error(f"BaseBalance to_sqlite {ex}")


class ICBCBalance(BaseBalance):

    ''' 工商银行
        账　号	币种	钞汇标志	账户属性	昨日余额	当前余额	可用余额	查询时间	操作
        4301016509812100729	英镑	汇	基本账户	600,000.00	600,000.00	600,000.00	15:50:08	
        4301016509813100767	港币	汇	基本账户	20,004,076.60	20,004,076.60	20,004,076.60	15:50:08'''

    # 文件开始取数索引
    ROW_START_IDX = 2

    def __init__(self, file_path, row_start_idx=ROW_START_IDX):
        super().__init__(file_path, row_start_idx)

    def build_self(self, row_idx):
        sheet = self.excel_sheet
        # 依次按列取值
        self.acc_no = sheet.cell(row_idx, 0).value
        self.acc_name = CONSTANTS.BANK_NO_DICT[self.acc_no]
        self.balance = sheet.cell(row_idx, 6).value
        self.query_date = sheet.cell(row_idx, 7).value
        self.currency = sheet.cell(row_idx, 1).value
        return self


class HXBBalance(BaseBalance):

    ''' 工商银行
        序号	账户别名	账号	账户名称	币种	可用余额
        1	未定义	12592000000000515	江苏银行股份有限公司无锡分行	人民币	10,211.33'''

    # 文件开始取数索引
    ROW_START_IDX = 1

    def __init__(self, file_path, row_start_idx=ROW_START_IDX):
        super().__init__(file_path, row_start_idx)

    def build_self(self, row_idx):
        sheet = self.excel_sheet
        # 依次按列取值
        self.acc_no = sheet.cell(row_idx, 2).value
        self.acc_name = CONSTANTS.BANK_NO_DICT[self.acc_no]
        self.balance = sheet.cell(row_idx, 5).value
        self.query_date = ""
        self.currency = sheet.cell(row_idx, 4).value
        return self


if (__name__ == "__main__"):
    bfr = HXBBalance(
        r"D:\Repos\华夏银行\20230606\华夏银行无锡分行_20230606_余额.xlsx").to_sqlite()
