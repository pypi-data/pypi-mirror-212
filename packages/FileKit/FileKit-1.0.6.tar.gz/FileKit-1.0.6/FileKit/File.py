"""
    简易使用python的 文件读写内置模块，
    如果需要相对复杂操作请使用原生的python内置读写模块，以更可靠与高效
"""


def read(file_name, encoding='utf-8', mode='r'):
    """ 读取文本文件全部内容 """
    if mode == 'rb':
        file = open(file_name, mode=mode)
    else:
        file = open(file_name, mode=mode, encoding=encoding)
    text = file.read()
    file.close()
    return text


def write(file_name, text, encoding='utf-8', mode='w'):
    """  覆盖模式写入文本文件内容， 如果文件不存在会新建 """
    if mode == 'wb':
        file = open(file_name, mode=mode, encoding=encoding)
    else:
        file = open(file_name, mode=mode)
    file.write(text)
    file.close()


def read_lines(file_name, encoding='utf-8'):
    """  读取文件为数组 """
    file = open(file_name, mode='r', encoding=encoding)
    ls_text = file.readlines()
    file.close()
    return ls_text


def write_lines(file_name, ls_text, encoding='utf-8'):
    """ 覆盖写入文件数组，如果没有文件会新建 """
    file = open(file_name, mode='w', encoding=encoding)
    file.writelines(ls_text)
    file.close()


def write_append(file_name, text, encoding='utf-8'):
    """ 追加写入 文件。 如果文件不存在会报错 """
    file = open(file_name, mode='a', encoding=encoding)
    file.write(text)
    file.close()




