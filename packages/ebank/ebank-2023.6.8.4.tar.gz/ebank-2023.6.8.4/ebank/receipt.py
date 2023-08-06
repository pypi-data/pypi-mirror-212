import re
from encoo.logger import Logger
import pdfplumber
from utils import baiduocr, misc as util
from utils.filesearch import FileSearch


class ReceiptFactory:
    """网银回单解析
    昆仑银行，汉口银行，浦发银行，进出口银行，民生银行，上海银行，交通银行，华夏银行，安徽农金，北京银行，浙商银行
    Returns:
        回单数据保存成xls文件
    """
    RECEIPT_CLS = {
        "昆仑银行": "KunLunRct", "汉口银行": "HanKouRct", "浦发银行": "PuFaRct",
        "进出口银行": "JinChuKouRct", "民生银行": "MinShengRct", "上海银行": "ShangHaiRct",
        "交通银行": "JiaoTongRct", "华夏银行": "HuaXiaRct", "安徽农金": "AnHuiNongJinRct",
        "北京银行": "BeiJingRct", "浙商银行": "ZheShangRct"}

    ROOT_DIR = r"C:\nas-个人文件夹\RPA用（误删）\RPA银行下载文件"
    __logger = Logger("ReceiptFactory")

    def __init__(self, run_date, root_dir=ROOT_DIR) -> None:

        self.__file_list = FileSearch(
            run_date, root_dir).search_rct_files()

    def extract_to_xls(self, xlsPath: str):
        try:
            row_list = self.get_rct_data()
            util.wt_rct_excel(xlsPath, row_list)
        except Exception as e:
            self.__logger.error(f"ReceiptFactory extract_to_xls-{e}")

        return xlsPath

    def get_rct_data(self):

        row_list = []
        for f in self.__file_list:
            rcts = self.__extract_pdf(f)

            for rct in rcts:
                row_list.append(rct)

        return row_list

    def __extract_pdf(self, pdf_path):
        rcts = []
        bank_name = pdf_path.split("\\")[-4]

        rct_cls = self.RECEIPT_CLS.get(bank_name)
        if rct_cls is not None:
            cur_cls = globals()[rct_cls]
            rcts = cur_cls(file_path=pdf_path).extract()
        else:
            self.__logger.info(f"__extract_pdf not find cls for {bank_name}")

        return rcts


class Receipt:

    _logger = Logger("Receipt")

    def __init__(self, file_path=None, *args):
        self.file_path = file_path
        self.pay_no = ""
        self.pay_name = ""
        self.rec_no = ""
        self.rec_name = ""

        self.amt = 0
        self.pay_amt = 0
        self.rec_amt = 0

        self.trans_date = ""

        self.cur_no = ""
        self.cur_name = ""
        self.ant_no = ""
        self.ant_name = ""

        self.company_name = ""
        self.bank_name = ""

        self.rct_no = ""
        self.flow_no = ""

        self.pdf_tables = []
        self.is_multi_pages = False
        self.sub_pdfs = []

        self.__load()
        self.__init_data(args)

    def __load(self):

        if self.file_path is not None:
            pdf = pdfplumber.open(self.file_path)
            if len(pdf.pages) > 1:
                self.is_multi_pages = True
                self.sub_pdfs = util.split_pdf(self.file_path)
            else:
                self.pdf_tables = pdf.pages[0].extract_tables()
                self.pdf_text = pdf.pages[0].extract_text()

    def __init_data(self, *args):
        if len(args[0]) == 3:
            self.company_name = args[0][0]
            self.bank_name = args[0][1]
            self.cur_no = args[0][2]
        elif self.file_path is not None:
            file_paths = self.file_path.split("\\")
            self.company_name = file_paths[-3]
            self.bank_name = file_paths[-4]
            self.cur_no = util.get_curno(file_paths[-1])
        else:
            pass  # 不初始化值

    def fmt(self):
        if self.pay_name is not None:
            self.pay_name = self.pay_name.replace("\n", "")
        if self.rec_name is not None:
            self.rec_name = self.rec_name.replace("\n", "")
        # cal pay / rec amt
        if (self.pay_no == self.cur_no):
            self.pay_amt = self.amt
            self.cur_name = self.pay_name

            self.ant_no = self.rec_no
            self.ant_name = self.rec_name

        if (self.rec_no == self.cur_no):
            self.rec_amt = self.amt
            self.cur_name = self.rec_name

            self.ant_no = self.pay_no
            self.ant_name = self.pay_name
        return self

    def extract(self) -> list["Receipt"]:
        pass


