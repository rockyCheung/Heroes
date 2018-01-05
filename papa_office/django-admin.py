#!/Users/zhangpenghong/Documents/workspace10/djangoDemo/venv/bin/python2.7
# -*- coding:utf-8 -*-
from django.core import management
import sys


if __name__ == "__main__":
    reload(sys)  # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
    sys.setdefaultencoding('utf-8')
    management.execute_from_command_line()
