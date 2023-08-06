name = "yplib"

import os
from datetime import datetime
import uuid


# 检查文件夹是否存在,不存在,就创建新的
def check_file(file_name):
    if os.path.exists(file_name) is False:
        os.mkdir(file_name)


def list_to_txt(list_data, file_name):
    file_path = 'data'
    check_file(file_path)
    text_file = open(file_path + '/' + str(file_name)
                     + '_' + datetime.today().strftime('%Y%m%d_%H%M%S')
                     + '_' + str(uuid.uuid4().hex).replace('-', '')[0:5]
                     + '.txt',
                     'a', encoding='utf-8')
    for one_str in list_data:
        text_file.write(str(one_str) + '\n')
    text_file.close()