class KunLunRct(Receipt):

    def __init__(self, file_path=""):
        super().__init__(file_path)

    def extract(self) -> list[Receipt]:
        self._logger.debug(f"KunLunRct  {self.pdf_tables}")

        rct_list = []
        try:
            for table in self.pdf_tables:
                rct = Receipt()
                rct.file_path = self.file_path
                rct.company_name = self.company_name
                rct.bank_name = self.bank_name
                rct.cur_no = self.cur_no

                rct.pay_name = table[0][2]
                rct.rec_name = table[0][-1]

                rct.pay_no = table[1][2]
                rct.rec_no = table[1][-1]

                rct.amt = util.fmt_amt(table[5][1])
                rct.trans_date = table[9][-1]
                rct.flow_no = table[9][-4]

                rct.fmt()
                rct_list.append(rct)
        except Exception as ex:
            self._logger.debug(f"KunLunRct  {ex}")

        return rct_list


class HanKouRct(Receipt):

    def __init__(self, file_path=""):
        super().__init__(file_path)

    def extract(self) -> list[Receipt]:
        self._logger.debug(f"HanKouRct  {self.pdf_tables}")

        rct_list = []
        try:
            for table in self.pdf_tables:
                rct = Receipt()
                rct.file_path = self.file_path
                rct.company_name = self.company_name
                rct.bank_name = self.bank_name
                rct.cur_no = self.cur_no

                # rct.rct_no = ""
                rct.pay_name = table[1][2]
                rct.rec_name = table[1][-3]

                rct.pay_no = table[2][2]
                rct.rec_no = table[2][-3]

                rct.amt = util.fmt_amt(table[4][-3])
                rct.trans_date = util.fmt_trans_date(table[0][-3])
                rct.flow_no = table[0][2]

                rct.fmt()
                rct_list.append(rct)
        except Exception as ex:
            self._logger.debug(f"HanKouRct  {ex}")

        return rct_list


class PuFaRct(Receipt):

    def __init__(self, file_path=""):
        super().__init__(file_path)

    def extract(self) -> list[Receipt]:
        self._logger.debug(f"PuFaRct  {self.pdf_tables}")

        rct_list = []
        try:
            for table in self.pdf_tables:
                rct = Receipt()
                rct.file_path = self.file_path
                rct.company_name = self.company_name
                rct.bank_name = self.bank_name
                rct.cur_no = self.cur_no

                rct.rct_no = table[0][2]
                rct.pay_name = table[1][2]
                rct.rec_name = table[1][-2]

                rct.pay_no = table[2][2]
                rct.rec_no = table[2][-2]

                rct.amt = util.fmt_amt(table[6][-4])
                rct.trans_date = util.fmt_trans_date(table[5][2])
                rct.flow_no = table[5][-1]

                rct.fmt()
                rct_list.append(rct)
        except Exception as ex:
            self._logger.debug(f"PuFaRct {ex}")

        return rct_list


