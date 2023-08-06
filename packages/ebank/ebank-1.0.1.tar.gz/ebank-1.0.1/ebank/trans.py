import sqlite3
from abc import ABC, abstractmethod
from encoo.logger import Logger
from utils import sfun


class BaseTrans(ABC):

    BANK_NAME_IDX = -3
    BANK_NO_IDX = -1
    SQLITE3_PATH = r"D:\Repos\ebanktool\ebank\ebank.db"

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

        self.excel_sheet = sfun.read_xl(self.file_path)
        # 从文件路径中加载信息
        self.__from_filepath()

    def __from_filepath(self):
        """ 从路径中获取信息
        D:\\Ouye\\12家银行流水回单\\渤海银行\\2022-11-07\\H_2017037908000158_2022-11-01~2022-11-04.xls
        """
        try:
            fps = self.file_path.split("\\")
            self.bank_name = fps[self.BANK_NAME_IDX]
            self.bank_no = sfun.get_curno(fps[self.BANK_NO_IDX])

        except Exception as ex:
            self._logger.error(f"BaseTrans __from_filepath {ex}")

    @abstractmethod
    def build_trans(self, row_idx) -> list[str]:
        pass

    def extract(self) -> list[tuple]:
        row_list = []
        self._logger.info(f"BaseTrans extract idx {self.row_start_idx}")
        try:
            for row_idx in range(self.row_start_idx, self.excel_sheet.nrows):
                # 依次按列取值
                trans_row = self.build_trans(row_idx)
                row_list.append(tuple(trans_row))
            # end for
        except Exception as ex:
            self._logger.error(f"BaseTrans extract  {ex}")
        # end try
        return row_list

    def to_sqlite(self) -> None:
        rows = self.extract()
        self._logger.info(f"BaseTrans to_sqlite {rows}")
        try:
            conn = sqlite3.connect(self.SQLITE3_PATH)
            cur = conn.cursor()
            sql = ' insert into trans(file_path,bank_name,acc_name,acc_no,trans_date,flow_no,rec_amt,pay_amt,' + \
                ' balance,other_acc_name,other_acc_no,other_bank_name,purpose,abstract,remark,rct_path) ' + \
                ' values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'

            cur.executemany(sql, rows)
            conn.commit()

            cur.close()
            conn.close()
        except Exception as ex:
            self._logger.error(f"BaseTrans to_sqlite {ex}")


class BeiJingTrans(BaseTrans):

    # 流水文件开始取数索引
    ROW_START_IDX = 3

    def __init__(self, file_path, row_start_idx=ROW_START_IDX):
        super().__init__(file_path, row_start_idx)

    def build_trans(self, row_idx) -> list[str]:

        sheet = self.excel_sheet
        # 依次按列取值
        row_trans_date = sheet.cell(row_idx, 4).value
        row_flow_no = sheet.cell(row_idx, 2).value
        row_rec_amt = sheet.cell(row_idx, 8).value
        row_pay_amt = sheet.cell(row_idx, 7).value
        row_balance = sheet.cell(row_idx, 9).value
        row_ant_name = sheet.cell(row_idx, 10).value
        row_ant_no = sheet.cell(row_idx, 11).value
        row_purpose = sheet.cell(row_idx, 6).value
        row_abstract = sheet.cell(row_idx, 13).value

        return [self.file_path,
                self.bank_name,
                self.acc_name,
                self.acc_no,
                row_trans_date,
                row_flow_no,
                row_rec_amt,
                row_pay_amt,
                row_balance,
                row_ant_name,
                row_ant_no,
                self.other_bank_name,
                row_purpose,
                row_abstract,
                self.remark,
                self.rct_path]


if (__name__ == "__main__"):
    bfr = BeiJingTrans(
        r"D:\Ouye\12家银行流水回单\北京银行\东方付通信息技术有限公司\2022-11-07\H20000021408900101114394 2022-03-01~2022-03-10.xls").to_sqlite()
