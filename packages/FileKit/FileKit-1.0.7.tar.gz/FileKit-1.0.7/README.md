# Filekit

简易使用 Python 的文件读写内置模块，针对单词读写操作。省去 open 和 close。

## 介绍

```python
def read(file_name, encoding='utf-8'):
    """读取文本文件全部内容"""
    file = open(file_name, mode='r', encoding=encoding)
    text = file.read()
    file.close()
    return text
```

如果需要相对复杂操作，请使用原生的 Python 内置读写模块，以获得更可靠和高效的处理。

## 安装
使用以下命令安装 Filekit：
```shell
pip install Filekit
```