class JinChuKouRct(Receipt):
    '''使用baidu OCR '''

    KEY_RCT_NO = ""
    KEY_PAY_NAME = ""
    KEY_PAY_NO = ""
    KEY_REC_NAME = "8-1-9-2"
    KEY_REC_NO = "8-2-9-3"

    KEY_AMT = "7-4-9-5"
    KEY_DATE = "0-0-5-1"
    KEY_FLOW_NO = "5-0-9-1"

    def __init__(self, file_path=None, *args):
        super().__init__(file_path, *args)

    rct_list = []

    def extract(self) -> list[Receipt]:
        if self.is_multi_pages == True:
            for pdf_path in self.sub_pdfs:
                rcts = JinChuKouRct(pdf_path, self.company_name,
                                    self.bank_name, self.cur_no).extract()
                for rct in rcts:
                    self.rct_list.append(rct)
        else:
            return self.__extract(self.pdf_text)
        return self.rct_list

    def __extract(self, pdf_text):
        self._logger.debug(f"JinChuKouRct pdf_text{pdf_text}")

        rcts = []
        try:
            pdf_kvs = []
            if (len(self.pdf_tables) > 0):
                pdf_kvs = baiduocr().ocr_table(self.file_path)
            else:
                self._logger.error(f"JinChuKouRct not table {self.file_path}")
            self._logger.debug(
                f"JinChuKouRct {self.file_path} pdf_kv{pdf_kvs}")

            for kv in pdf_kvs:
                rct = Receipt()
                rct.file_path = self.file_path
                rct.company_name = self.company_name
                rct.bank_name = self.bank_name
                rct.cur_no = self.cur_no

                rct.pay_name = kv.get(self.KEY_PAY_NAME, "")
                rct.pay_no = kv.get(self.KEY_PAY_NO, "")
                rct.rec_name = kv.get(self.KEY_REC_NAME, "")
                rct.rec_no = kv.get(self.KEY_REC_NO, "")

                rct.amt = util.fmt_amt(kv.get(self.KEY_AMT, ""))

                date_str = s = re.findall(
                    r"\d*", kv.get(self.KEY_DATE, ""))[0]
                rct.trans_date = util.fmt_trans_date(date_str)

                rct.flow_no = kv.get(self.KEY_FLOW_NO, "")

                rct.fmt()
                rcts.append(rct)
        except Exception as ex:
            self._logger.error(f"JinChuKouRct __extract {ex}")

        return rcts


class MinShengRct(Receipt):

    def __init__(self, file_path=""):
        super().__init__(file_path)

    def extract(self) -> list[Receipt]:
        self._logger.debug(f"MinShengRct  {self.pdf_tables}")

        rct_list = []
        try:
            for table in self.pdf_tables:
                rct = Receipt()
                rct.file_path = self.file_path
                rct.company_name = self.company_name
                rct.bank_name = self.bank_name
                rct.cur_no = self.cur_no

                # rct.rct_no = ""
                rct.pay_name = table[2][2]
                rct.rec_name = table[2][-1]

                rct.pay_no = table[3][2]
                rct.rec_no = table[3][-1]

                rct.amt = util.fmt_amt(table[5][1])
                rct.trans_date = util.fmt_trans_date(table[6][-2])
                rct.flow_no = table[7][1]

                rct.fmt()
                rct_list.append(rct)
        except Exception as ex:
            self._logger.debug(f"MinShengRct  {ex}")

        return rct_list


class ZheShangRct(Receipt):

    def __init__(self, file_path=None, *args):
        super().__init__(file_path, *args)

    rct_list = []

    def extract(self) -> list[Receipt]:
        if self.is_multi_pages == True:
            for pdf_path in self.sub_pdfs:
                rcts = ZheShangRct(pdf_path, self.company_name,
                                   self.bank_name, self.cur_no).extract()
                for rct in rcts:
                    self.rct_list.append(rct)
        else:
            return self.__extract()
        return self.rct_list

    def __extract(self):
        self._logger.debug(f"ZheShangRct  {self.pdf_tables}")

        rct_list = []
        try:
            for table in self.pdf_tables:
                rct = Receipt()
                rct.file_path = self.file_path
                rct.company_name = self.company_name
                rct.bank_name = self.bank_name
                rct.cur_no = self.cur_no

                # rct.rct_no = ""
                rct.pay_name = str(table[0][1]).removeprefix("户名:")
                rct.rec_name = str(table[0][-1]).removeprefix("户名:")

                rct.pay_no = str(table[1][1]).removeprefix("账号:")
                rct.rec_no = str(table[1][-1]).removeprefix("账号:")

                rct.amt = util.fmt_amt(table[3][2])

                trans = table[4][0]
                flow_nos = re.findall(r"(?<=交易流水号：)\d*", trans)
                if (len(flow_nos) > 0):
                    rct.flow_no = flow_nos[0]

                trans_dates = re.findall(r"(?<=交易时间：)\d{4}-\d{2}-\d{2}", trans)
                if (len(trans_dates) > 0):
                    rct.trans_date = trans_dates[0]

                rct.fmt()
                rct_list.append(rct)
        except Exception as ex:
            self._logger.debug(f"ZheShangRct  {ex}")

        return rct_list


