
BANK_NAME_IDX = 2
BANK_NO_IDX = -1
SQLITE3_PATH = r"dbs\ebank.db"


BANK_NO_DICT = {
    "4301016509812100729": "江苏银行股份有限公司",
    "4301016509813100767": "江苏银行股份有限公司",
    "4301016509814104041": "江苏银行股份有限公司",
    "4301016509827101946": "江苏银行股份有限公司",
    "4301016509829100872": "江苏银行股份有限公司",
    "4301016509838105663": "江苏银行股份有限公司",
    "4301016519100210521": "江苏银行股份有限公司",
    "4301016529100527482": "江苏银行股份有限公司",
    "12592000000000515": "江苏银行股份有限公司无锡分行"
}

SQL_INSERT_TRANS = 'insert into trans(file_path,bank_name,acc_name,acc_no,trans_date,flow_no,rec_amt,pay_amt,' + \
    ' balance,other_acc_name,other_acc_no,other_bank_name,purpose,abstract,remark,rct_path, task_id,' + \
    ' create_date,update_date,status) ' + \
    ' values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'


SQL_INSERT_BALANCE = 'insert into balance(file_path,bank_name,acc_name,acc_no,' + \
    ' balance, query_date,currency,task_id,' + \
    ' create_date,update_date,status) ' + \
    ' values(?,?,?,?,?,?,?,?,?,?,?)'
