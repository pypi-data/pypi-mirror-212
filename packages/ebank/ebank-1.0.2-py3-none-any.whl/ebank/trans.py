import sqlite3
from abc import ABC, abstractmethod
from datetime import datetime

import constants as CONSTANTS
from encoo.logger import Logger
from utils import sfun


class BaseTrans(ABC):

    _logger = Logger("BaseTrans")

    def __init__(self, file_path, row_start_idx):

        # 流水文件路径
        self.file_path = file_path
        # 开始取数行索引
        self.row_start_idx = row_start_idx

        # 银行名称
        self.bank_name = ""

        # 本方户名
        self.acc_name = ""
        # 本方账号
        self.acc_no = ""

        # 交易日期
        self.trans_date = ""
        # 流水号
        self.flow_no = ""
        # 收入金额
        self.rec_amt = 0.00
        # 支出金额
        self.pay_amt = 0.00
        # 余额
        self.balance = 0.00

        # 对方户名
        self.other_acc_name = ""
        # 对方账号
        self.other_acc_no = ""
        # 对方行名
        self.other_bank_name = ""

        # 用途
        self.purpose = ""
        # 摘要
        self.abstract = ""
        # 备注
        self.remark = ""

        # 回单路径
        self.rct_path = ""
        self.task_id = ""

        self.excel_sheet = sfun.read_xl(self.file_path)
        # 从文件路径中加载信息
        self.__from_filepath()

    def __from_filepath(self):
        """ 从路径中获取信息
        D:\Repos\工商银行\20230604\H_4301016509827101946_20230601-20230604_流水.xlsx
        """
        try:
            fps = self.file_path.split("\\")
            self.bank_name = fps[CONSTANTS.BANK_NAME_IDX]
            self.acc_no = sfun.get_curno(fps[CONSTANTS.BANK_NO_IDX])
            self.acc_name = CONSTANTS.BANK_NO_DICT[self.acc_no]

        except Exception as ex:
            self._logger.error(f"BaseTrans __from_filepath {ex}")

    @abstractmethod
    def build_trans(self, row_idx):
        pass

    def extract(self) -> list[tuple]:
        row_list = []

        try:
            self.task_id = datetime.now().strftime("%Y%m%d%H%M%S")
            for row_idx in range(self.row_start_idx, self.excel_sheet.nrows):
                # 调用子类实现的方法
                self.build_trans(row_idx)

                trans_row = (self.file_path,
                             self.bank_name,
                             self.acc_name,
                             self.acc_no,
                             self.trans_date,
                             self.flow_no,
                             self.rec_amt,
                             self.pay_amt,
                             self.balance,
                             self.other_acc_name,
                             self.other_acc_no,
                             self.other_bank_name,
                             self.purpose,
                             self.abstract,
                             self.remark,
                             self.rct_path,
                             self.task_id,
                             datetime.now(),
                             datetime.now(),
                             1
                             )

                row_list.append(trans_row)
            # end for
        except Exception as ex:
            self._logger.error(f"BaseTrans extract  {ex}")
        # end try
        return row_list

    def to_sqlite(self) -> None:
        rows = self.extract()
        self._logger.info(f"BaseTrans to_sqlite {rows}")
        try:
            conn = sqlite3.connect(CONSTANTS.SQLITE3_PATH)
            cur = conn.cursor()
            sql = CONSTANTS.SQL_INSERT_TRANS
            cur.executemany(sql, rows)
            conn.commit()

            cur.close()
            conn.close()
        except Exception as ex:
            self._logger.error(f"BaseTrans to_sqlite {ex}")


class ICBCTrans(BaseTrans):

    '''工商银行
    日期	交易类型	凭证种类	凭证号	对方户名	对方账号	摘要	借方发生额	贷方发生额	余额
    2023-06-01	转账	0	00000000000000000	CHFMCNSH	"1001190709278132949" 	23060135315	0.00 	686,502,400.00 	687,103,056.00
    2023-06-01	转账	0	00000000000000000		"0101000111*********" 	LMS2023053146349	686,502,400.00 	0.00 	600,656.00 '''

    # 流水文件开始取数索引
    ROW_START_IDX = 5

    def __init__(self, file_path, row_start_idx=ROW_START_IDX):
        super().__init__(file_path, row_start_idx)

    def build_trans(self, row_idx):
        sheet = self.excel_sheet
        # 依次按列取值
        self.trans_date = sheet.cell(row_idx, 0).value
        self.flow_no = sheet.cell(row_idx, 3).value
        self.rec_amt = sheet.cell(row_idx, 8).value
        self.pay_amt = sheet.cell(row_idx, 7).value
        self.balance = sheet.cell(row_idx, 9).value
        self.other_acc_name = sheet.cell(row_idx, 4).value
        self.other_acc_no = sheet.cell(row_idx, 5).value
        self.purpose = ""
        self.abstract = sheet.cell(row_idx, 6).value
        return self


class HXBTrans(BaseTrans):

    ''''华夏银行
        序号	交易日期	交易时间	支出金额	收入金额	余额	对方账号	对方户名	对方行名	核心流水号	交易描述	摘要	凭证号码
        1	2023-02-13	11:28:34	7.00		469.45	60220903	网上银行结算手续费收入		475384	网银结算手续费		
        2	2023-02-13	11:28:34	63,056.41		476.45	99060171480000008	同业系统往来-无锡分行	江苏银行股份有限公司	475384	网上银行跨行付款	理财利息'''

    # 流水文件开始取数索引
    ROW_START_IDX = 7

    def __init__(self, file_path, row_start_idx=ROW_START_IDX):
        super().__init__(file_path, row_start_idx)

    def build_trans(self, row_idx):
        sheet = self.excel_sheet
        # 依次按列取值
        self.trans_date = sheet.cell(row_idx, 1).value
        self.flow_no = sheet.cell(row_idx, 9).value
        self.rec_amt = sheet.cell(row_idx, 4).value
        self.pay_amt = sheet.cell(row_idx, 3).value
        self.balance = sheet.cell(row_idx, 5).value
        self.other_acc_name = sheet.cell(row_idx, 7).value
        self.other_acc_no = sheet.cell(row_idx, 6).value
        self.other_bank_name = sheet.cell(row_idx, 8).value
        self.purpose = ""
        self.abstract = sheet.cell(row_idx, 11).value
        return self


if (__name__ == "__main__"):
    bfr = HXBTrans(
        r"D:\Repos\华夏银行\20230606\H_12592000000000515_20230201-20230228_流水.xls").to_sqlite()