class BeiJingRct(Receipt):

    def __init__(self, file_path=None, *args):
        super().__init__(file_path, *args)

    rct_list = []

    def extract(self) -> list[Receipt]:
        if self.is_multi_pages == True:
            for pdf_path in self.sub_pdfs:
                rcts = BeiJingRct(pdf_path, self.company_name,
                                  self.bank_name, self.cur_no).extract()
                for rct in rcts:
                    self.rct_list.append(rct)
        else:
            return self.__extract()
        return self.rct_list

    def __extract(self):
        self._logger.debug(f"BeiJingRct  {self.pdf_tables}")

        rct_list = []
        try:
            for table in self.pdf_tables:
                rct = Receipt()
                rct.file_path = self.file_path
                rct.company_name = self.company_name
                rct.bank_name = self.bank_name
                rct.cur_no = self.cur_no

                # rct.rct_no = ""
                rct.pay_name = table[0][1]
                rct.rec_name = table[0][-1]

                rct.pay_no = table[1][1]
                rct.rec_no = table[1][-1]

                rct.amt = util.fmt_amt(table[4][1])
                rct.trans_date = util.fmt_trans_date(table[3][-1])

                rct.flow_no = str(table[7][-1])[0:19]

                rct.fmt()
                rct_list.append(rct)
        except Exception as ex:
            self._logger.debug(f"BeiJingRct  {ex}")

        return rct_list


class ShangHaiRct(Receipt):

    RE_SPLIT_GROUP = r"(?=记账日期)[\S\s]*?(?=打印时间)"
    RE_RCT_NO = r"(?<=回单编号:)[A-Z|\d]*"
    RE_PAY_NAME = r"(?<=付款人名称:)\S*"
    RE_PAY_NO = r"(?<=付款人账号:)\S*"
    RE_AMT = r"(?<=金额\(小写\):)\S*"
    RE_DATE = r"(?<=记账日期:)[\d*年\d*月\d*日]*"

    def __init__(self, file_path=None, *args):
        super().__init__(file_path, *args)

    rct_list = []

    def extract(self) -> list[Receipt]:
        if self.is_multi_pages == True:
            for pdf_path in self.sub_pdfs:
                rcts = ShangHaiRct(pdf_path, self.company_name,
                                   self.bank_name, self.cur_no).extract()
                for rct in rcts:
                    self.rct_list.append(rct)
        else:
            return self.__extract(self.pdf_text)
        return self.rct_list

    def __extract(self, pdf_text):
        self._logger.debug(f"ShangHaiRct __extract{pdf_text}")
        rcts = []
        try:
            matches = re.finditer(
                self.RE_SPLIT_GROUP, pdf_text, re.MULTILINE)
            for match in matches:
                group_text = match.group().replace(" ", "")
                # print(f"group_text-{group_text}")
                rct = Receipt()
                rct.file_path = self.file_path
                rct.company_name = self.company_name
                rct.bank_name = self.bank_name
                rct.cur_no = self.cur_no

                iter_rct_no = re.finditer(self.RE_RCT_NO, group_text)
                rct.rct_no = next(iter_rct_no).group()

                iter_pay_name = re.finditer(self.RE_PAY_NAME, group_text)
                pay_name_group = next(
                    iter_pay_name).group().split("收款人名称:")
                rct.pay_name = pay_name_group[0]
                rct.rec_name = pay_name_group[1]

                iter_pay_no = re.finditer(self.RE_PAY_NO, group_text)
                pay_no_group = next(iter_pay_no).group().split("收款人账号:")
                rct.pay_no = pay_no_group[0]
                rct.rec_no = pay_no_group[1]

                iter_amt = re.finditer(self.RE_AMT, group_text)
                rct.amt = util.fmt_amt(next(iter_amt).group())

                iter_date = re.finditer(self.RE_DATE, group_text)
                rct.trans_date = util.fmt_trans_date(next(iter_date).group())
                # rct.flow_no=""

                rct.fmt()
                rcts.append(rct)
        except Exception as ex:
            self._logger.error(f"ShangHaiRct __extract {ex}")

        return rcts


class JiaoTongRct(Receipt):

    RE_SPLIT_GROUP = r"(?=回单编号)[\S\s]*?(?=批次号)"
    RE_RCT_NO = r"(?<=回单编号：)[A-Z|\d]*"
    RE_PAY_NAME = r"付款人名称：(.*?)开户行名称"
    RE_RCE_NAME = r"收款人名称：(.*?)开户行名称"

    RE_PAY_NO = r"(?<=付款人账号：)\d*"
    RE_RCE_NO = r"(?<=收款人账号：)\d*"

    RE_AMT = r"(?<=CNY金额：)[.|,|\d]*"
    RE_DATE = r"(?<=记账日期：)\d*"
    RE_FLOW_NO = r"(?<=会计流水号：)[A-Z|\d]*"

    def __init__(self, file_path=None, *args):
        super().__init__(file_path, *args)

    rct_list = []

    def extract(self) -> list[Receipt]:
        if self.is_multi_pages == True:
            for pdf_path in self.sub_pdfs:
                rcts = JiaoTongRct(pdf_path, self.company_name,
                                   self.bank_name, self.cur_no).extract()
                for rct in rcts:
                    self.rct_list.append(rct)
        else:
            return self.__extract(self.pdf_text)
        return self.rct_list

    def __extract(self, pdf_text):
        self._logger.debug(f"JiaoTongRct __extract{pdf_text}")
        rcts = []
        try:
            matches = re.finditer(
                self.RE_SPLIT_GROUP, pdf_text, re.MULTILINE)
            for match in matches:
                group_text = match.group().replace(" ", "").replace("\n", "")
                print(f"group_text-{group_text}")
                rct = Receipt()
                rct.file_path = self.file_path
                rct.company_name = self.company_name
                rct.bank_name = self.bank_name
                rct.cur_no = self.cur_no

                iter_rct_no = re.finditer(self.RE_RCT_NO, group_text)
                rct.rct_no = next(iter_rct_no).group()

                rct.pay_name = re.findall(self.RE_PAY_NAME, group_text)[0]
                rct.rec_name = re.findall(self.RE_RCE_NAME, group_text)[0]

                rct.pay_no = re.findall(self.RE_PAY_NO, group_text)[0]
                rct.rec_no = re.findall(self.RE_RCE_NO, group_text)[0]

                iter_amt = re.finditer(self.RE_AMT, group_text)
                rct.amt = util.fmt_amt(next(iter_amt).group())

                iter_date = re.finditer(self.RE_DATE, group_text)
                rct.trans_date = util.fmt_trans_date(next(iter_date).group())

                iter_flow_no = re.finditer(self.RE_FLOW_NO, group_text)
                rct.flow_no = util.fmt_trans_date(next(iter_flow_no).group())

                rct.fmt()
                rcts.append(rct)
        except Exception as ex:
            self._logger.error(f"JiaoTongRct __extract {ex}")

        return rcts


class HuaXiaRct(Receipt):

    # RE_SPLIT_GROUP = r"(?=回单编号)[\S\s]*?(?=批次号)"
    RE_RCT_NO = r"(?<=回单编码:)[A-Z|\d]*"
    RE_PAY_NAME = r"转出户名:(.*?)转入户名"
    RE_RCE_NAME = r"(?<=转入户名:)\S*"

    RE_PAY_NO = r"(?<=转出账号:)\d*"
    RE_RCE_NO = r"(?<=转入账号:)\d*"

    RE_AMT = r"(?<=金额:)[.|,|\d]*"
    RE_DATE = r"(?<=交易日期)\S*"
    RE_FLOW_NO = r"(?<=流水号:)[A-Z|\d]*"

    def __init__(self, file_path=None, *args):
        super().__init__(file_path, *args)

    rct_list = []

    def extract(self) -> list[Receipt]:
        if self.is_multi_pages == True:
            for pdf_path in self.sub_pdfs:
                rcts = HuaXiaRct(pdf_path, self.company_name,
                                 self.bank_name, self.cur_no).extract()
                for rct in rcts:
                    self.rct_list.append(rct)
        else:
            return self.__extract(self.pdf_text)
        return self.rct_list

    def __extract(self, pdf_text):

        pdf_text = pdf_text.replace(" ", "")
        self._logger.debug(f"HuaXiaRct __extract{pdf_text}")
        rcts = []
        try:
            if (pdf_text != ""):
                rct = Receipt()
                rct.file_path = self.file_path
                rct.company_name = self.company_name
                rct.bank_name = self.bank_name
                rct.cur_no = self.cur_no

                iter_rct_no = re.finditer(self.RE_RCT_NO, pdf_text)
                rct.rct_no = next(iter_rct_no).group()

                if ("转账业务" in pdf_text):
                    rct.pay_name = re.findall(self.RE_PAY_NAME, pdf_text)[0]
                    rct.rec_name = re.findall(self.RE_RCE_NAME, pdf_text)[0]

                    rct.pay_no = re.findall(self.RE_PAY_NO, pdf_text)[0]
                    rct.rec_no = re.findall(self.RE_RCE_NO, pdf_text)[0]

                    iter_amt = re.finditer(self.RE_AMT, pdf_text)
                    rct.amt = util.fmt_amt(next(iter_amt).group())

                    iter_date = re.finditer(self.RE_DATE, pdf_text)
                    rct.trans_date = util.fmt_trans_date(
                        next(iter_date).group())
                # end if
                iter_flow_no = re.finditer(self.RE_FLOW_NO, pdf_text)
                rct.flow_no = next(iter_flow_no).group()

                rct.fmt()
                rcts.append(rct)
        except Exception as ex:
            self._logger.error(f"HuaXiaRct __extract {ex}")

        return rcts


class AnHuiNongJinRct(Receipt):
    '''使用baidu OCR '''

    KEY_RCT_NO = ""
    KEY_PAY_NAME = "2-0-3-1"
    KEY_PAY_NO = "2-1-3-2"
    KEY_REC_NAME = "5-0-6-1"
    KEY_REC_NO = "5-1-6-2"

    KEY_AMT = "5-3-6-4"
    KEY_DATE = "5-5-6-6"
    KEY_FLOW_NO = "5-6-6-7"

    def __init__(self, file_path=None, *args):
        super().__init__(file_path, *args)

    rct_list = []

    def extract(self) -> list[Receipt]:
        if self.is_multi_pages == True:
            for pdf_path in self.sub_pdfs:
                rcts = AnHuiNongJinRct(pdf_path, self.company_name,
                                       self.bank_name, self.cur_no).extract()
                for rct in rcts:
                    self.rct_list.append(rct)
        else:
            return self.__extract(self.pdf_text)
        return self.rct_list

    def __extract(self, pdf_text):
        rcts = []
        try:
            pdf_kvs = baiduocr().ocr_table(self.file_path)
            self._logger.debug(
                f"AnHuiNongJinRct {self.file_path} pdf_kv{pdf_kvs}")

            for kv in pdf_kvs:
                rct = Receipt()
                rct.file_path = self.file_path
                rct.company_name = self.company_name
                rct.bank_name = self.bank_name
                rct.cur_no = self.cur_no

                rct.pay_name = kv.get(self.KEY_PAY_NAME, "")
                rct.pay_no = kv.get(self.KEY_PAY_NO, "")
                rct.rec_name = kv.get(self.KEY_REC_NAME, "")
                rct.rec_no = kv.get(self.KEY_REC_NO, "")

                rct.amt = util.fmt_amt(kv.get(self.KEY_AMT, ""))

                rct.trans_date = util.fmt_trans_date(
                    kv.get(self.KEY_DATE, ""))
                rct.flow_no = kv.get(self.KEY_FLOW_NO, "")

                rct.fmt()
                rcts.append(rct)
        except Exception as ex:
            self._logger.error(f"AnHuiNongJinRct __extract {ex}")

        return rcts


if __name__ == "__main__":
    pass
